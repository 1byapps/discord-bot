import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} olarak Discord\'a bağlandık! Bot aktif.')
    await bot.change_presence(activity=discord.Game(name="!yardim | 7/24 Aktif"))

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Gecikme: {latency}ms')

@bot.command()
async def sa(ctx):
    await ctx.send(f'Aleyküm selam {ctx.author.mention}, hoş geldin!')

@bot.command()
async def yardim(ctx):
    mesaj = """
**🤖 Bot Komutları:**
`!ping` - Botun gecikme süresini gösterir.
`!sa` - Selam verir.
`!sil <sayı>` - Belirtilen sayıda mesajı siler.
"""
    await ctx.send(mesaj)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def sil(ctx, miktar: int = 5):
    await ctx.channel.purge(limit=miktar + 1)
    await ctx.send(f'🧹 {miktar} adet mesaj silindi.', delete_after=3)

# Canlı tutma web sunucusunu başlat
keep_alive()

# Token güvenli ortam değişkeninden okunur
TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    print("HATA: DISCORD_TOKEN bulunamadı!")
else:
    bot.run(TOKEN)
