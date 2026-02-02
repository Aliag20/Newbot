from pyrogram import Client, filters
import yt_dlp
import os
from database import *

# إعدادات الاتصال
API_ID = "8086158965"
API_HASH = "8086158965"
BOT_TOKEN = "8336468616:AAGcoSiyD1coEDRkDt1RPS77g_TwaMzd8bU"

app = Client("OmniBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
setup_db()

# --- ميزة التنزيل ---
@app.on_message(filters.regex(r"(https?://\S+)"))
async def downloader(client, message):
    url = message.text
    if "tiktok.com" in url or "instagram.com" in url:
        msg = await message.reply("⏳ جاري المعالجة...")
        ydl_opts = {'outtmpl': 'video.mp4', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        await message.reply_video("video.mp4")
        os.remove("video.mp4")
        await msg.delete()

# --- ميزة الردود التلقائية ---
@app.on_message(filters.command("اضف_رد") & filters.group)
async def add_rep(client, message):
    if get_rank(message.from_user.id) >= 1: # آدمن أو مطور
        parts = message.text.split(" ", 2)
        add_response(parts[1], parts[2])
        await message.reply(f"✅ تم إضافة الرد: {parts[1]}")

# --- ميزة رفع الرتب ---
@app.on_message(filters.command("رفع_مطور") & filters.user("YOUR_SUDO_ID"))
async def promote(client, message):
    target = message.reply_to_message.from_user.id
    set_rank(target, 2)
    await message.reply("🔥 تم رفعه إلى رتبة مطور")
from ai_engine import get_ai_response

# سيستجيب البوت عند منشنته أو الرد عليه
@app.on_message(filters.mentioned | filters.reply)
async def ai_chat(client, message):
    user_input = message.text
    # إرسال حالة "يتم الكتابة" لإعطاء طابع احترافي
    await client.send_chat_action(message.chat.id, "typing")
    ai_text = await get_ai_response(user_input)
    await message.reply(ai_text)
    @app.on_message(filters.command("الاحصائيات") & filters.user("YOUR_SUDO_ID"))
async def stats(client, message):
    # حساب عدد الردود المسجلة
    c.execute('SELECT COUNT(*) FROM responses')
    res_count = c.fetchone()[0]
    
    status_msg = (
        "📊 **لوحة تحكم المعماري (2099)**\n"
        "--- --- --- --- ---\n"
        f"🤖 حالة البوت: متصل (Online)\n"
        f"🧠 محرك AI: يعمل (Gemini-Pro)\n"
        f"💾 الردود المحفوظة: {res_count}\n"
        "🌐 الاستضافة: Railway Cloud\n"
        "--- --- --- --- ---"
    )
    await message.reply(status_msg)
    
app.run()
