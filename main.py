import discord
import os
import asyncio
import random
from datetime import datetime, timedelta
from discord.ext import tasks
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True 

client = discord.Client(intents=intents)

# --- الإعدادات ---
WELCOME_CHANNEL_ID = 1456605013559218217 
LEAVE_CHANNEL_ID = 1469739078089179291
REMINDER_CHANNEL_ID = 1476013464832184583
CHAT_CHANNEL_ID = 1456597406366826550
ADMIN_ROLE_ID = 1456601653171196034 # رتبة الإدارة المسموح لها بالمسح

BLACK_IMAGE_URL = "https://wallpapercave.com/wp/wp2593000.jpg"

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

@tasks.loop(seconds=20.0) 
async def auto_reminder():
    await client.wait_until_ready() 
    channel = client.get_channel(REMINDER_CHANNEL_ID)
    if channel:
        message = random.choice(REMINDERS)
        embed = discord.Embed(description=message, color=0x000000)
        await channel.send(embed=embed)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # 1. الرد على السلام
    if message.channel.id == CHAT_CHANNEL_ID and message.content == "السلام عليكم":
        await message.reply("وعليكم السلام ورحمة الله وبركاته")

    # 2. أمر المسح لرتبة محددة (/مسح)
    if message.content == "/مسح":
        # التأكد من وجود الرتبة لدى العضو
        role = discord.utils.get(message.author.roles, id=ADMIN_ROLE_ID)
        
        if role:
            # حساب وقت "قبل 24 ساعة" من الآن
            one_day_ago = datetime.utcnow() - timedelta(days=1)
            
            # حذف الرسائل التي أرسلت في آخر 24 ساعة
            deleted = await message.channel.purge(after=one_day_ago)
            
            msg = await message.channel.send(f"✅ تم تنظيف الروم وحذف {len(deleted)} رسالة (آخر 24 ساعة).")
            await asyncio.sleep(3)
            await msg.delete()
        else:
            await message.reply("❌ عذراً، هذا الأمر مخصص فقط لأصحاب الرتبة المحددة.")

@client.event
async def on_member_join(member):
    channel = client.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(title="مرحباً بك في السيرفر! ✨", description=f"يا هلا والله بـ {member.mention}\nنورتنا يا بطل، نتمنى لك وقتاً ممتعاً!", color=0x000000)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=BLACK_IMAGE_URL)
        await channel.send(embed=embed)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(LEAVE_CHANNEL_ID)
    if channel:
        embed = discord.Embed(title="وداعاً.. نراك قريباً 💔", description=f"العضو **{member.name}** غادرنا أو تم طرده..", color=0x000000)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=BLACK_IMAGE_URL)
        await channel.send(embed=embed)

keep_alive()
client.run(os.getenv('TOKEN'))
