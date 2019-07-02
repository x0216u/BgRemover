from os import remove
import flask
from time import sleep
import telebot
from utilities import *
from local_data import *

# Connect to bot and add proxy
bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook('{}/bot/{}'.format(TOKEN, WEBHOOK_URL))

app = Flask(__name__)
@app.route('/bot/{}'.format(secret), methods=["POST"])
def webhook():
    json_string = request.get_json()
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    resp = flask.jsonify(success=True)
    return resp

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


# Bot run
a
