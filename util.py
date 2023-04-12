import requests

def open_session():
    API_KEY = {'X-API-key': 'K3TGNSPM'}
    session = requests.Session()
    session.headers.update(API_KEY)
    return session

def get_tick(session):
    response = session.get(f'http://localhost:9999/v1/case')
    case_info = response.json()
    tick = case_info['tick']
    return tick

def get_bid_orders(session, ticker):
    response = session.get(f'http://localhost:9999/v1/securities/book?ticker={ticker}')
    order_book = response.json()
    bids = order_book['bids']
    bids_clean = []
    for bid in bids:
        bid_clean = {
            'price': bid['price'],
            'quantity': bid['quantity']
        }
        bids_clean.append(bid_clean)
    return bids_clean

def get_ask_orders(session, ticker):
    response = session.get(f'http://localhost:9999/v1/securities/book?ticker={ticker}')
    order_book = response.json()
    asks = order_book['asks']
    asks_clean = []
    for ask in asks:
        ask_clean = {
            'price': ask['price'],
            'quantity': ask['quantity']
        }
        asks_clean.append(ask_clean)
    return asks_clean

def get_position(session, ticker):
    response = session.get('http://localhost:9999/v1/securities')
    securities = response.json()
    position = -1
    for security in securities:
        if security['ticker'] == ticker:
            position = security['position']
    return position
