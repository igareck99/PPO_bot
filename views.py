from flask import Flask,request,jsonify
import requests
from app import app, db
import json
import telebot
from models import *

token = '1628527567:AAFoB0fsz-8QKfkGow8biMztfSDUuYWXSjw'
bot = telebot.TeleBot(token)
chat_status = {'auth':1}
@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Введите Свои данные в формате логин пароль')
    print(message)

@bot.message_handler(func=lambda message: len(message.text.split()) == 2)
def auth(message):
    m = message.text.split()
    login = m[0]
    password = m[1]
    pupil = Pupil.query.filter(Pupil.login == login) \
        .filter(Pupil.password == password).first()
    teacher = Teacher.query.filter(Teacher.login == login) \
        .filter(Teacher.password == password).first()
    sys_admin = Sys_Admin.query.filter(Sys_Admin.login == login) \
        .filter(Sys_Admin.password == password).first()
    print('ccdcdc',pupil)
    for x in [pupil,teacher,sys_admin]:
        if x is not None:
                if x.login == login and x.password == password:
                    bot.send_message(message.chat.id, 'Здравствуйте {} {}'.format(x.name,x.patronim))
                break
                #появляется доступ к кнопкам
        else:
            bot.send_message(message.chat.id, 'Неверный пароль, попробуйте ещё раз')
            return


def write_json(data, filename='anwser'):
    with open(filename,'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)








