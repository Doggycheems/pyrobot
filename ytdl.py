from logging import INFO
from pyrogram import Client, filters
from pytube import YouTube, exceptions
import os
import requests
import logging
import sys
from autologging import logged, traced

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=INFO)
logger = logging.getLogger(__name__)

bot_token = "1521937075:AAFzUp-yZEGpbrRxwlm3BMXFFY15hfV5oIw"  # BOT Token
api_id = 1519291
api_hash = "ff3b1871585d32a794465da51b077361"

app = Client("ytdl", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
with app:
    botname = app.get_me().username


@traced
@logged
@app.on_message(filters.command(["ytdl", f"ytdl@{botname}"], prefixes="/") & ~filters.edited)
def ytdl(client, message):
    text = f"Ciao {str(message.from_user.first_name)}, questo plugin del bot scritto da @doggy_cheems serve a scaricare video da youtube" + \
        "Scrivi /helpyt per sapere come funziono"
    app.send_message(chat_id=message.chat.id, text=text)


@traced
@logged
@app.on_message(filters.command(["helpyt", f"helpyt@{botname}"], prefixes="/") & ~filters.edited)
def help(client, message):
    text = 'Puoi scaricare video e audio usando:\n' + \
        '/video link\n' + \
        '/audio link'
    app.send_message(chat_id=message.chat.id, text=text)


@traced
@logged
@app.on_message(filters.command(["video", f"video@{botname}"], prefixes="/") & ~filters.edited)
def video_dl(client, message):
    chat_id = message.chat.id
    link = message.text.split(maxsplit=1)[1]
    try:
        yt = YouTube(link)
        video = yt.streams.get_highest_resolution().download('res')
        caption = yt.title
        with open('a.jpg', 'wb') as t:
            t.write(requests.get(yt.thumbnail_url).content)
        thumb = open('a.jpg', 'rb')
        app.send_chat_action(chat_id, "upload_video")
        client.send_video(chat_id=chat_id, video=video, caption=caption,
                          thumb=thumb, duration=yt.length)
        if os.path.exists(video):
            os.remove(video)
        if os.path.exists('a.jpg'):
            os.remove('a.jpg')

    except exceptions.RegexMatchError:
        message.reply_text("URL errato.")
    except exceptions.LiveStreamError:
        message.reply_text("Impossibile scaricare live.")
    except exceptions.VideoUnavailable:
        message.reply_text("Video non disponibile.")
    except exceptions.HTMLParseError:
        message.reply_text("Impossibile scaricare il contenuto.")


@traced
@logged
@app.on_message(filters.command(["audio", f"audio@{botname}"], prefixes="/") & ~filters.edited)
def audio_dl(client, message):
    chat_id = message.chat.id
    link = message.text.split('audio', maxsplit=1)[1]
    try:
        yt = YouTube(link)
        audio = yt.streams.get_audio_only().download('res')
        title = yt.title
        app.send_chat_action(chat_id, "upload_audio")
        with open('a.jpg', 'wb') as t:
            t.write(requests.get(yt.thumbnail_url).content)
        thumb = open('a.jpg', 'rb')
        client.send_audio(chat_id=chat_id, audio=audio, title=title,
                          thumb=thumb, performer=yt.author, duration=yt.length)
        if os.path.exists(audio):
            os.remove(audio)
        if os.path.exists('a.jpg'):
            os.remove('a.jpg')

    except exceptions.RegexMatchError:
        message.reply_text("URL errato.")
    except exceptions.LiveStreamError:
        message.reply_text("Impossibile scaricare live.")
    except exceptions.VideoUnavailable:
        message.reply_text("Video non disponibile.")
    except exceptions.HTMLParseError:
        message.reply_text("Impossibile scaricare il contenuto.")


app.run()