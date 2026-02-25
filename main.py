import discord
import os
import asyncio
import random
from discord.ext import tasks
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True # ضروري ليتمكن البوت من قراءة الرسائل والرد عليها

client = discord.Client(intents=intents)

# --- إعدادات القنوات ---
WELCOME_CHANNEL_ID = 1456605013559218217 
LEAVE_CHANNEL_ID = 1469739078089179291
REMINDER_CHANNEL_ID = 1476013464832184583
CHAT_CHANNEL_ID = 1456597406366826550 # قناة الرد على السلام

# رابط صورة سوداء فخمة للترحيب والخروج
BLACK_IMAGE_URL = "https://wallpapercave.com/wp/wp2593000.jpg"

# كلمات دينية فقط للتذكير
REMINDERS = [
    "✨ **تذكير:** سبحان الله وبحمده، سبحان الله العظيم.",
    "🌟 **تذكير:** لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير.",
    "📿 **تذكير:** استغفر الله العظيم واتوب إليه.",
    "📖 **تذكير:** صلوا على من بكى شوقاً لرؤيتنا، اللهم صلِ وسلم على نبينا محمد.",
    "💎 **تذكير:** سبحان الله، والحمد لله، ولا إله إلا الله، والله أكبر."
]

@client.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح باسم: {client.user}')
    if not auto_reminder.is_running():
        auto_reminder.start()

# 1. التذكير التلقائي (كلمات دينية)
@tasks.loop(seconds=20.0) 
async def auto_reminder():
    await client.wait_until_ready() 
    channel = client.get_channel(REMINDER_CHANNEL_ID)
    if channel:
        message = random.choice(REMINDERS)
        embed = discord.Embed(description=message, color=0x000000) # لون أسود
        await channel.send(embed=embed)

# 2. الرد التلقائي على السلام عليكم
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.channel.id == CHAT_CHANNEL_ID:
        if message.content == "السلام عليكم":
            await message.reply("وعليكم السلام ورحمة الله وبركاته")

# 3. ترحيب بصورة سوداء وشكل الحساب
@client.event
async def on_member_join(member):
    channel = client.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="مرحباً بك في السيرفر! ✨",
            description=f"يا هلا والله بـ {member.mention}\nنورتنا يا بطل، نتمنى لك وقتاً ممتعاً!",
            color=0x000000
        )
        embed.set_thumbnail(url=member.display_avatar.url) # صورة حساب الشخص
        embed.set_image(url=BLACK_IMAGE_URL) # الصورة السوداء
        await channel.send(embed=embed)

# 4. خروج بصورة سوداء وشكل الحساب
@client.event
async def on_member_remove(member):
    channel = client.get_channel(LEAVE_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="وداعاً.. نراك قريباً 💔",
            description=f"العضو **{member.name}** غادرنا أو تم طرده..\nنتمنى له التوفيق أينما كان.",
            color=0x000000
        )
        embed.set_thumbnail(url=member.display_avatar.url) # صورة حساب الشخص
        embed.set_image(url=BLACK_IMAGE_URL) # الصورة السوداء
        await channel.send(embed=embed)

keep_alive()
client.run(os.getenv('TOKEN'))
