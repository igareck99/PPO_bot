from flask import Flask,request,jsonify
import requests
from app import app, db
import json
import telebot
import re
from models import *
token = '1628527567:AAFoB0fsz-8QKfkGow8biMztfSDUuYWXSjw'
bot = telebot.TeleBot(token)
from help_func import *
chat_status = {'auth':1,'init':2,'add_group_sys':3}
markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
itembtn1 = telebot.types.KeyboardButton('Добавить Новую группу')
itembtn2 = telebot.types.KeyboardButton('Добавить Студента в группу')
itembtn3 = telebot.types.KeyboardButton('Назначить группу преподавателю')
itembtn4 = telebot.types.KeyboardButton('Зарегистрировать пользователя')
register_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
itembtn5 = telebot.types.KeyboardButton('Учитель')
itembtn6 = telebot.types.KeyboardButton('Ученик')
itembtn7 = telebot.types.KeyboardButton('Админ Системы')
itembtn8 = telebot.types.KeyboardButton('Админ учебного процесса')
markup.row(itembtn1, itembtn2)
markup.row(itembtn3, itembtn4)
register_markup.row(itembtn5,itembtn6)
register_markup.row(itembtn7,itembtn8)
@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200


@bot.message_handler(commands=['start'])
def start(message):
    pupil = Pupil.query.all()
    teacher = Teacher.query.all()
    sys_admin = Sys_Admin.query.all()
    l = []
    for x in pupil:
        l.append(x)
    for x in teacher:
        l.append(x)
    for x in sys_admin:
        l.append(x)
    for x in l:
        if x.chat_id == message.chat.id:
            x.chat_id = message.chat.id
            x.status = 2
            db.session.commit()
            bot.send_message(message.chat.id, 'Здравствуйте,  {} {}'.format(x.name, x.patronim), reply_markup=markup)
            return
    bot.send_message(message.chat.id, 'Здравствуйте! Введите Свои данные в формате логин пароль')
    print(message)

@bot.message_handler(func=lambda message: len(message.text.split()) == 2 and check_status(message.chat.id) ==1)
def auth(message):
    print('Auth message started')
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

@bot.message_handler(func=lambda message: check_status(message.chat.id) == 3)
def add_group(message):
    s = Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()
    s.status = 2
    name = message.text.split(' ')[0]
    time = ' '.join(message.text.split()[1::])
    x = Group(name, time)
    db.session.add(x)
    db.session.commit()
    bot.send_message(message.chat.id, 'Группа была успешно добавлена', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Добавить Студента в группу' and check_status(message.chat.id) == 2)
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

@bot.message_handler(func=lambda message: check_status(message.chat.id)== 4)
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
        x.status = 2
        db.session.commit()
        bot.send_message(message.chat.id, 'Этот ученик уже в этой группе', reply_markup=markup)
        return
    p.cats.append(g)
    db.session.commit()
    x.status = 2
    db.session.commit()
    bot.send_message(message.chat.id, 'Ученик добавлен в группу', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Назначить группу преподавателю' and check_status(message.chat.id) == 2)
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


@bot.message_handler(func=lambda message: check_status(message.chat.id) ==5)
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



@bot.message_handler(func=lambda message: message.text == 'Зарегистрировать пользователя'and check_status(message.chat.id) == 2)
def register_user(message):
    x = Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()
    x.status = 6
    db.session.commit()
    bot.send_message(message.chat.id, 'Выберите кого вы хотите зарегестрировать. ', reply_markup=register_markup)


@bot.message_handler(func=lambda message: message.text == 'Ученик' and check_status(message.chat.id) == 6)
def register_pupil_info(message):
    x = Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()
    x.status = 7
    db.session.commit()
    bot.send_message(message.chat.id, 'Передайте аргументы. Должно быть 6 слов ')


@bot.message_handler(func=lambda message: check_status(message.chat.id) == 7)
def register_pupil(message):
    x = Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()
    m = message.text.split(' ')
    x.status = 2
    db.session.commit()
    if len(m)!=6:
        bot.send_message(message.chat.id, 'Ошибка аргументов. Должно быть 6 слов ', reply_markup=markup)
    else:
        p = Pupil(m[0],m[1],m[2],m[3],m[4],m[5])
        db.session.add(p)
        db.session.commit()
        bot.send_message(message.chat.id, 'Ученик успешно создан ', reply_markup=markup)