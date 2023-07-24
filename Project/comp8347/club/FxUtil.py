import yfinance as yf
from datetime import datetime, timedelta

SYMBOL_MAP = {
    "CAD": None,
    "USD": "CADUSD=X",
    "INR": "CADINR=X",
    "PKR": "CADPKR=X",
    "YEN": "CADJPY=X",
}

cache = {}
start_dt = datetime.now().date() - timedelta(days=2)
end_dt = start_dt + timedelta(days=1)


def compute_fx_rate(symbol):
    if symbol == 'CAD':
        return 1
    if symbol not in SYMBOL_MAP:
        print(f"unknown symbol '{symbol}', cannot get fx")
        return 0.0
    ticker = SYMBOL_MAP[symbol]

    if ticker not in cache:
        data = yf.download(ticker, start=start_dt, end=end_dt)
        data = data.iloc[0]['Adj Close']
        cache[ticker] = data
    fx = cache[ticker]
    # print(f"Obtained fx value of {symbol} w.r.t. CAD as: {fx}")
    return fx


def compute_fx_amount(symbol, cad_amount):
    return cad_amount * compute_fx_rate(symbol)


def clear_fx_cache():
    cache.clear()


if __name__ == "__main__":
    compute_fx_rate("USD")
    print(compute_fx_amount("USD", 1000.0))
    print(cache)
