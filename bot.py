from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp
import os

BOT_TOKEN = "7907611450:AAHgD3ebO0Pe8jXgOjY8Np-BKRdW9SKDa5s"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Smart Utility Bot!\n\n"
        "Available Commands:\n"
        "/yt <url>\n"
        "/mp3 <url>\n"
        "/fb <url>\n"
        "/ig <url>\n"
        "/tt <url>\n"
    )

async def youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide YouTube URL.\nExample: /yt https://youtube.com/...")
        return
    url = context.args[0]
    await update.message.reply_text(f"⬇️ Downloading YouTube video...\n{url}")

    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
    }

    os.makedirs('downloads', exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info)

    await update.message.reply_document(document=open(file_name, 'rb'))
    os.remove(file_name)

async def mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide YouTube URL.\nExample: /mp3 https://youtube.com/...")
        return
    url = context.args[0]
    await update.message.reply_text(f"🎵 Downloading MP3...\n{url}")

    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    os.makedirs('downloads', exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

    await update.message.reply_audio(audio=open(file_name, 'rb'))
    os.remove(file_name)

# Placeholders for Facebook, IG, TikTok (Later we can integrate external API)
async def facebook(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📹 Facebook download feature is under development.")

async def instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 Instagram download feature is under development.")

async def tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 TikTok download feature is under development.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('yt', youtube))
    app.add_handler(CommandHandler('mp3', mp3))
    app.add_handler(CommandHandler('fb', facebook))
    app.add_handler(CommandHandler('ig', instagram))
    app.add_handler(CommandHandler('tt', tiktok))

    app.run_polling()
