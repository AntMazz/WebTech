from stagelopen import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False)



    def __init__(self, email, username, password, role):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
        

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def __repr__(self):
        return f"UserName: {self.username}"



class Interesting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interest =db.Column(db.Text, nullable=False)
    stage_id =db.Column(db.Integer, db.ForeignKey('stage.id'))

    def __init__(self, interest, stage_id):
        self.interest = interest
        self.stage_id = stage_id




class Student(db.Model):

    id = db.Column(db.Integer,primary_key= True)
    naam = db.Column(db.Text)
    achternaam = db.Column(db.Text)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id')) 
    stage = db.relationship('Stage', backref='student', lazy=True)
    
    
    

    def __init__(self,naam, achternaam, user_id):
        self.naam = naam
        self.achternaam = achternaam
        self.user_id = user_id
        
    

    def __repr__(self):
        if self.begeleider:
            return f"Student {self.naam} heeft {self.begeleider.naam} als begeleider."
        else:
            return f"Student {self.naam} heeft nog geen begeleider toegewezen gekregen."


class Instelling(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    naam = db.Column(db.Text)
    soort = db.Column(db.Text)
    stage = db.relationship('Stage', backref='instelling', lazy=True)

    def __init__(self, naam, soort):
        self.naam = naam
        self.soort = soort
    


class Begeleider(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    naam = db.Column(db.Text)
    achternaam = db.Column(db.Text)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id')) 

    
    stage = db.relationship('Stage', backref='begeleider', lazy=True)

    def __init__(self,naam, achternaam, user_id):
        self.naam = naam
        self.achternaam = achternaam
        self.user_id = user_id
    


class Stage(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    instelling_id = db.Column(db.Integer, db.ForeignKey('instelling.id'))
    begeleider_id = db.Column(db.Integer, db.ForeignKey('begeleider.id'))
    cijfer = db.Column(db.Float)
    periode = db.Column(db.String)
    

    
    
    def __init__(self, student_id, instelling_id, begeleider_id, cijfer, periode):
        self.student_id = student_id
        self.instelling_id = instelling_id
        self.begeleider_id = begeleider_id
        self.cijfer = cijfer
        self.periode = periode

    def __repr__(self):
        if self.student:
            return f"Student {self.student_id} loopt stage bij {self.instelling_id} van de opleiding."
        else:
            return f"Student {self.student_id} loopt nog geen stage."

db.create_all()


    






    











