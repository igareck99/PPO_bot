from flask import Flask,request,jsonify
import requests
from app import app, db
import json
import telebot
import re
from models import *
from help_func import *
token = '1628527567:AAFoB0fsz-8QKfkGow8biMztfSDUuYWXSjw'
bot = telebot.TeleBot(token)
chat_status = {'auth':1,'init':2,'add_group_sys':3}
markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
itembtn1 = telebot.types.KeyboardButton('Добавить Новую группу')
itembtn2 = telebot.types.KeyboardButton('Добавить Студента в группу')
itembtn3 = telebot.types.KeyboardButton('Назначить группу преподавателю')
itembtn4 = telebot.types.KeyboardButton('Зарегестрировать пользователя')
markup.row(itembtn1, itembtn2)
markup.row(itembtn3, itembtn4)
@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Введите Свои данные в формате логин пароль')
    print(message)

@bot.message_handler(func=lambda message: len(message.text.split()) == 2 and Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()==None)
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
    x = notNone([pupil, teacher, sys_admin])
    if x:
        if x.login == login and x.password == password:
            if isinstance(x, Sys_Admin):
                bot.send_message(message.chat.id, 'Здравствуйте,  {} {}'.format(x.name, x.patronim), reply_markup=markup)
                x.chat_id = message.chat.id
                x.status = 2
                db.session.commit()
    else:
        bot.send_message(message.chat.id, 'Неверный пароль, попробуйте ещё раз')
        return


#Действия для Администратора Системы
@bot.message_handler(func=lambda message: message.text == 'Добавить Новую группу')
def add_group_text(message):
    x = Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()
    x.status = 3
    db.session.commit()
    bot.send_message(message.chat.id, 'Введите название группы и время через пробел')

@bot.message_handler(func=lambda message: Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first().status == 3 )
def add_group(message):
    s = Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()
    s.status = 2
    name = message.text.split(' ')[0]
    time = ' '.join(message.text.split()[1::])
    x = Group(name, time)
    db.session.add(x)
    db.session.commit()
    bot.send_message(message.chat.id, 'Группа была успешно добавлена', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Добавить Студента в группу' and Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first().status == 2)
def add_student_to_group_info(message):
    p = Pupil.query.all()
    x = Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()
    g = Group.query.all()
    pupil_string = 'Cписок студентов\n'
    for i in p:
        s = '{} {} {} {}'.format(i.id, i.surname, i.name, i.patronim)
        pupil_string += s + '\n'
    pupil_string += '\n'+'Cписок групп' + '\n'
    for y in g:
        s = '{} {} {}'.format(y.id, y.name, y.time)
        pupil_string += s + '\n'
    pupil_string += 'Введите Id пользователя и id группы через пробел'
    x.status = 4
    db.session.commit()
    bot.send_message(message.chat.id, pupil_string)

@bot.message_handler(func=lambda message: Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first().status == 4)
def add_student_to_group(message):
    x = Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()
    m = message.text.split(' ')
    if len(m) != 2:
        x.status = 2
        db.session.commit()
        bot.send_message(message.chat.id, 'Неправильный ввод', reply_markup=markup)
        return
    p = Pupil.query.filter(Pupil.id == int(m[0])).first()
    g = Group.query.filter(Group.id == int(m[1])).first()
    if notNone([p, g]) is None:
        x.status = 2
        db.session.commit()
        bot.send_message(message.chat.id, 'Неправильный id ученика или группы', reply_markup=markup)
        return
    if g in Pupil.query.filter(Pupil.id == int(m[0])).first().cats:
        print(g)
        x.status = 2
        db.session.commit()
        bot.send_message(message.chat.id, 'Этот ученик уже в этой группе', reply_markup=markup)
        return
    p.cats.append(g)
    db.session.commit()
    x.status = 2
    db.session.commit()
    bot.send_message(message.chat.id, 'Ученик добавлен в группу', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Назначить группу преподавателю' and Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first().status == 2)
def add_teacher_to_group_info(message):
    t = Teacher.query.all()
    x = Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()
    g = Group.query.all()
    teacher_string = 'Cписок Учителей\n'
    for i in t:
        s = '{} {} {} {}'.format(i.id, i.surname, i.name, i.patronim)
        teacher_string += s + '\n'
    teacher_string += '\n'+'Cписок групп' + '\n'
    for y in g:
        s = '{} {} {}'.format(y.id, y.name, y.time)
        teacher_string += s + '\n'
    teacher_string += 'Введите Id пользователя и id группы через пробел'
    x.status = 5
    db.session.commit()
    bot.send_message(message.chat.id, teacher_string)


@bot.message_handler(func=lambda message: Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first().status ==5)
def add_teacher_to_group(message):
    x = Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()
    m = message.text.split(' ')
    if len(m) != 2:
        x.status = 2
        db.session.commit()
        bot.send_message(message.chat.id, 'Неправильный ввод', reply_markup=markup)
        return
    p = Teacher.query.filter(Pupil.id == int(m[0])).first()
    g = Group.query.filter(Group.id == int(m[1])).first()
    if notNone([p, g]) is None:
        x.status = 2
        db.session.commit()
        bot.send_message(message.chat.id, 'Неправильный id учителя или группы', reply_markup=markup)
        return
    if g in Teacher.query.filter(Teacher.id == int(m[0])).first().rel:
        x.status = 2
        db.session.commit()
        bot.send_message(message.chat.id, 'Этот учитель уже в этой группе', reply_markup=markup)
        return
    p.rel.append(g)
    db.session.commit()
    x.status = 2
    db.session.commit()
    bot.send_message(message.chat.id, 'Учитель закреплен за группой', reply_markup=markup)






