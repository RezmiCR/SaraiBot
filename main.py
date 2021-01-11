import telebot
from flask import Flask, request
import json
import random

# Fetching token and server url from a json file
private_json = open('private.json', 'rt', encoding='utf-8')
private_dict = json.load(private_json)
private_json.close()
token = private_dict['test-token']
secret = private_dict['secret']
url = private_dict['url'] + secret

# Fetching updated responses from the responses.json
response_json = open('responses.json', 'rt', encoding='utf-8')
responses_dict = json.load(response_json)
response_json.close()

# Temporary solution for calling random value from json
copypasta_responses = ['lamar','gg']

bot = telebot.TeleBot(token, threaded=False)
bot.remove_webhook()
bot.set_webhook(url = url)

app = Flask(__name__)
@app.route('/'+secret, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, 'Buenas')

@bot.message_handler(commands=['ayuda'])
def help(m):
    bot.send_message(m.chat.id, 'No tengo idea de que estoy haciendo')

@bot.message_handler(commands=['wumbojet'])
def wumbojet(m):
    bot.send_message(m.chat.id, '¿alguien dijo algo sobre el mejor jugador de solitario de centroamérica? https://youtu.be/UQRtd-ocw_k')

@bot.message_handler(commands=['copypasta'])
def roast(m):
    bot.send_message(m.chat.id, responses_dict['copypasta'][copypasta_responses[random.randint(0,1)]])

# @bot.message_handler(content_types=['text'])
# def echo(m):
#    bot.send_message(m.chat.id, m.text)

# @bot.message_handler(content_types=['photo'])
# def photo(m):
#    bot.send_message(m.chat.id, 'Nice duck bro')