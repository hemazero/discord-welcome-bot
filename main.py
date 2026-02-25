import discord
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True 

client = discord.Client(intents=intents)

# --- إعدادات القنوات ---
WELCOME_CHANNEL_ID = 1456605013559218217 
LEAVE_CHANNEL_ID = 1469739078089179291

@client.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح باسم: {client.user}')

# 1. حدث دخول عضو جديد (يرسل لقناة الويلكم)
@client.event
async def on_member_join(member):
    channel = client.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f"يا هلا والله بـ {member.mention}! نورت السيرفر ✨")

# 2. حدث خروج عضو أو طرده (يرسل لقناة الطرد)
@client.event
async def on_member_remove(member):
    channel = client.get_channel(LEAVE_CHANNEL_ID)
    if channel:
        await channel.send(f"العضو **{member.name}** غادر السيرفر أو تم طرده.. وداعاً 👋")

keep_alive()
client.run(os.getenv('TOKEN'))
