import discord
import os
import asyncio
from discord.ext import tasks
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True 

client = discord.Client(intents=intents)

# --- إعدادات القنوات ---
WELCOME_CHANNEL_ID = 1456605013559218217 
LEAVE_CHANNEL_ID = 1469739078089179291
REMINDER_CHANNEL_ID = 1456597406366826550  # القناة التي سيرسل فيها التذكير التلقائي

# قائمة بالأذكار أو التنبيهات التي سيرسلها البوت
REMINDERS = [
    "✨ تذكير: سبحان الله وبحمده، سبحان الله العظيم.",
    "💡 معلومة: هل تعلم أن البوت الآن يعمل 24 ساعة بفضل Render؟",
    "🕒 تذكير: لا تنسوا شرب الماء والقيام بتمريض أعينكم من الشاشة.",
    "🌟 اذكروا الله يذكركم: لا إله إلا الله وحده لا شريك له."
]

@client.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح باسم: {client.user}')
    if not auto_reminder.is_running():
        auto_reminder.start()

# دالة التذكير التلقائي (تعمل كل ساعة مثلاً)
@tasks.loop(hours=1.0) 
async def auto_reminder():
    channel = client.get_channel(REMINDER_CHANNEL_ID)
    if channel:
        import random
        message = random.choice(REMINDERS)
        await channel.send(message)

# حدث دخول عضو جديد
@client.event
async def on_member_join(member):
    channel = client.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f"يا هلا والله بـ {member.mention}! نورت السيرفر ✨")

# حدث خروج عضو أو طرده
@client.event
async def on_member_remove(member):
    channel = client.get_channel(LEAVE_CHANNEL_ID)
    if channel:
        await channel.send(f"العضو **{member.name}** غادر السيرفر أو تم طرده.. وداعاً 👋")

keep_alive()
client.run(os.getenv('TOKEN'))
