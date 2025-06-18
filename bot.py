import os
import requests
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7907611450:AAHgD3ebO0Pe8jXgOjY8Np-BKRdW9SKDa5s"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "မင်္ဂလာပါ! \n\n"
        "သုံးနိုင်တဲ့ command တွေက:\n"
        "/yt <youtube-url>\n"
        "/mp3 <youtube-url>\n"
        "/fb <facebook-video-url>\n"
        "/tt <tiktok-video-url>\n"
        "/start\n"
    )

# YouTube video download (video only)
async def yt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ YouTube URL ထည့်ပါ။ ဥပမာ: /yt https://youtube.com/xxxx")
        return

    await update.message.reply_text("🚀 YouTube video download လုပ်နေပါပြီ... ခဏစောင့်ပါ...")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }

    os.makedirs("downloads", exist_ok=True)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, "rb") as video_file:
            await update.message.reply_video(video_file, caption=info.get('title', 'YouTube Video'))

        os.remove(filename)
        await update.message.reply_text("✅ YouTube video ပို့ပြီးပါပြီ။")
    except Exception as e:
        await update.message.reply_text(f"❌ YouTube download မအောင်မြင်ပါ: {str(e)}")

# YouTube mp3 download
async def mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ YouTube URL ထည့်ပါ။ ဥပမာ: /mp3 https://youtube.com/xxxx")
        return

    await update.message.reply_text("🚀 YouTube mp3 download လုပ်နေပါပြီ... ခဏစောင့်ပါ...")

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

        with open(filename, "rb") as audio_file:
            await update.message.reply_audio(audio_file, title=info.get('title', 'YouTube Audio'))

        os.remove(filename)
        await update.message.reply_text("✅ YouTube mp3 ပို့ပြီးပါပြီ။")
    except Exception as e:
        await update.message.reply_text(f"❌ YouTube mp3 download မအောင်မြင်ပါ: {str(e)}")

# Facebook video download (simple downloader with requests)
async def fb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ Facebook video URL ထည့်ပါ။ ဥပမာ: /fb https://www.facebook.com/video_url")
        return

    await update.message.reply_text("🚀 Facebook video download လုပ်နေပါပြီ... ခဏစောင့်ပါ...")

    # Facebook downloader service (example, may break if service changes)
    api_url = "https://api.savevideo.me/api/ajaxSearch"
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    data = {'url': url}

    try:
        response = requests.post(api_url, data=data, headers=headers, timeout=15)
        response.raise_for_status()
        json_data = response.json()

        video_url = None
        for item in json_data.get('data', []):
            if item.get('type') == 'mp4':
                video_url = item.get('url')
                break

        if not video_url:
            await update.message.reply_text("❌ Facebook video URL ရှာမတွေ့ပါ။ URL ကိုစစ်ပါ။")
            return

        os.makedirs("downloads", exist_ok=True)
        file_path = "downloads/facebook_video.mp4"

        video_resp = requests.get(video_url, stream=True, timeout=30)
        video_resp.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in video_resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        with open(file_path, "rb") as video_file:
            await update.message.reply_video(video_file, caption="Facebook Video Downloaded")

        os.remove(file_path)
        await update.message.reply_text("✅ Facebook video ပို့ပြီးပါပြီ။")
    except Exception as e:
        await update.message.reply_text(f"❌ Facebook video download မအောင်မြင်ပါ: {str(e)}")

# TikTok video download via SnapTik API
async def tt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ TikTok URL ထည့်ပါ။ ဥပမာ: /tt https://www.tiktok.com/@username/video/1234567890")
        return

    await update.message.reply_text("🚀 TikTok video download လုပ်နေပါပြီ... ခဏစောင့်ပါ...")

    api_url = "https://api.snaptik.app/aweme/v1/aweme/detail"
    params = {"url": url}

    try:
        response = requests.get(api_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        video_list = data.get("data", {}).get("video_list", [])
        if not video_list:
            await update.message.reply_text("❌ TikTok video data မတွေ့ပါ။ URL ကိုစစ်ပါ။")
            return

        video_url = None
        for video in video_list:
            if video.get("quality_type") == 2 and video.get("url"):
                video_url = video["url"]
                break
        if not video_url:
            video_url = video_list[0].get("url")

        if not video_url:
            await update.message.reply_text("❌ TikTok video URL မရနိုင်ပါ။")
            return

        os.makedirs("downloads", exist_ok=True)
        file_path = "downloads/tiktok_video.mp4"

        video_resp = requests.get(video_url, stream=True, timeout=30)
        video_resp.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in video_resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        with open(file_path, "rb") as video_file:
            await update.message.reply_video(video_file, caption="TikTok Video Downloaded via SnapTik API")

        os.remove(file_path)
        await update.message.reply_text("✅ TikTok video ပို့ပြီးပါပြီ။")

    except Exception as e:
        await update.message.reply_text(f"❌ TikTok video download မအောင်မြင်ပါ: {str(e)}")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("yt", yt))
    app.add_handler(CommandHandler("mp3", mp3))
    app.add_handler(CommandHandler("fb", fb))
    app.add_handler(CommandHandler("tt", tt))
    app.run_polling()
