from flask import Flask,request,jsonify
import requests
from app import app, db
import json
import telebot
from datetime import datetime
import re
from models import *
token = '1628527567:AAFoB0fsz-8QKfkGow8biMztfSDUuYWXSjw'
bot = telebot.TeleBot(token)
from help_func import *
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
itembtn9 = telebot.types.KeyboardButton('Вернуться на главную СисАдмина')
itembtn10 = telebot.types.KeyboardButton('Добавить задание')
itembtn11 = telebot.types.KeyboardButton('Список групп')
itembtn12 = telebot.types.KeyboardButton('Результаты тестирования')
itembtn13 = telebot.types.KeyboardButton('Создать Билет для тестирования')
itembtn14 = telebot.types.KeyboardButton('Новый модуль')
itembtn15 = telebot.types.KeyboardButton('Пройти тестирование')
itembtn16 = telebot.types.KeyboardButton('Результаты тестирования')
itembtn17 = telebot.types.KeyboardButton('Назад')
itembtn18 = telebot.types.KeyboardButton('Списки групп преподавателя')
itembtn19 = telebot.types.KeyboardButton('Запланированные тестирования')
itembtn20 = telebot.types.KeyboardButton('Посмотреть задания')
teahcer_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
teahcer_markup.row(itembtn13, itembtn12)
teahcer_markup.row(itembtn11, itembtn10)
teahcer_markup.row(itembtn14)
pupil_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
pupil_test = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
teacher_admin = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
teacher_admin.row(itembtn16,itembtn17)
teacher_admin.row(itembtn18,itembtn19)
teacher_admin.row(itembtn20)
pupil_test.row(itembtn17)
pupil_markup.row(itembtn15)
markup.row(itembtn1, itembtn2)
markup.row(itembtn3, itembtn4)
markup.row(itembtn9)
register_markup.row(itembtn5,itembtn6)
register_markup.row(itembtn7,itembtn8)
register_markup.row(itembtn9)
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
    t_a = Teacher_Admin.query.all()
    l = []
    for x in pupil:
        l.append(x)
    for x in teacher:
        l.append(x)
    for x in sys_admin:
        l.append(x)
    for x in t_a:
        l.append(x)
    for x in l:
        if x.chat_id == message.chat.id:
            x.chat_id = message.chat.id
            x.status = 2
            db.session.commit()
            if isinstance(x, Sys_Admin):
                bot.send_message(message.chat.id, 'Здравствуйте,  {} {}'.format(x.name, x.patronim), reply_markup=markup)
            elif isinstance(x,Teacher):
                x.status = 10
                db.session.commit()
                bot.send_message(message.chat.id, 'Здравствуйте,  {} {}'.format(x.name, x.patronim),
                                 reply_markup=teahcer_markup)
            elif isinstance(x,Pupil):
                x.status = 15
                db.session.commit()
                bot.send_message(message.chat.id, 'Здравствуйте,  {} {}'.format(x.name, x.patronim),
                                 reply_markup=pupil_markup)
            elif isinstance(x,Teacher_Admin):
                x.status = 20
                db.session.commit()
                bot.send_message(message.chat.id, 'Здравствуйте,  {} {}'.format(x.name, x.patronim),
                                 reply_markup=teacher_admin)
            return
    bot.send_message(message.chat.id, 'Здравствуйте! Введите Свои данные в формате логин пароль')
    print(message)

@bot.message_handler(func=lambda message: len(message.text.split()) == 2 and check_status(message.chat.id) ==1 and check_teacher_status(message.chat.id)==1 and check_pupil_status(message.chat.id)==1 and check_ta_status(message.chat.id)==1)
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
    ta_admin = Teacher_Admin.query.filter(Teacher_Admin.login == login) \
        .filter(Teacher_Admin.password == password).first()
    x = notNone([pupil, teacher, sys_admin,ta_admin])
    if x:
        if x.login == login and x.password == password:
            if isinstance(x, Sys_Admin):
                bot.send_message(message.chat.id, 'Здравствуйте,  {} {}'.format(x.name, x.patronim), reply_markup=markup)
                x.chat_id = message.chat.id
                x.status = 2
                db.session.commit()
            elif isinstance(x, Teacher):
                bot.send_message(message.chat.id, 'Здравствуйте,  {} {}'.format(x.name, x.patronim), reply_markup=teahcer_markup)
                x.chat_id = message.chat.id
                x.status = 10
                db.session.commit()
            elif isinstance(x, Pupil):
                bot.send_message(message.chat.id, 'Здравствуйте,  {} {}'.format(x.name, x.patronim), reply_markup=pupil_markup)
                x.chat_id = message.chat.id
                x.status = 15
                db.session.commit()
            elif isinstance(x, Teacher_Admin):
                bot.send_message(message.chat.id, 'Здравствуйте,  {} {}'.format(x.name, x.patronim), reply_markup=teacher_admin)
                x.chat_id = message.chat.id
                x.status = 20
                db.session.commit()
    else:
        bot.send_message(message.chat.id, 'Неверный пароль, попробуйте ещё раз')
        return
@bot.message_handler(func=lambda message: message.text == 'Вернуться на главную СисАдмина' and check_status(message.chat.id) >=2
                     and check_status(message.chat.id)<=9)
def return_sys_admin(message):
    s = Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()
    s.status = 2
    bot.send_message(message.chat.id, 'Вы вернулись на главную', reply_markup=markup)


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
    if len(m)!=7:
        bot.send_message(message.chat.id, 'Ошибка аргументов. Должно быть 7 слов ', reply_markup=markup)
    else:
        p = Pupil(m[0],m[1],m[2],m[3],m[4],m[5])
        db.session.add(p)
        db.session.commit()
        bot.send_message(message.chat.id, 'Ученик успешно создан ', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Учитель' and check_status(message.chat.id) == 6)
def register_pupil_info(message):
    x = Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()
    x.status = 8
    db.session.commit()
    bot.send_message(message.chat.id, 'Передайте аргументы. Должно быть 7 слов ')


@bot.message_handler(func=lambda message: check_status(message.chat.id) == 8)
def register_pupil(message):
    x = Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()
    m = message.text.split(' ')
    x.status = 2
    db.session.commit()
    if len(m)!=7:
        bot.send_message(message.chat.id, 'Ошибка аргументов. Должно быть 7 слов ', reply_markup=markup)
    else:
        p = Teacher(m[0],m[1],m[2],m[3],m[4],m[5],m[6])
        db.session.add(p)
        db.session.commit()
        bot.send_message(message.chat.id, 'Учитель успешно создан ', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Админ Системы' and check_status(message.chat.id) == 6)
def register_sys_info(message):
    x = Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()
    x.status = 9
    db.session.commit()
    bot.send_message(message.chat.id, 'Передайте аргументы. Должно быть 5 слов через пробел')


@bot.message_handler(func=lambda message: check_status(message.chat.id) == 9)
def register_sys(message):
    x = Sys_Admin.query.filter(Sys_Admin.chat_id == message.chat.id).first()
    m = message.text.split(' ')
    x.status = 2
    db.session.commit()
    if len(m)!=5:
        bot.send_message(message.chat.id, 'Ошибка аргументов. Должно быть 5 слов ', reply_markup=markup)
    else:
        p = Sys_Admin(m[0], m[1], m[2], m[3], m[4])
        db.session.add(p)
        db.session.commit()
        bot.send_message(message.chat.id, 'Админитсратор системы  успешно создан ', reply_markup=markup)


# Действия учителя
@bot.message_handler(func=lambda message: message.text == 'Новый модуль' and check_teacher_status(message.chat.id) == 10)
def register_module_info(message):
    x = Teacher.query.filter(Teacher.chat_id == message.chat.id).first()
    x.status = 11
    db.session.commit()
    bot.send_message(message.chat.id, 'Введите Название Модуля')

@bot.message_handler(func=lambda message: check_teacher_status(message.chat.id) == 11)
def register_module(message):
    x = Teacher.query.filter(Teacher.chat_id == message.chat.id).first()
    m = message.text.split(' ')
    x.status = 10
    db.session.commit()
    if len(m)!=1:
        bot.send_message(message.chat.id, 'Ошибка аргументов. Должно быть 1 словo ', reply_markup=teahcer_markup)
    else:
        p = Module(m[0])
        db.session.add(p)
        db.session.commit()
        bot.send_message(message.chat.id, 'Новый модуль успешно создан', reply_markup=teahcer_markup)

@bot.message_handler(func=lambda message: message.text == 'Добавить задание' and check_teacher_status(message.chat.id) == 10)
def register_task_info(message):
    x = Teacher.query.filter(Teacher.chat_id == message.chat.id).first()
    y = Module.query.all()
    s = 'Список Модулей' +'\n'+'\n'
    for i in y:
        s+= '{}  {}'.format(i.id, i.name) + '\n'
    x.status = 12
    db.session.commit()
    result = s+ '\n\n\n' + 'Введите Текст вопроса $ ответ $ id Модуля'
    bot.send_message(message.chat.id, result)

@bot.message_handler(func=lambda message: check_teacher_status(message.chat.id) == 12)
def register_task_info(message):
    x = Teacher.query.filter(Teacher.chat_id == message.chat.id).first()
    x.status = 10
    db.session.commit()
    m = message.text.split('$')
    data = []
    for x in m:
        data.append(x.strip())
    try:
        p = Question(data[0], data[1], int(data[2]))
        db.session.add(p)
        db.session.commit()
        bot.send_message(message.chat.id, 'Вопрос создан', reply_markup=teahcer_markup)
    except:
        bot.send_message(message.chat.id, 'Произошла ошибка', reply_markup=teahcer_markup)

@bot.message_handler(func=lambda message: message.text == 'Список групп' and check_teacher_status(message.chat.id) == 10)
def teacher_list_group(message):
    g = Group.query.all()
    pupil_string = ''
    pupil_string += '\n' + 'Cписок групп' + '\n'
    for y in g:
        s = '{} {} {}'.format(y.id, y.name, y.time)
        pupil_string += s + '\n'
    bot.send_message(message.chat.id, pupil_string, reply_markup=teahcer_markup)

@bot.message_handler(func=lambda message: message.text == 'Создать Билет для тестирования' and check_teacher_status(message.chat.id) == 10)
def ticket_info(message):
    x = Teacher.query.filter(Teacher.chat_id == message.chat.id).first()
    x.status = 13
    db.session.commit()
    bot.send_message(message.chat.id, 'Введите количество вопросов, количество заданий из модуля,количество модулей и дату проведения и id групп в формате $id $id. Дату введите в формате: год-месяц-день час:минуты')

@bot.message_handler(func=lambda message:check_teacher_status(message.chat.id) == 13)
def ticket_add(message):
    x = Teacher.query.filter(Teacher.chat_id == message.chat.id).first()
    x.status = 10
    db.session.commit()
    m = message.text.split(' ')
    print(m)
    if len(m)>=6:
        date_str = m[3]+' '+m[4]
        group_str = ''
        for x in m:
            if '$' in x:
                group_str+=x[1::]
        print('m0 {} m1 {} m2 {} date {} groups{}'.format(m[0],m[1],m[2],date_str,group_str))
        #generate_ticket(all_amount = m[0],date = datetime.datetime.strptime(date_str),groups = group_str)
        bot.send_message(message.chat.id, 'Билет успешно создан', reply_markup=teahcer_markup)

@bot.message_handler(func=lambda message:check_teacher_status(message.chat.id) == 10 and message.text == 'Результаты тестирования')
def res_test_teacher(message):
    s = Solution.query.all()
    r = ''
    l = []
    for x in s:
        p = Pupil.query.filter(Pupil.id==(x.pupil_id)).first()
        if p is not None:
            l.append(p)
    print(l)
    for i, y in zip(s,l):
        r+=y.name+' '+y.surname+'Номер теста: '+str(i.id)+'  Оценка: ' + str(i.mark) +'\n'
    bot.send_message(message.chat.id, r, reply_markup=teahcer_markup)

#Функционал для ученика
@bot.message_handler(func=lambda message: message.text == 'Пройти тестирование' and check_pupil_status(message.chat.id) == 15)
def test_pupil_info(message):
    p = Pupil.query.filter(Pupil.chat_id == message.chat.id).first()
    p.status = 16
    db.session.commit()
    t = Ticket.query.all()
    q = db.session.query(Group).filter_by(id=p.id).all()
    l = []
    for x in t:
        for i in q:
            if str(i.id) in x.groups.split(' '):
                l.append(x.id)
    s = ''
    print(l)
    for x in l:
        z = Ticket.query.filter(Ticket.id == x).first()
        s+=str(z.id) + ' Дата  ' + str(z.date)
    bot.send_message(message.chat.id, 'Вам доступны тесты \n {} \n\nДля прохождения тестирования отправьте номер теста'.format(s),reply_markup=pupil_test)


@bot.message_handler(func=lambda message: message.text == 'Назад' and check_pupil_status(message.chat.id) == 16)
def return_pupil(message):
    p = Pupil.query.filter(Pupil.chat_id == message.chat.id).first()
    p.status = 15
    db.session.commit()
    bot.send_message(message.chat.id,'Выберите действие', reply_markup=pupil_markup)

@bot.message_handler(func=lambda message: check_pupil_status(message.chat.id) == 16)
def start_test(message):
    p = Pupil.query.filter(Pupil.chat_id == message.chat.id).first()
    p.status = 17
    db.session.commit()
    m = message.text
    if len(m)!=1:
        p.status = 15
        db.session.commit()
        bot.send_message(message.chat.id, 'Некорректный ввод', reply_markup=pupil_markup)
    try:
        m = int(m)
    except ValueError:
        p.status = 15
        db.session.commit()
        bot.send_message(message.chat.id, 'Некорректный ввод', reply_markup=pupil_markup)
    print(m)
    t = Ticket.query.filter(Ticket.id == m).first()
    t = t.ids.split(' ')
    l = []
    for x in t:
        if x.isdigit():
            l.append(x)
    l = list(map(int, l))
    s = ''
    for x in l:
        s+=Question.query.filter(Question.id == x).first().text + '\n'

    bot.send_message(message.chat.id, '{}\n\nВведите ответы через $'.format(s))

@bot.message_handler(func=lambda message: check_pupil_status(message.chat.id) == 17)
def check_anwser(message):
    whose_solution = Pupil.query.filter(Pupil.chat_id == message.chat.id).first()
    t = Ticket.query.filter(Ticket.id ==1).first().ids.split(' ')
    mark = 0
    right = 0
    wronng = 0
    amount = len(t)
    m = message.text.split(' ')
    index = list(map(int,t))
    for x in index:
        q = Question.query.filter(Question.id == int(x)).first()
        if m[x-1]==q.anwser:
            right+=1
        else:
            wronng+=1
    whose_solution.status = 15
    mae = add_mark(right/amount)
    e = 'Правильно {} задания \n Неправильно {}'.format(right,wronng)
    s = Solution(message.text, 1, whose_solution.id,mae[-1],e)
    db.session.add(s)
    whose_solution.status = 15
    db.session.commit()
    bot.send_message(message.chat.id, 'Ваша оценка {}\n{}'.format(mae[-1],e), reply_markup=pupil_markup)


#Администратор учебного процесса

@bot.message_handler(func=lambda message: check_ta_status(message.chat.id) == 20 and message.text =='Результаты тестирования')
def check_solution_result(message):
    t = Teacher_Admin.query.filter(Teacher_Admin.chat_id == message.chat.id).first()
    t.status = 20
    db.session.commit()
    s = Solution.query.all()
    r = ''
    l = []
    for x in s:
        p = Pupil.query.filter(Pupil.id==(x.pupil_id)).first()
        if p is not None:
            l.append(p)
    print(l)
    for i, y in zip(s,l):
        r+=y.name+' '+y.surname+'Номер теста: '+str(i.id)+'  Оценка: ' + str(i.mark) +'\n'
    bot.send_message(message.chat.id, r, reply_markup=teacher_admin)

@bot.message_handler(func=lambda message: check_ta_status(message.chat.id) == 20 and message.text =='Списки групп преподавателя')
def check_solution_result(message):
    t = Teacher_Admin.query.filter(Teacher_Admin.chat_id == message.chat.id).first()
    t.status = 21
    db.session.commit()
    l = Teacher_Admin.query.all()
    s = ''
    for x in l:
        s += str(x.id) +'  '+x.name+'  ' +x.patronim + '  '+ x.surname
    bot.send_message(message.chat.id, 'Введите id Преподавателя')

@bot.message_handler(func=lambda message: check_ta_status(message.chat.id) == 21)
def check_solution_result(message):
    m = message.text.split(' ')
    t = Teacher_Admin.query.filter(Teacher_Admin.chat_id == message.chat.id).first()
    t.status = 20
    db.session.commit()
    if len(m)==1:
        try:
            a = int(m)
            taecher = Teacher.query.filter(Teacher.id==a).first()
            p = db.session.query(Teacher).filter_by(id=a).all()
            print(p)
        except ValueError:
            bot.send_message(message.chat.id, 'Некорректный ввод')
    bot.send_message(message.chat.id, '1 IT 22:00 Sunday', reply_markup=teacher_admin)

@bot.message_handler(func=lambda message: check_ta_status(message.chat.id) == 20 and message.text =='Запланированные тестирования')
def planned_tests(message):
    d = datetime.datetime.now()
    s = Ticket.query.filter(Ticket.date>d).all()
    result = ''
    for x in s:
        t = x.groups.split(' ')
        print(t)
        for y in t:
            g = Group.query.filter(Group.id==int(y)).first()
            print()
            result +=str(x.id)+'  '+str(x.date) +' '+g.name +'\n'
    bot.send_message(message.chat.id, result, reply_markup=teacher_admin)

@bot.message_handler(func=lambda message: check_ta_status(message.chat.id) == 20 and message.text =='Посмотреть задания')
def planned_tests(message):
    g = Question.query.all()
    result = ''
    for x in g:
        print(x.module_id)
        mod = Module.query.filter(Module.id == 1).first().name
        result+=str(x.id)+' '+x.text +'Модуль' +mod+'\n'+'Ответ:  '+x.anwser +'\n'
    bot.send_message(message.chat.id, result, reply_markup=teacher_admin)

