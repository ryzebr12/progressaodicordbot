import discord
from discord.ext import commands
import yfinance as yf

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="/", intents=intents)

# Replace 'YOUR_SERVER_ID' with the actual server ID where you want to restrict the bot usage
SERVER_ID = '1044714888750178335'


def get_exchange_rate(base_currency, target_currency):
    ticker = f"{base_currency}{target_currency}=X"
    data = yf.download(tickers=ticker, period='1d')
    rate = data["Close"].iloc[-1]
    return rate


def convert_currency(amount, exchange_rate):
    converted_amount = amount * exchange_rate
    return converted_amount


def print_currency_options():
    options = {
        "1": "Euro (EUR)",
        "2": "Iene japonês (JPY)",
        "3": "Libra esterlina (GBP)",
        "4": "Franco suíço (CHF)",
        "5": "Qatari Riyal (QAR)",
        "6": "China Yuan Renminbi (CNY)",
        "7": "Dólar dos Estados Unidos (USD)",
        "8": "Real Brasileiro (BRL)"
    }
    options_str = "\n".join([f"{key}. {value}" for key, value in options.items()])
    return f"Escolha as moedas para conversão:\n{options_str}"


def get_currency_code(option):
    codes = {
        "1": "EUR",
        "2": "JPY",
        "3": "GBP",
        "4": "CHF",
        "5": "QAR",
        "6": "CNY",
        "7": "USD",
        "8": "BRL"
    }
    return codes.get(option)


@bot.event
async def on_ready():
    print("Bot está pronto!")


@bot.command()
async def convert(ctx, base_option: str, target_option: str, amount: float):
    if ctx.guild.id != int(SERVER_ID):
        await ctx.send("Desculpe, este bot só pode ser usado em um servidor específico.")
        return

    base_currency = get_currency_code(base_option)
    target_currency = get_currency_code(target_option)

    if base_currency is None or target_currency is None:
        await ctx.send("Opção inválida. Por favor, selecione uma opção válida.")
        return

    try:
        exchange_rate = get_exchange_rate(base_currency, target_currency)

        result = ""
        result += f"Moeda de origem: {base_currency}\n"
        result += f"Moeda de destino: {target_currency}\n"
        result += f"Valor original: {amount} {base_currency}\n"
        result += f"Taxa de câmbio atual: 1 {base_currency} = {exchange_rate} {target_currency}\n"
        result += f"Valor convertido: {convert_currency(amount, exchange_rate):.2f} {target_currency}"

        await ctx.send(result)

    except Exception as e:
        await ctx.send(f"Ocorreu um erro ao obter a taxa de câmbio: {str(e)}")


@bot.command()
async def currencies(ctx):
    if ctx.guild.id != int(SERVER_ID):
        await ctx.send("Desculpe, este bot só pode ser usado em um servidor específico.")
        return

    options = print_currency_options()
    await ctx.send(options)


@bot.command()
async def currency_help(ctx):
    if ctx.guild.id != int(SERVER_ID):
        await ctx.send("Desculpe, este bot só pode ser usado em um servidor específico.")
        return

    options = print_currency_options()
    await ctx.send(f"Opções de moedas:\n{options}\n\nUse o comando `/convert <moeda_origem> <moeda_destino> <valor>` para realizar a conversão de moedas.")


bot.run("MTEyNjMxMTMxMzc5NTE5NTAxMA.GpB6IT.11hWY9Hh1T8-Kef5Ef9Mrno_49o8ZODs3Cjgiw")
