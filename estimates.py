import requests
from data.config import DISCORD_BOT_TOKEN, FINHUB_API_KEY

FINNHUB_API_KEY = FINHUB_API_KEY
BASE_URL = 'https://finnhub.io/api/v1'


BOT_TOCKEN = DISCORD_BOT_TOKEN
CHANNEL = 1209662010804019260

def get_stock_recommendations_trend(symbol):
    try:
        url = f'https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token={FINNHUB_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if isinstance(data, list) and data:  # Check if data is a non-empty list
            # Extract previous and last recommendations
            previous_recommendation_period = data[-2]['period'] 
            prev_rec_buy = data[-2]['buy']
            prev_rec_sell = data[-2]['sell']
            last_recommendation_period = data[-1]['period'] 
            last_rec_buy = data[-1]['buy']
            last_rec_sell = data[-1]['sell']

            result = (
                f"Recommendations Trend for {symbol}:\n"
                f"Previous: {previous_recommendation_period} \n buy recommendation: {prev_rec_buy}, sell recommendation: {prev_rec_sell}\n"
                f"Last: {last_recommendation_period} \n buy recommendation: {last_rec_buy}, sell recommendation: {last_rec_sell}\n"
            )
        else:
            result = f"No recommendation trend data available for {symbol}"
        
        return result


    except requests.exceptions.RequestException as e:
        return f"Error fetching recommendations trend: {e}"
    
def estimate_surprise(symbol, limit = 5):
    try:
        surprises = []
        url = f'https://finnhub.io/api/v1/stock/earnings?symbol={symbol}&token={FINNHUB_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'error' not in data:
            surprises.extend([
                f"**{symbol.capitalize()} Surprises:**",
                *[f"{article['actual']} - {article['estimate']} ({article['surprise']})" for article in data[:limit]]
            ])
        else:
            surprises.append(f"Error fetching news for {symbol}: {data['error']}")
        return "\n".join(surprises)
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching recommendations trend: {e}"
