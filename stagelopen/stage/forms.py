from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired
from stagelopen.models import Student, Instelling, Begeleider



class AddForm(FlaskForm):
    student_id = StringField('Student', validators=[DataRequired()])
    instelling_id = StringField('Instelling', validators=[DataRequired()])
    begeleider_id = StringField('Begeleider', validators=[DataRequired()])
    cijfer = StringField('Cijfer', validators=[DataRequired()])
    periode = StringField('Periode', validators=[DataRequired()])
    submit = SubmitField('Add')
    

    def __init__(self, *args, **kwargs):
        super(AddForm, self).__init__(*args, **kwargs)
        self.student_id.choices = [(student.id, student.voornaam + ' ' + student.achternaam) for student in Student.query.all()]
        self.instelling_id.choices = [(instelling.id, instelling.naam) for instelling in Instelling.query.all()]
        self.begeleider_id.choices = [(begeleider.id, begeleider.voornaam + ' ' + begeleider.achternaam) for begeleider in Begeleider.query.all()]



class UpdateForm(FlaskForm):
    student_id = StringField('Student', validators=[DataRequired()])
    instelling_id = StringField('Instelling', validators=[DataRequired()])
    begeleider_id = StringField('Begeleider', validators=[DataRequired()])
    cijfer = StringField('Cijfer', validators=[DataRequired()])
    periode = StringField('Periode', validators=[DataRequired()])
    submit = SubmitField('Save')


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')


class ApplyForm(FlaskForm):
    interest = TextAreaField("Why are you interested in this stage?", validators=[DataRequired()])
    submit = SubmitField("Apply")
