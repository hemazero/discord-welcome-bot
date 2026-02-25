import discord
import os
from keep_alive import keep_alive

# إعداد الصلاحيات
intents = discord.Intents.default()
intents.members = True 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح باسم: {client.user}')

@client.event
async def on_member_join(member):
    # --- استبدل الرقم التالي بـ ID القناة التي تريد الترحيب فيها ---
    channel_id = 1456605013559218217 
    channel = client.get_channel(channel_id)
    
    if channel:
        await channel.send(f"يا هلا والله بـ {member.mention}! نورت السيرفر ✨")

# تشغيل خادم الحماية من النوم
keep_alive()

# تشغيل البوت باستخدام التوكن المخفي في Secrets (Render)
client.run(os.getenv('TOKEN'))
