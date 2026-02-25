import discord
import os
import asyncio
import random
from discord.ext import tasks
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True 

client = discord.Client(intents=intents)

# رابط الصورة السوداء الموحدة
BLACK_IMAGE_URL = "https://wallpapercave.com/wp/wp2593000.jpg"

REMINDERS = [
    "✨ **تذكير:** سبحان الله وبحمده، سبحان الله العظيم.",
    "🌟 **تذكير:** لا إله إلا الله وحده لا شريك له.",
    "📿 **تذكير:** استغفر الله العظيم واتوب إليه.",
    "📖 **تذكير:** اللهم صلِ وسلم على نبينا محمد."
]

@client.event
async def on_ready():
    print(f'البوت العام جاهز! متصل باسم: {client.user}')
    if not auto_reminder.is_running():
        auto_reminder.start()

# 1. التذكير التلقائي (يبحث عن قناة باسم "تذكير" أو "reminders")
@tasks.loop(seconds=60.0) 
async def auto_reminder():
    await client.wait_until_ready()
    for guild in client.guilds:
        channel = discord.utils.get(guild.text_channels, name="تذكير") or \
                  discord.utils.get(guild.text_channels, name="reminders")
        if channel:
            message = random.choice(REMINDERS)
            embed = discord.Embed(description=message, color=0x000000)
            await channel.send(embed=embed)

# 2. الأوامر (السلام والمسح)
@client.event
async def on_message(message):
    if message.author == client.user: return

    # الرد على السلام في أي قناة
    if message.content == "السلام عليكم":
        await message.reply("وعليكم السلام ورحمة الله وبركاته")

    # أمر المسح -مسح (يعتمد على صلاحيات الشخص وليس رتبة محددة)
    if message.content == "-مسح":
        if message.author.guild_permissions.manage_messages:
            deleted = await message.channel.purge(limit=100)
            msg = await message.channel.send(f"✅ تم تنظيف {len(deleted)} رسالة.")
            await asyncio.sleep(3)
            await msg.delete()
        else:
            await message.reply("❌ تحتاج صلاحية `إدارة الرسائل` لاستخدام هذا الأمر.")

# 3. ترحيب عام (يبحث عن قناة باسم "welcome" أو "الترحيب")
@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome") or \
              discord.utils.get(member.guild.text_channels, name="الترحيب")
    if channel:
        embed = discord.Embed(title="مرحباً بك! ✨", description=f"يا هلا بـ {member.mention} نورتنا!", color=0x000000)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=BLACK_IMAGE_URL)
        await channel.send(embed=embed)

# 4. خروج عام (يبحث عن قناة باسم "logs" أو "المغادرين")
@client.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="logs") or \
              discord.utils.get(member.guild.text_channels, name="المغادرين")
    if channel:
        embed = discord.Embed(title="وداعاً 💔", description=f"العضو **{member.name}** غادرنا..", color=0x000000)
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)

keep_alive()
client.run(os.getenv('TOKEN'))
