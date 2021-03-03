from models import *
import random
import datetime
from app import db
def notNone(x):
    for i in x:
        if i is not None:
            return i
    return None

def check_status(i):
    try:
        x = Sys_Admin.query.filter(Sys_Admin.chat_id == i).first()
        return x.status
    except AttributeError:
        return 1

def check_teacher_status(i):
    try:
        x = Teacher.query.filter(Teacher.chat_id == i).first()
        #print(x.status)
        return x.status
    except AttributeError:
        return 1
def check_pupil_status(i):
    try:
        x = Pupil.query.filter(Pupil.chat_id == i).first()
        return x.status
    except AttributeError:
        return 1

def generate_ticket(all_amount,groups, mode_amount=0, mode=0, date=datetime.datetime.now()):
    q = Question.query.all()
    random.seed(5000)
    list_ticket = []
    index = all_amount
    available_id= [x for x in range(1,all_amount+1)] if all_amount<=len(q) else [x for x in range(1,len(q))]
    string_ids = ''
    while index!= 0:
        index = index - 1
        index_quesion = random.choice(available_id)-1
        available_id.remove(index_quesion+1)
        list_ticket.append(index_quesion-1)
        string_ids+=str(q[index_quesion].id) +'\n'
    t = Ticket(ids=string_ids,date = date,groups=groups)
    db.session.add(t)
    db.session.commit()
    return list_ticket
