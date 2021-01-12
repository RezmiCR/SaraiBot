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

# Fetching updated data from the responses.json
response_json = open('responses.json', 'rt', encoding='utf-8')
responses_dict = json.load(response_json)
responses_keys = []
for i in responses_dict.keys():
    responses_keys.append(i)
response_json.close()

# Returns a random response from a given type of response eg. 'ascii'
def get_random(given_dict, key):
    try:
        data = given_dict[key]
        resp = []
        for j in data:
            resp.append(j)
        return data[resp[random.randint(0, len(resp) - 1)]]
    except KeyError:
        return 'Key error, contact a dev'

# WIP
def config_call(m_text):
    m_text += ' '
    words = []
    nums = []
    prev = ''
    current = ''
    for ch in m_text:
        if ch != ' ':
            current = current + ch
            prev = ch
        elif prev != ' ' and not prev.isnumeric():
            words.append(current)
            current = ''
        elif prev != ' ' and current.isnumeric():
            nums.append(current)
            current = ''
        else:
            current = ''
    return str(len(words)) + ' words, and ' + str(len(nums)) + ' nums'

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
    bot.send_message(m.chat.id, 'No tengo idea de qué estoy haciendo\nPero pueden probar los siguiente comandos\nwumbojet - Mensaje importante\ncopypasta - Respuesta random\nascii - Ascii robado random')

@bot.message_handler(commands=['wumbojet'])
def wumbojet(m):
    bot.send_message(m.chat.id, '¿alguien dijo algo sobre el mejor jugador de solitario de centroamérica? https://youtu.be/UQRtd-ocw_k')

@bot.message_handler(commands=['copypasta'])
def roast(m):
    bot.send_message(m.chat.id, get_random(responses_dict, 'copypasta'))

@bot.message_handler(commands=['ascii'])
def ascii(m):
    bot.send_message(m.chat.id, get_random(responses_dict, 'ascii'))

@bot.message_handler(commands=['config'])
def config(m):
    bot.send.message(m.chat.id, 'This command isn\'t ready yet\nBut you said: ' + config_call(m.text) )

# @bot.message_handler(content_types=['text'])
# def echo(m):
#    bot.send_message(m.chat.id, m.text)

# @bot.message_handler(content_types=['photo'])
# def photo(m):
#    bot.send_message(m.chat.id, 'Nice duck bro')

print(get_random(responses_dict, 'ascii'))