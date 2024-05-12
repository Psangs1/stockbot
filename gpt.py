from openai import OpenAI
from data.config import OPENAI_API_KEY
import stockcommands.stock as sc
import stockcommands.estimates as est
from stockcommands.stock import get_stock_info

client = OpenAI(api_key=OPENAI_API_KEY)
def generate_response(prompt):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a stock analysist, informing users on the best trends of data and knowledgable on a wide selection of trades"},
        {"role": "user", "content": prompt}
        ]
    )

    return (completion.choices[0].message.content)
def stockinfo(prompt):
    symbol = prompt[-4:]
    print(symbol)
    stockinfo = get_stock_info(symbol)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a stock analyst, informing users on the best trends of data and knowledgable on a wide selection of trades"},
            {"role": "user", "content": f"{prompt} + stock info: {stockinfo}"}
        ]
    )
    return (completion.choices[0].message.content)

def estimates(prompt):
    symbol = prompt[-4:]
    stockestimate = est.get_stock_recommendations_trend(symbol)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a stock analyst, informing users on the best trends of data and knowledgable on a wide selection of trades"},
            {"role": "user", "content": f"{prompt} + use these stock estimates: {stockestimate}, surprise: {est.estimate_surprise(symbol)}"}
        ]
    )
    return (completion.choices[0].message.content)
