import yt_dlp
import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- /start command ---
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

# --- /yt command: YouTube video download ---
async def yt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ YouTube URL တစ်ခုထည့်ပေးပါ။ ဥပမာ: /yt https://youtube.com/...")
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

# --- /mp3 command: YouTube audio (mp3) download ---
async def mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ YouTube URL တစ်ခု ထည့်ပေးပါ။ ဥပမာ: /mp3 https://youtube.com/...")
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

# --- /fb command: Facebook video download using yt_dlp ---
async def fb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text("❌ Facebook URL တစ်ခု ထည့်ပေးပါ။ ဥပမာ: /fb https://facebook.com/...")
        return
    await update.message.reply_text("🚀 Facebook video ကို download လုပ်နေပါပြီ... ခဏစောင့်ပါ...")

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

# --- /tt command: TikTok video download using savetik.co ---
async def tt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❌ TikTok URL တစ်ခု ထည့်ပေးပါ။ ဥပမာ: /tt https://tiktok.com/...")
        return
    url = context.args[0]
    await update.message.reply_text("🚀 TikTok video ကို download လုပ်နေပါပြီ... ခဏစောင့်ပါ...")

    def get_savetik_video_links(tiktok_url):
        session = requests.Session()
        main_url = "https://savetik.co/"

        session.get(main_url)
        post_url = "https://savetik.co/id/ajax/ajax.php"
        data = {'url': tiktok_url}
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; Bot/1.0)',
            'Referer': main_url,
            'X-Requested-With': 'XMLHttpRequest',
        }
        response = session.post(post_url, data=data, headers=headers)
        if response.status_code != 200:
            return None
        json_data = response.json()
        if 'result' not in json_data:
            return None
        html_content = json_data['result']
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http'):
                links.append(href)
        return links

    try:
        links = get_savetik_video_links(url)
        if not links:
            await update.message.reply_text("❌ TikTok video download link ရရှိမရပါ။ URL ကိုစစ်ပါ။")
            return
        for link in links:
            await update.message.reply_text(link)
        await update.message.reply_text("✅ TikTok video download links ပို့ပြီးပါပြီ။")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# --- Main ---
TOKEN = "7907611450:AAHgD3ebO0Pe8jXgOjY8Np-BKRdW9SKDa5s"

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("yt", yt))
app.add_handler(CommandHandler("mp3", mp3))
app.add_handler(CommandHandler("fb", fb))
app.add_handler(CommandHandler("tt", tt))

app.run_polling()
# --- End of bot.py ---