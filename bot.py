import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp
from TikTokApi import TikTokApi
import asyncio

TOKEN = "7907611450:AAHgD3ebO0Pe8jXgOjY8Np-BKRdW9SKDa5s"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "မင်္ဂလာပါ! \n\n"
        "သုံးနိုင်တဲ့ command တွေက:\n"
        "/yt <url> - YouTube video download\n"
        "/mp3 <url> - YouTube mp3 download\n"
        "/fb <url> - Facebook video download\n"
        "/tt <url> - TikTok video download\n"
    )

# YouTube video downloader (/yt)
async def yt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ YouTube URL တစ်ခု ထည့်ပေးပါ။ ဥပမာ: /yt https://youtube.com/xxxxxx")
        return

    await update.message.reply_text("🚀 YouTube video download လုပ်နေပါပြီ... ခဏစောင့်ပါ...")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
    }
    os.makedirs("downloads", exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video_file:
            await update.message.reply_video(video_file, caption=info.get('title', 'YouTube Video'))

        os.remove(filename)
        await update.message.reply_text("✅ YouTube video ပို့ပြီးပါပြီ။")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# YouTube mp3 downloader (/mp3)
async def mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ YouTube URL တစ်ခု ထည့်ပေးပါ။ ဥပမာ: /mp3 https://youtube.com/xxxxxx")
        return

    await update.message.reply_text("🚀 mp3 ဖိုင် download လုပ်နေပါပြီ... ခဏစောင့်ပါ...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
    }
    os.makedirs("downloads", exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            filename = filename.rsplit('.', 1)[0] + ".mp3"

        with open(filename, 'rb') as audio_file:
            await update.message.reply_audio(audio_file, title=info.get('title', 'mp3'))

        os.remove(filename)
        await update.message.reply_text("✅ mp3 ဖိုင်ပို့ပြီးပါပြီ။")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# Facebook video downloader (/fb) - Using SaveFrom.net API
import requests

async def fb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ Facebook URL တစ်ခု ထည့်ပေးပါ။ ဥပမာ: /fb https://www.facebook.com/xxxx/video/xxxx")
        return

    await update.message.reply_text("🚀 Facebook video download လုပ်နေပါပြီ... ခဏစောင့်ပါ...")

    api_url = f"https://api.savefrom.net/api/convert?url={url}"
    try:
        # Note: SaveFrom.net official API may not be public or may require paid plan,
        # so this might need alternative APIs or web scraping methods.
        # Here is a placeholder for demonstration.

        # If you have working FB video downloader API, replace this part accordingly.

        await update.message.reply_text("❌ Facebook downloader API မရရှိသေးပါ။")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# TikTok video downloader (/tt)
async def tt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ TikTok URL တစ်ခု ထည့်ပေးပါ။ ဥပမာ: /tt https://www.tiktok.com/@username/video/1234567890")
        return

    await update.message.reply_text("🚀 TikTok video download လုပ်နေပါပြီ... ခဏစောင့်ပါ...")

    try:
        api = TikTokApi()

        video = api.video(url=url)
        video_data = video.bytes()

        os.makedirs("downloads", exist_ok=True)
        file_path = "downloads/tiktok_video.mp4"

        with open(file_path, "wb") as f:
            f.write(video_data)

        with open(file_path, "rb") as video_file:
            await update.message.reply_video(video_file, caption="TikTok Video Downloaded")

        os.remove(file_path)
        await update.message.reply_text("✅ TikTok video ပို့ပြီးပါပြီ။")

    except Exception as e:
        await update.message.reply_text(f"❌ TikTok video download မအောင်မြင်ပါ: {str(e)}")

# Main bot setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("yt", yt))
app.add_handler(CommandHandler("mp3", mp3))
app.add_handler(CommandHandler("fb", fb))
app.add_handler(CommandHandler("tt", tt))

if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
