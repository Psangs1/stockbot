import requests
from data.config import OPENAI_API_KEY

FINNHUB_API_KEY = 'cnaktmpr01ql0f8a33h0cnaktmpr01ql0f8a33hg'
BASE_URL = 'https://finnhub.io/api/v1'


BOT_TOCKEN = "MTIwOTY1MDIzODE0NzUzNDg3OQ.G9Uw4M.J_mosyr4xODFyE9OoHd5S56ObmzVqPpkWEeSgs"
CHANNEL = 1209662010804019260

def stock_exists(symbol):
    try:
        url = f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={FINNHUB_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        # If the API returns data for the symbol, it exists
        if data:
            return True
        else:
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error checking symbol existence for {symbol}: {e}")
        return False

def get_stock_info(stock_symbol):
    try:
        url = f'{BASE_URL}/quote?symbol={stock_symbol}&token={FINNHUB_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if 'error' in data:
            return None  # Return None for invalid stock symbol

        # Extract relevant information from the API response
        stock_price = data.get('c', 'N/A')
        return f"The current price of {stock_symbol} is ${stock_price}"

    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"
def get_stock_price(symbol):
    try:
        url = f'{BASE_URL}/quote?symbol={symbol}&token={FINNHUB_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if 'error' in data:
            return None  # Return None for invalid stock symbol

        # Extract relevant information from the API response
        stock_price = data.get('c', 'N/A')
        return stock_price

    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"


def get_top_headlines(categories, limit=5):
    try:
        headlines = []

        for category in categories:
            url = f'{BASE_URL}/news?category={category}&token={FINNHUB_API_KEY}'
            response = requests.get(url)
            response.raise_for_status()
            news_data = response.json()

            if 'error' not in news_data:
                headlines.extend([
                    f"**{category.capitalize()} News:**",
                    *[f"{article['source']} - {article['headline']} ({article['url']})" for article in news_data[:limit]]
                ])
            else:
                headlines.append(f"Error fetching news for {category}: {news_data['error']}")

        return "\n".join(headlines)

    except requests.exceptions.RequestException as e:
        return f"Error fetching news: {e}"

def company_news(symbol, start, finish, limit = 5):
    try:
        stories = []
        url = f'{BASE_URL}/company-news?symbol={symbol}&from={start}&to={finish}&token={FINNHUB_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
        if 'error' not in news_data:
            stories.extend([
                f"**{symbol.capitalize()} News:**",
                *[f"{article['source']} - {article['headline']} ({article['url']})" for article in news_data[:limit]]
            ])
        else:
            stories.append(f"Error fetching news for {symbol}: {news_data['error']}")
        return "\n".join(stories)
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching news: {e}"
#peers
def company_peers(symbol, limit=5):
    try:
        peers = []
        url = f'{BASE_URL}/stock/peers?symbol={symbol}&token={FINNHUB_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Check if data is empty
        if not data:
            return ["No peers found for symbol {symbol}"]

        # Extend the peers list
        peers.extend(data[:limit])

        # Return the array with a success message
        return [
            "Peers for {symbol}:",
            peers
        ]
    except requests.exceptions.RequestException as e:
        # Return the array with an error message in case of an exception
        return [
            f"Error fetching data: {e}"
        ]
#financials

