import discord
from discord.ext import commands
import yfinance as yf

# Configuração do bot
TOKEN = 'token'
bot_prefix = '/'

# Definição das intenções
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Criação do bot
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.command(name='conversao')
async def conversao(ctx, moeda_origem, moeda_destino, quantidade):
    try:
        data = yf.download(f'{moeda_origem}{moeda_destino}=X')
        taxa = data['Close'].iloc[-1]
        resultado = float(quantidade) * taxa

        await ctx.send(f'{quantidade} {moeda_origem} equivalem a {resultado} {moeda_destino}')
    except:
        await ctx.send('Erro ao realizar a conversão')

@bot.command(name='ajuda')
async def ajuda(ctx):
    moedas_disponiveis = ['USD', 'EUR', 'JPY', 'GBP', 'AUD', 'CAD']
    moedas_formatadas = ', '.join(moedas_disponiveis)

    await ctx.send(f'Opções de moedas disponíveis: {moedas_formatadas}')

bot.run(TOKEN)
