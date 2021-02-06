from pyrogram import Client, filters, emoji
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
bot_token = "1521937075:AAFzUp-yZEGpbrRxwlm3BMXFFY15hfV5oIw"  # BOT Token
api_id = 1519291
api_hash = "ff3b1871585d32a794465da51b077361"
app = Client("doggy", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


MENTION = "[{}](tg://user?id={})"  # User mention markup
MESSAGE = "{} Hey, grazie per essere entrato nel gruppo, ti ricrdo di rispettare le regole per non venire punito{}!"  # Welcome message


@app.on_message(filters.new_chat_members)
def welcome(client, message):
    # Build the new members list (with mentions) by using their first_name
    new_members = [u.mention for u in message.new_chat_members]

    # Build the welcome message by using an emoji and the list we built above
    text = MESSAGE.format(emoji.PARTYING_FACE, ", ".join(new_members))

    # Send the welcome message, without the web page preview
    message.reply_text(text, disable_web_page_preview=True)



app.run()