from flask import Flask, request
from os import remove
from time import sleep
import telebot
from utilities import *
from local_data import *

# Set proxy
telebot.apihelper.proxy = {
  'https': PROXY
}

# Connect to bot and add proxy
secret = TOKEN
bot = telebot.TeleBot(secret, threaded=False)
bot.remove_webhook()
bot.set_webhook(url="https://25d54f6d.ngrok.io/bot/{}".format(TOKEN))
print(bot.get_me())

app = Flask(__name__)
@app.route('/bot/{}'.format(secret), methods=["POST"])
def webhook():
    print('Server sleep...')
    json_string = request.get_json()
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "ok"

# Helper
@bot.message_handler(commands=['start', 'help'])
def info_message(message):
    bot.send_message(message.chat.id, text='''Hi, this bot can remove background from photos.''')
    sleep(1)

# Get file
@bot.message_handler(content_types=['photo'])
def echo_message(message):
    bot.send_message(message.chat.id, text='Wait...')
    # Download user photo
    fileID = message.photo[-1].file_id
    file = bot.get_file(fileID)
    user_file_path = download_file(file.file_path)

    # Send to BgREmove
    without_bg = remove_bg(user_file_path)
    if without_bg:
        without_bg_file = open(without_bg, 'rb')
        bot.send_photo(message.chat.id, without_bg_file)
        bot.send_document(message.chat.id, without_bg_file)
        remove(without_bg)
        remove(user_file_path)
        sleep(0.5)
    else:
        bot.send_message(message.chat.id, "Can't remove background")
        sleep(0.5)


app.run()
