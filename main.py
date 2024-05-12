from discord.ext import commands, tasks
import discord
import openai
from data.config import OPENAI_API_KEY, DISCORD_BOT_TOKEN  # Replace with your actual config structure
from gpt.gpt import generate_response, stockinfo
import gpt.gpt as g
from stockcommands.stock import *
from stockcommands.estimates import get_stock_recommendations_trend, estimate_surprise
from game.portfoliofunc import *


openai.api_key = OPENAI_API_KEY


BOT_TOCKEN = DISCORD_BOT_TOKEN
CHANNEL = 1209662010804019260

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Hello! stockbot is ready!")
    channel = bot.get_channel(CHANNEL)
    await channel.send("Hello! I'm ready!")
    # timed_news.start()
    
@bot.command()
async def hello(ctx):
    await ctx.send(embed=discord.Embed(description="Hello!")) 


BASE_URL = 'https://finnhub.io/api/v1'

@bot.command(name='stockinfo')
async def stock_info_command(ctx, stock_symbol):
    result = get_stock_info(stock_symbol)
    if result is not None:
        await ctx.send(embed=discord.Embed(description=result))
    else:
        await ctx.send(embed=discord.Embed(description=f"Invalid stock symbol: {stock_symbol}"))
        
#stocknews
@bot.command(name='stocknews')
async def stock_news_command(ctx, *categories):
    if not categories:
        await ctx.send(embed=discord.Embed(description="Please provide at least one stock category."))
        return

    result = get_top_headlines(categories)

    if result is not None:
        await ctx.send(embed=discord.Embed(description=result))
    else:
        await ctx.send(embed=discord.Embed(description="Error fetching stock news."))
        
#companynews
@bot.command(name='companynews')
async def company_news_command(ctx, companies, start, finish):
    if not companies:
        await ctx.send(embed=discord.Embed(description="Please provide at least one company symbol."))
        return
    result = company_news(companies, start, finish)

    if result is not None:
        await ctx.send(embed=discord.Embed(description=result))
    else:
        await ctx.send(embed=discord.Embed(description="Error fetching company news."))

@bot.command(name='companypeers')
async def company_news_command(ctx, symbol):
    if not symbol:
        await discord.Embed(description="Please provide at least one company symbol.").send(ctx)
        return

    result = company_peers(symbol)

    if result is not None:
        await discord.Embed(description=result).send(ctx)
    else:
        await discord.Embed(description="Error fetching company news.").send(ctx)

@bot.command(name='stockestimate')
async def stock_estimate_command(ctx, symbol):
    if not symbol:
        await discord.Embed(description="Please provide at least one company symbol.").send(ctx)
        return

    result = get_stock_recommendations_trend(symbol)

    if result is not None:
        await discord.Embed(description=result).send(ctx)
    else:
        await discord.Embed(description="Error fetching company news.").send(ctx)
        
@bot.command(name='stocksurprise')
async def company_news_command(ctx, symbol):
    if not symbol:
        await discord.Embed(description="Please provide at least one company symbol.").send(ctx)
        return

    result = estimate_surprise(symbol)

    if result is not None:
        await discord.Embed(description=f"Surprise: {result}").send(ctx) #f"Surprise: {result)
    else:
        await discord.Embed(title="Error fetching company news.").send(ctx)

@bot.command(name='stockexists')
async def stockexists(ctx, stock_symbol):
    await ctx.send(embed=discord.Embed(description=str(stock_exists(stock_symbol))))

@bot.command(name='askgpt')
async def ask_gpt_command(ctx, *, question):
    gpt_response = generate_response(question)
    await ctx.send(embed=discord.Embed(description=f"GPT-3.5 says: {gpt_response}"))
@bot.command(name='askgptstock')
async def ask_gpt_stock_command(ctx,*, question):
    gpt_response = stockinfo(question)
    await ctx.send(embed=discord.Embed(description=f"GPT-3.5 says: {gpt_response}"))
@bot.command(name='askgptestimate')
async def ask_gpt_stock_command(ctx,*, question):
    gpt_response = g.estimates(question)
    await discord.Embed(description=f"GPT-3.5 says: {gpt_response}").send(ctx)  

#timmed commands
@tasks.loop(minutes=60) 
async def timed_news():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL)
    await channel.send(embed=discord.Embed(description=get_top_headlines("general", 1)))

#portfolio commands
@bot.command(name='createportfolio')
async def startportfolio(ctx):
    await createportfolio(ctx)

@bot.command(name='viewportfolio')
async def viewportfolio(ctx ):
    await describeportfolio(ctx) 
    
@bot.command(name='addstock')
async def addstocks(ctx, stock, quantity):
    await addstock(ctx, stock, quantity) 
    
@bot.command(name='removestock')
async def removestocks(ctx, stock, quantity):
    await removestock(ctx, stock, quantity) 
    
@bot.command(name='trackportfolio')
async def portfolioprgoress(ctx):
    await trackportfolio(ctx) 
    
#run
bot.run(BOT_TOCKEN)
        
