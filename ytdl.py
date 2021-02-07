  
# -*- coding: utf-8 -*-

import requests, os, validators
import youtube_dl
from pyrogram import Client, filters
from pyrogram.types import  InlineKeyboardMarkup, InlineKeyboardButton

api_id = 1519291 #int of api id get from my.telegram.org
api_hash = "ff3b1871585d32a794465da51b077361" #str of api hash get from my.telegram.org
token = "1521937075:AAFzUp-yZEGpbrRxwlm3BMXFFY15hfV5oIw" #str of token get from BotFather
app = Client("Downlaoder", api_id, api_hash, bot_token=token) # You Can Change The Session Name by Replace "Downlaoder" to your session name


def downloada(url, quality):
    if quality == "1":
        ydl_opts_start = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # need ffmpeg if you don't have ffmpeg, Change it to "best" or install ffmpeg :)
            'outtmpl': f'/data/data/com.termux/files/home/pyrobot/%(id)s.mp4',
            'no_warnings': True,
            'ignoreerrors': True,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True

        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'
    if quality == "2":
        ydl_opts_start = {
            'format': 'best[height=480]',
            'outtmpl': f'/data/data/com.termux/files/home/pyrobot/%(title)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'

# here you can Edit Start message
@app.on_message(filters.command('ytdl', '/'))
def ytdl(c, m): # c Mean Client | m Mean Message
      m.reply_text('Ciao, questo è un plugin scritto da @doggy_cheems\n Manda il link di un video e proverò a scaricarlo') #Edit it and add your Bot ID :)


@app.on_message(filters.regex(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"))
def webpage(c, m): # c Mean Client | m Mean Message
    url1 = m.text
    if validators.url(url1):
        sample_url = "https://da.gd/s?url={}".format(url1)
        url = requests.get(sample_url).text
        chat_id = m.chat.id
        keys = c.send_message(
            chat_id,
            f"Ok\n {url1} è l'URL🥳 \n\nScegli la qualità :\n💡Permi HD per scaricarlo nella miglior qualità possibile",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "HD (Consigliato)",
                            callback_data="%s and 1" % url
                        ),

                    ],
                    [
                        InlineKeyboardButton(
                            "SD (480p)",
                            callback_data="%s and 2" % url
                        ),

                    ]
                ]
            ), disable_web_page_preview=True
        )
    else:
        c.send_message(m.chat.id,"Manda un URL valido")


@app.on_callback_query()
def download(c, q): # c Mean Client | q Mean Query
    global check_current
    check_current = 0
    def progress(current, total): #Thanks to my dear friend Hassan Hoot for Progress Bar :)
        global check_current
        if ((current//1024//1024) % 50 )== 0 :
            if check_current != (current//1024//1024):
                check_current = (current//1024//1024)
                upmsg.edit(f"{current//1024//1024}MB su {total//1024//1024}MB scaricati")
        elif (current//1024//1024) == (total//1024//1024):
            upmsg.delete()
    
    chat_id = q.message.chat.id
    data = q.data
    url, quaitly = data.split(" and ")
    dlmsg = c.send_message(chat_id, 'Sto scaricando...')
    path = downloada(url, quaitly)
    upmsg = c.send_message(chat_id, 'Invio il file...')
    dlmsg.delete()
    thumb = path.replace('.mp4',".jpg",-1)
    if  os.path.isfile(thumb):
        thumb = open(thumb,"rb")
        path = open(path, 'rb')
        c.send_photo(chat_id,thumb,caption='Scaricato tramite @doggycheems_bot') #Edit it and add your Bot ID :)
        c.send_video(chat_id, path, caption='Scaricato tramite @doggycheems_bot',
                    file_name="File", supports_streaming=True, progress=progress) #Edit it and add your Bot ID :)
        upmsg.delete()
    else:
        path = open(path, 'rb')
        c.send_video(chat_id, path, caption='Scaricato tramite @doggycheems_bot',
                    file_name="File", supports_streaming=True, progress=progress)
        upmsg.delete()

app.run()
