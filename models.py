from app import db

ROLE_STUDENT = 0
ROLE_TEACHER = 1
ROLE_SYS = 3
ROLE_STUDY = 2
course_pupils = db.Table(
    'group_pupils',
    db.Column('pupil_id', db.Integer(), db.ForeignKey('pupil.id')),
    db.Column('group_id', db.Integer(), db.ForeignKey('group.id'))
)
class Pupil(db.Model):
    __tablename__ = 'pupil'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index = True)
    surname = db.Column(db.String(120), index = True)
    patronim = db.Column(db.String(120), index = True,nullable=True,default = '')
    email = db.Column(db.String(120), index = True)
    phone = db.Column(db.String(120), index = True)
    login = db.Column(db.String(120), index = True,nullable=False)
    password = db.Column(db.String(120), index = True,nullable = False)
    role = db.Column(db.SmallInteger, default = ROLE_STUDENT)
    cats = db.relationship('Group', secondary=course_pupils, backref=db.backref('pupil', lazy='dynamic'))
    pupil_id = db.Column(db.Integer, db.ForeignKey('solution.id'))
    chat_id = db.Column(db.Integer)
    status = db.Column(db.SmallInteger, default=0)
    def __init__(self, name,surname,email,phone,login,password,patronim=''):
        self.name = name
        self.surname = surname
        self.patronim = patronim
        self.email = email
        self.phone = phone
        self.login = login
        self.password = password


    def __repr__(self):
        return 'Pupil {} {} {} '.format(self.name,self.patronim,self.surname)



group_teachers = db.Table(
    'group_teachers',
    db.Column('teacher_id', db.Integer(), db.ForeignKey('teacher.id')),
    db.Column('group_id', db.Integer(), db.ForeignKey('group.id'))
)
class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(120), index=True)
    patronim = db.Column(db.String(120), index=True, nullable=True, default='')
    email = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(120), index=True)
    login = db.Column(db.String(120), index=True, nullable=False)
    password = db.Column(db.String(120), index=True, nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_TEACHER)
    rel = db.relationship('Group', secondary=group_teachers, backref=db.backref('teacher', lazy='dynamic'))
    chat_id = db.Column(db.Integer)
    status = db.Column(db.SmallInteger, default=0)
    def __init__(self,name,surname,email,phone,login,password,patronim=''):
        self.name = name
        self.surname = surname
        self.patronim = patronim
        self.email = email
        self.phone = phone
        self.login = login
        self.password = password

    def __repr__(self):
        return 'Teacher {} {} {}'.format(self.name,self.surname,self.patronim)


class Module(db.Model):
    __tablename__ = 'module'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    hours = db.Column(db.Integer, default=2)
    tasks = db.Column('Question', db.ForeignKey('question.id'))
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f'{self.id} {self.name}'


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), index=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    anwser = db.Column(db.String(100), index=True)
    image = db.Column(db.LargeBinary, nullable=True)
    def __init__(self,text,anwser,module_id): #Доделать
        self.text = text
        self.anwser = anwser
        self.module_id = module_id

    def __repr__(self):
        return f'{self.id} {self.text}'




class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    time = db.Column(db.String(120), index=True)

    def __init__(self,name,time):
        self.name = name
        self.time = time

    def __repr__(self):
        return f'{self.name} {self.time}'



class Solution(db.Model):
    __tablename__ = 'solution'
    id = db.Column(db.Integer, primary_key=True)
    homework_solution = db.Column(db.String(120), index=True)
    ticket = db.Column(db.Integer)
    pupil_id = db.relationship('Pupil', backref='solution',lazy='dynamic')
    mark = db.Column(db.Integer, index=True)
    comment = db.Column(db.String(500), index=True)
    solutions = db.relationship("Pupil")

    def __repr__(self):
        return f'{self.id} {self.pupil}'


class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    ids = db.Column(db.String(200), index=True)

    def __repr__(self):
        return f'{self.id} {self.ids}'


class Sys_Admin(db.Model):
    __tablename__ = 'sys_admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(120), index=True)
    patronim = db.Column(db.String(120), index=True, nullable=True, default='')
    login = db.Column(db.String(120), index=True, nullable=False)
    password = db.Column(db.String(120), index=True, nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_SYS)
    chat_id = db.Column(db.Integer)
    status = db.Column(db.SmallInteger, default=0)
    def __init__(self,name,surname,patronim,login,password):
        self.login = login
        self.password = password
        self.name = name
        self.surname = surname
        self.patronim = patronim

    def __repr__(self):
        return f'{self.id} {self.login}'


class Chat_table(db.Model):
    __tablename__ = 'chat_model'
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)

    def __init__(self,chat_id):
        self.chat_id = chat_id


    def __repr__(self):
        return f'{self.id} {self.chat_id}'