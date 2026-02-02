from pyrogram import Client, filters
import yt_dlp
import os
import google.generativeai as genai
from database import *

# إعدادات المحرك
API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-pro')

app = Client("OmniBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
setup_db()

@app.on_message(filters.regex(r"(https?://\S+)"))
async def downloader(client, message):
    url = message.text
    if any(site in url for site in ["tiktok.com", "instagram.com"]):
        msg = await message.reply("⏳ جاري المعالجة...")
        ydl_opts = {'outtmpl': 'video.mp4', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        await message.reply_video("video.mp4")
        os.remove("video.mp4")
        await msg.delete()

@app.on_message(filters.command("اضف_رد") & filters.group)
async def add_rep(client, message):
    if get_rank(message.from_user.id) >= 1:
        parts = message.text.split(" ", 2)
        if len(parts) > 2:
            add_response(parts[1], parts[2])
            await message.reply(f"✅ تم إضافة الرد: {parts[1]}")

@app.on_message(filters.command("الاحصائيات") & filters.user(12345678)) # استبدل بالرقم التعريفي الخاص بك
async def stats(client, message):
    c.execute('SELECT COUNT(*) FROM responses')
    res_count = c.fetchone()[0]
    status_msg = (
        "📊 **لوحة تحكم المعماري**\n"
        "--- --- --- --- ---\n"
        f"🤖 حالة البوت: متصل\n"
        f"💾 الردود المحفوظة: {res_count}\n"
    )
    await message.reply(status_msg)

@app.on_message(filters.mentioned | filters.reply)
async def ai_chat(client, message):
    await client.send_chat_action(message.chat.id, "typing")
    response = model.generate_content(message.text)
    await message.reply(response.text)

app.run()
