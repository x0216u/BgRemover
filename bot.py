from flask import Flask, request
import telebot
from local_data import *

# Set proxy
telebot.apihelper.proxy = {
  'https': PROXY
}

# Connect to bot and add proxy
secret = TOKEN
bot = telebot.TeleBot(secret, threaded=False)
bot.remove_webhook()
bot.set_webhook(url="https://8f09deee.ngrok.io/bot/{}".format(TOKEN))

# Webhook
app = Flask(__name__)
@app.route('/bot/{}'.format(secret), methods=["POST"])
def webhook():
    json_string = request.get_json()
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "ok"

# Helper
@bot.message_handler(commands=['start', 'help'])
def info_message(message):
    bot.send_message(message.chat.id, text='''Hi, this bot can remove background from photos.''')

# Get file
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    print('get message')
    bot.send_message(message.chat.id, text='Салам, ну ты кросс, смог оживить меня, го за работу быстро')

# Run server
app.run()
