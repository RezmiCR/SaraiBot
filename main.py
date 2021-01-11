import telebot
from flask import Flask, request

# Temporally saving some data in a .txt due to laziness
f = open('private.txt', 'rt')
botToken = f.readline()
testBotToken = f.readline()
secret = f.readline()
url = f.readline() + secret
f.close()

token = botToken # swappable between botToken and testBotToken

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

@bot.message_handler(commands=['roast'])
def roast(m):
    bot.send_message(m.chat.id, 'Nigga don’t hate me cause I’m beautiful nigga maybe if you got rid of that Yee Yee Ass hair cut you got you would get bitches on your dick, oh, better yet maybe Tanisha will call your dog ass if she ever stops fucking with that brain Surgeon or Lawyer she fucking with, ♪♪ Niiiggggaaaaaa ♪♪')

# @bot.message_handler(content_types=['text'])
# def echo(m):
#    bot.send_message(m.chat.id, m.text)

# @bot.message_handler(content_types=['photo'])
# def photo(m):
#    bot.send_message(m.chat.id, 'Nice duck bro')