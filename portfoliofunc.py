from data.config import OPENAI_API_KEY
import stockcommands.stock as sc
import stockcommands.estimates as est
import discord
import game.portfolio as Portfolio
from game.portfolio import *

USERPORTFOLIO = None

async def createportfolio(ctx):
    global USERPORTFOLIO
    embed = discord.Embed(
        title="Portfolio",
        description="Portfolio has been created! This is where you can mannage investing in different stocks, and seeing how they perform!",
    )
    USERPORTFOLIO = Portfolio.myPortfolio()
    
    await ctx.send(embed=embed)

async def describeportfolio(ctx):
    global USERPORTFOLIO
    embed = discord.Embed(
        title="Portfolio",
        description=f"""Portfolio has been created! This is where you can mannage investing in different stocks, and seeing how they perform!\n
        You can invest in up to 5 stocks total. To add a stock to your portfolio, type !addstock followed by the stock symbol. To remove a stock from your portfolio, type !removestock followed by the stock symbol.\n
        Current stocks include: {USERPORTFOLIO.getStocks()}
        """,
    )
    
    await ctx.send(embed=embed)

async def addstock(ctx, stock, quantity):
    global USERPORTFOLIO
    success, message = USERPORTFOLIO.addStock(stock, quantity)
    if success:
        embed = discord.Embed(
            title="Portfolio",
            description=f"Added {stock} to your portfolio!",
        )
    else:
        embed = discord.Embed(
            title="Portfolio",
            description=f"{message}",
        )
    await ctx.send(embed=embed)

async def removestock(ctx, stock, quantity):
    global USERPORTFOLIO
    success, message = USERPORTFOLIO.removeStock(stock, quantity)
    if success:
        embed = discord.Embed(
            title="Portfolio",
            description=f"Removed {stock} from your portfolio!",
        )
    else:
        embed = discord.Embed(
            title="Portfolio",
            description=f"{message}",
        )
    await ctx.send(embed=embed)
    
async def trackportfolio(ctx):
    global USERPORTFOLIO
    netreturns, netreturnpersymbol = USERPORTFOLIO.trackPortfolio()
    embed = discord.Embed(
        title="Portfolio",
        description=f"""Net returns: {netreturns}\n
        Net returns per stock: {netreturnpersymbol}
        """,
    )
    await ctx.send(embed=embed)