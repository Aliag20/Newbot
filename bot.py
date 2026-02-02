import os
from pyrogram import Client, filters
import yt_dlp
import google.generativeai as genai
from database import *

# قراءة البيانات من بيئة التشغيل (Railway Variables)
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
AI_KEY = os.environ.get("GEMINI_API_KEY")

# التحقق من وجود البيانات لتجنب انهيار النظام
if not all([API_ID, API_HASH, BOT_TOKEN]):
    print("❌ خطأ: لم يتم العثور على المتغيرات في Railway Variables!")
    exit()

# إعداد المحرك
genai.configure(api_key=AI_KEY)
model = genai.GenerativeModel('gemini-pro')

app = Client("OmniBot", api_id=int(API_ID), api_hash=API_HASH, bot_token=BOT_TOKEN)
setup_db()

@app.on_message(filters.regex(r"(https?://\S+)"))
async def downloader(client, message):
    url = message.text
    if any(site in url for site in ["tiktok.com", "instagram.com"]):
        msg = await message.reply("⏳ جاري المعالجة...")
        ydl_opts = {'outtmpl': 'video.mp4', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if os.path.exists("video.mp4"):
            await message.reply_video("video.mp4")
            os.remove("video.mp4")
        await msg.delete()

@app.on_message(filters.command("الاحصائيات"))
async def stats(client, message):
    c.execute('SELECT COUNT(*) FROM responses')
    res_count = c.fetchone()[0]
    await message.reply(f"📊 حالة البوت: متصل\n💾 الردود: {res_count}")

@app.on_message(filters.mentioned | filters.reply)
async def ai_chat(client, message):
    try:
        await client.send_chat_action(message.chat.id, "typing")
        response = model.generate_content(message.text)
        await message.reply(response.text)
    except:
        await message.reply("⚠️ محرك AI يحتاج لمفتاح API صحيح.")

app.run()
