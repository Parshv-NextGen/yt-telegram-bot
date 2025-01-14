import telebot
from yt_dlp import YoutubeDL
import os

# Get the bot token from Railway environment variables
BOT_TOKEN = os.getenv("7677245007:AAG2y2C-WYCGDuqEj8wvTB5-m5uF4IyzReY")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me a YouTube link to download as MP4 or MP3. Use /mp4 or /mp3 to specify the format.")

@bot.message_handler(commands=['mp4'])
def handle_mp4(message):
    msg = bot.reply_to(message, "Send the YouTube video link to download as MP4.")
    bot.register_next_step_handler(msg, download_mp4)

def download_mp4(message):
    url = message.text
    try:
        bot.reply_to(message, "Downloading MP4. Please wait...")
        with YoutubeDL({'format': 'bestvideo+bestaudio', 'outtmpl': 'video.mp4'}) as ydl:
            ydl.download([url])
        with open("video.mp4", "rb") as video:
            bot.send_video(message.chat.id, video)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

@bot.message_handler(commands=['mp3'])
def handle_mp3(message):
    msg = bot.reply_to(message, "Send the YouTube video link to download as MP3.")
    bot.register_next_step_handler(msg, download_mp3)

def download_mp3(message):
    url = message.text
    try:
        bot.reply_to(message, "Downloading MP3. Please wait...")
        with YoutubeDL({
            'format': 'bestaudio',
            'outtmpl': 'audio.mp3',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }) as ydl:
            ydl.download([url])
        with open("audio.mp3", "rb") as audio:
            bot.send_audio(message.chat.id, audio)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

@bot.message_handler(func=lambda message: True)
def handle_invalid(message):
    bot.reply_to(message, "Invalid input. Use /mp4 or /mp3 to start downloading.")

bot.infinity_polling()
