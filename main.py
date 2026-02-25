import discord
import os
import asyncio
import random
from discord.ext import tasks
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True 

client = discord.Client(intents=intents)

# --- إعدادات القنوات ---
WELCOME_CHANNEL_ID = 1456605013559218217 
LEAVE_CHANNEL_ID = 1469739078089179291
REMINDER_CHANNEL_ID = 1456597406366826550 

REMINDERS = [
    "✨ **تذكير:** سبحان الله وبحمده، سبحان الله العظيم.",
    "💡 **معلومة:** هل تعلم أن البوت الآن يعمل 24 ساعة بفضل Render؟",
    "🕒 **تذكير:** لا تنسوا شرب الماء والقيام بتمريض أعينكم من الشاشة.",
    "🌟 **اذكروا الله يذكركم:** لا إله إلا الله وحده لا شريك له."
]

@client.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح باسم: {client.user}')
    if not auto_reminder.is_running():
        auto_reminder.start()

# دالة التذكير التلقائي (تعمل كل 20 ثانية كما طلبت)
@tasks.loop(seconds=20.0) 
async def auto_reminder():
    channel = client.get_channel(REMINDER_CHANNEL_ID)
    if channel:
        message = random.choice(REMINDERS)
        # إرسال التذكير في إطار (Embed) ليكون شكله احترافي
        embed = discord.Embed(description=message, color=discord.Color.blue())
        await channel.send(embed=embed)

@client.event
async def on_member_join(member):
    channel = client.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f"يا هلا والله بـ {member.mention}! نورت السيرفر ✨")

@client.event
async def on_member_remove(member):
    channel = client.get_channel(LEAVE_CHANNEL_ID)
    if channel:
        await channel.send(f"العضو **{member.name}** غادر السيرفر أو تم طرده.. وداعاً 👋")

keep_alive()
client.run(os.getenv('TOKEN'))
