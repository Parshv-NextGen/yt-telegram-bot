import telebot
from yt_dlp import YoutubeDL
import os
import io
from dotenv import load_dotenv

# Load environment variables from a .env file (for local development)
load_dotenv()

# Get the bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Start and help command
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me a YouTube link to download as MP4 or MP3. Use /mp4 or /mp3 to specify the format.")

# MP4 download command
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
        
        # Open the video file and send it as a stream
        with open("video.mp4", "rb") as video_file:
            video_stream = io.BytesIO(video_file.read())
            bot.send_video(message.chat.id, video_stream)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# MP3 download command
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
        
        # Open the audio file and send it as a stream
        with open("audio.mp3", "rb") as audio_file:
            audio_stream = io.BytesIO(audio_file.read())
            bot.send_audio(message.chat.id, audio_stream)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# Handle invalid input
@bot.message_handler(func=lambda message: True)
def handle_invalid(message):
    bot.reply_to(message, "Invalid input. Use /mp4 or /mp3 to start downloading.")

# Run the bot
bot.infinity_polling()
