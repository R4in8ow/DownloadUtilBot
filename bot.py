import yt_dlp
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "မင်္ဂလာပါ! \n\n"
        "သုံးနိုင်တဲ့ command တွေက:\n"
        "/mp3 <youtube-url> \n"
        "/start \n"
    )

# MP3 download command
async def mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ YouTube URL တစ်ခု ထည့်ပေးပါ။ ဥပမာ: /mp3 https://youtube.com/xxxxxx")
        return

    await update.message.reply_text("🚀 mp3 ဖိုင်ကို download လုပ်နေပါပြီ... ခဏစောင့်ပါ...")

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

        # Send audio file
        with open(filename, 'rb') as audio_file:
            await update.message.reply_audio(audio_file, title=info.get('title', 'mp3'))

        await update.message.reply_text("✅ mp3 ဖိုင်ပို့ပြီးပါပြီ။")

        # Optional: Clean up downloaded file
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# Setup the bot
TOKEN = "7907611450:AAHgD3ebO0Pe8jXgOjY8Np-BKRdW9SKDa5s"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("mp3", mp3))

app.run_polling()
