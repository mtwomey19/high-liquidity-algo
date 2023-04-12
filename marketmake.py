import util
from time import sleep

quantity = 5_000
ticker = "RY"
required_spread = 0.02

def get_highest_bid_price(session, ticker):
    bids = util.get_bid_orders(session, ticker)
    highest_bid_price = bids[0]['price']
    return highest_bid_price

def get_lowest_ask_price(session, ticker):
    asks = util.get_ask_orders(session, ticker)
    lowest_ask_price = asks[0]['price']
    return lowest_ask_price

def place_buy_order(session, ticker, highest_bid, lowest_ask, spread_divisor):
    spread = lowest_ask - highest_bid
    premium = spread / spread_divisor
    buy_price = highest_bid + premium
    session.post(f'http://localhost:9999/v1/orders?ticker={ticker}&type=LIMIT&quantity={quantity}&action=BUY&price={buy_price}')

def place_sell_order(session, ticker, highest_bid, lowest_ask, spread_divisor):
    spread = lowest_ask - highest_bid
    premium = spread / spread_divisor
    sell_price = lowest_ask - premium
    session.post(f'http://localhost:9999/v1/orders?ticker={ticker}&type=LIMIT&quantity={quantity}&action=SELL&price={sell_price}')

def main():
    session = util.open_session()
    tick = util.get_tick(session)
    while tick > 0:
        highest_bid_price = get_highest_bid_price(session, ticker)
        lowest_ask_price = get_lowest_ask_price(session, ticker)
        position = util.get_position(session, ticker)
        spread = lowest_ask_price - highest_bid_price
        if spread > required_spread and (position < 10_000 and position > -10_000):
            spread_divisor = 6
            place_buy_order(session, ticker, highest_bid_price, lowest_ask_price, spread_divisor)
            place_sell_order(session, ticker, highest_bid_price, lowest_ask_price, spread_divisor)
            print('Order placed :)')
            sleep(0.3)
        if position >= 10_000:
            place_sell_order(session, ticker, highest_bid_price, lowest_ask_price, spread_divisor=4.5)
            sleep(1)
        if position <= -10_000:
            place_buy_order(session, ticker, highest_bid_price, lowest_ask_price, spread_divisor=4.5)
            sleep(1)

main()
