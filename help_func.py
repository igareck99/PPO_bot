from models import Teacher,Sys_Admin,Pupil
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
        print(x.status)
        return x.status
    except AttributeError:
        return 1