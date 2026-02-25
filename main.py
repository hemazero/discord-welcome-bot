import discord
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True  # ضروري جداً لرؤية دخول وخروج الأعضاء

client = discord.Client(intents=intents)

# --- ضع ID القناة هنا ---
CHANNEL_ID = 1456605013559218217 

@client.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح باسم: {client.user}')

# 1. حدث دخول عضو جديد (ترحيب)
@client.event
async def on_member_join(member):
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"يا هلا والله بـ {member.mention}! نورت السيرفر ✨")

# 2. حدث خروج عضو أو طرده (وداع)
@client.event
async def on_member_remove(member):
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        # يمكنك تغيير الرسالة كما تحب
        await channel.send(f"للأسف، {member.name} غادرنا أو تم طرده.. وداعاً 💔")

keep_alive()
client.run(os.getenv('TOKEN'))
