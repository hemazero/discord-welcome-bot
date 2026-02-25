import discord
import os
import asyncio
import random
from discord.ext import tasks
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True 

client = discord.Client(intents=intents)

# القنوات (تأكد أن هذا ما تراه في GitHub الآن)
WELCOME_CHANNEL_ID = 1456605013559218217 
LEAVE_CHANNEL_ID = 1469739078089179291
REMINDER_CHANNEL_ID = 1476013464832184583 # الرقم الجديد

REMINDERS = [
    "✨ **تذكير:** سبحان الله وبحمده، سبحان الله العظيم.",
    "💡 **معلومة:** هل تعلم أن البوت الآن يعمل 24 ساعة بفضل Render؟",
    "🕒 **تذكير:** لا تنسوا شرب الماء والقيام بتمريض أعينكم من الشاشة.",
    "🌟 **اذكروا الله يذكركم:** لا إله إلا الله وحده لا شريك له."
]

@client.event
async def on_ready():
    print(f'تم التشغيل باسم: {client.user}')
    print(f'البوت مبرمج للإرسال في القناة: {REMINDER_CHANNEL_ID}') # سطر للتأكد من الـ Logs
    if not auto_reminder.is_running():
        auto_reminder.start()

@tasks.loop(seconds=20.0) 
async def auto_reminder():
    await client.wait_until_ready() 
    channel = client.get_channel(REMINDER_CHANNEL_ID)
    if channel:
        message = random.choice(REMINDERS)
        embed = discord.Embed(description=message, color=discord.Color.blue())
        await channel.send(embed=embed)
    else:
        print("خطأ: لم أستطع العثور على القناة، تأكد من الصلاحيات!")

keep_alive()
client.run(os.getenv('TOKEN'))
