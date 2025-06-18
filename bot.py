import yt_dlp
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "မင်္ဂလာပါ! \n\n"
        "သုံးနိုင်တဲ့ command တွေက:\n"
        "/yt <youtube-url> - YouTube Video Download\n"
        "/mp3 <youtube-url> - YouTube MP3 Download\n"
        "/fb <facebook-url> - Facebook Video Download\n"
        "/tt <tiktok-url> - TikTok Video Download\n"
        "/start - ဒီစာကိုပြန်ပေးပါ\n"
    )

# /yt command
async def yt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ YouTube URL ထည့်ပေးပါ။ ဥပမာ: /yt https://youtube.com/...")
        return
    await update.message.reply_text("🚀 YouTube video ကို download လုပ်နေပါပြီ... ခဏစောင့်ပါ...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
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

# /mp3 command
async def mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ YouTube URL ထည့်ပေးပါ။ ဥပမာ: /mp3 https://youtube.com/...")
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
        'quiet': True,
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

# /fb command
async def fb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ Facebook URL ထည့်ပေးပါ။ ဥပမာ: /fb https://facebook.com/...")
        return
    await update.message.reply_text("🚀 Facebook video download လုပ်နေပါပြီ... ခဏစောင့်ပါ...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }
    os.makedirs("downloads", exist_ok=True)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        with open(filename, 'rb') as video_file:
            await update.message.reply_video(video_file, caption=info.get('title', 'Facebook Video'))
        os.remove(filename)
        await update.message.reply_text("✅ Facebook video ပို့ပြီးပါပြီ။")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# /tt command - TikTok video download with yt-dlp
async def tt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ TikTok URL ထည့်ပေးပါ။ ဥပမာ: /tt https://tiktok.com/...")
        return
    await update.message.reply_text("🚀 TikTok video download လုပ်နေပါပြီ... ခဏစောင့်ပါ...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }
    os.makedirs("downloads", exist_ok=True)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        with open(filename, 'rb') as video_file:
            await update.message.reply_video(video_file, caption=info.get('title', 'TikTok Video'))
        os.remove(filename)
        await update.message.reply_text("✅ TikTok video ပို့ပြီးပါပြီ။")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# main bot setup
TOKEN = "7907611450:AAHgD3ebO0Pe8jXgOjY8Np-BKRdW9SKDa5s"
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("yt", YouTube))
app.add_handler(CommandHandler("mp3", mp3))
app.add_handler(CommandHandler("fb", facebook))
app.add_handler(CommandHandler("tt", tikTok))

app.run_polling()
