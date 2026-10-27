import os
import random
import discord
from discord.ext import commands
from datetime import datetime
from keep_alive import keep_alive

# Bot ayarları ve yetkileri
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# ----------------- ETKİNLİKLER (EVENTS) -----------------

@bot.event
async def on_ready():
    print(f'{bot.user.name} olarak Discord\'a bağlandık! Bot 7/24 aktif.')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name="!yardim | 7/24 Canlı"
        )
    )

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel and channel.permissions_for(member.guild.me).send_messages:
        embed = discord.Embed(
            title="🎉 Hoş Geldin!",
            description=f"Aramıza hoş geldin {member.mention}! Sunucumuz seninle **{member.guild.member_count}** kişi oldu.",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        await channel.send(embed=embed)

# ----------------- EĞLENCE & KULLANICI KOMUTLARI -----------------

@bot.command()
async def yardim(ctx):
    embed = discord.Embed(
        title="🤖 Bot Komut Paneli",
        description="Aşağıda kullanabileceğiniz tüm komutlar listelenmiştir:",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="⚡ Genel & Bilgi",
        value="`!ping` - Bot gecikmesini ölçer\n`!sunucu` - Sunucu istatistiklerini gösterir\n`!kullanici [@üye]` - Üye profil detayları\n`!avatar [@üye]` - Profil fotoğrafını büyütür",
        inline=False
    )
    embed.add_field(
        name="🎲 Eğlence",
        value="`!zar` - 1 ile 6 arasında zar atar\n`!yazitura` - Yazı mı tura mı?\n`!espri` - Rastgele komik bir espri yapar\n`!anket <soru>` - Hızlı oylama başlatır",
        inline=False
    )
    embed.add_field(
        name="🛡️ Moderasyon (Yönetici)",
        value="`!sil <sayı>` - Toplu mesaj temizler\n`!kick @üye [sebep]` - Üyeyi sunucudan atar\n`!ban @üye [sebep]` - Üyeyi sunucudan yasaklar",
        inline=False
    )
    embed.set_footer(text="Önek: ! | Render 7/24 Kesintisiz")
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    ms = round(bot.latency * 1000)
    await ctx.send(f"🏓 **Pong!** Gecikme: `{ms}ms`")

@bot.command()
async def sa(ctx):
    await ctx.send(f"Aleyküm selam {ctx.author.mention}, hoş geldin! Nasılsın?")

@bot.command()
async def zar(ctx):
    sayi = random.randint(1, 6)
    await ctx.send(f"🎲 {ctx.author.mention} zar attı: **{sayi}** geldi!")

@bot.command()
async def yazitura(ctx):
    sonuc = random.choice(["Yazı", "Tura"])
    await ctx.send(f"🪙 Para havada döndü ve... **{sonuc}** geldi!")

@bot.command()
async def espri(ctx):
    espriler = [
        "Adamın biri gülmüş, bahçeye dikmişler.",
        "Geçen gün bir espri patlattım, 3 kişi yaralandı.",
        "Röntgen Filmi çektirdik, yakında sinemalarda!",
        "Yıkanan Ton balığına ne denir? - Washington!",
        "Aya ilk bayrağı kim dikmiştir? - Terzi.",
        "Gözlüklerin numaralı mı? - Yok, kale arkası.",
        "İlahi Azrail, sen adamı öldürürsün!"
    ]
    await ctx.send(f"😄 {random.choice(espriler)}")

@bot.command()
async def anket(ctx, *, soru):
    embed = discord.Embed(
        title="📊 Yeni Anket!",
        description=soru,
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"Anketi başlatan: {ctx.author.display_name}")
    mesaj = await ctx.send(embed=embed)
    await mesaj.add_reaction("✅")
    await mesaj.add_reaction("❌")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.display_name} Kullanıcısının Avatarı", color=discord.Color.purple())
    if member.avatar:
        embed.set_image(url=member.avatar.url)
    else:
        embed.description = "Bu kullanıcının özel bir avatarı yok."
    await ctx.send(embed=embed)

@bot.command()
async def kullanici(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 {member.display_name} Bilgileri", color=discord.Color.teal())
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Kullanıcı Adı", value=str(member), inline=True)
    embed.add_field(name="Kullanıcı ID", value=str(member.id), inline=True)
    embed.add_field(name="Hesap Oluşturma", value=member.created_at.strftime("%d.%m.%Y"), inline=True)
    embed.add_field(name="Sunucuya Katılma", value=member.joined_at.strftime("%d.%m.%Y"), inline=True)
    roller = [r.mention for r in member.roles if r.name != "@everyone"]
    embed.add_field(name="Roller", value=" ".join(roller) if roller else "Yok", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def sunucu(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"🏰 {guild.name} İstatistikleri", color=discord.Color.dark_blue())
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Sunucu Sahibi", value=str(guild.owner), inline=True)
    embed.add_field(name="Toplam Üye", value=str(guild.member_count), inline=True)
    embed.add_field(name="Kanal Sayısı", value=str(len(guild.channels)), inline=True)
    embed.add_field(name="Oluşturulma Tarihi", value=guild.created_at.strftime("%d.%m.%Y"), inline=True)
    await ctx.send(embed=embed)

# ----------------- MODERASYON KOMUTLARI -----------------

@bot.command()
@commands.has_permissions(manage_messages=True)
async def sil(ctx, miktar: int = 5):
    await ctx.channel.purge(limit=miktar + 1)
    await ctx.send(f"🧹 **{miktar}** adet mesaj temizlendi.", delete_after=3)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, sebep="Belirtilmedi"):
    await member.kick(reason=sebep)
    await ctx.send(f"👢 {member.mention} sunucudan atıldı. Sebep: **{sebep}**")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, sebep="Belirtilmedi"):
    await member.ban(reason=sebep)
    await ctx.send(f"🔨 {member.mention} sunucudan yasaklandı. Sebep: **{sebep}**")

# Hata yakalama
@sil.error
@kick.error
@ban.error
async def mod_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu komutu kullanmak için yetkiniz yok!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Lütfen gerekli parametreleri girin (Örn: `!sil 10` veya `!kick @üye sebep`).")

# ----------------- SUNUCU BAŞLATMA -----------------

keep_alive()

TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    print("HATA: DISCORD_TOKEN bulunamadı!")
else:
    bot.run(TOKEN)
