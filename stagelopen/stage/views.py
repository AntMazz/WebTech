from flask import render_template,url_for,flash, redirect,request,Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from stagelopen import db
from stagelopen.models import Stage, Interesting
from functools import wraps
from flask import abort
from stagelopen.stage.forms import AddForm, UpdateForm, DeleteForm, ApplyForm





def roles_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('users.login'))
            if current_user.role not in roles:
                return abort(404)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

stage = Blueprint('stage', __name__)

@stage.route('/begeleider')
@roles_required('begeleider')
def begeleider_route():
    return render_template('begeleider.html')


@stage.route('/add_stage', methods=['GET', 'POST'])
@roles_required('begeleider')
def add_stage():
    form = AddForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        instelling_id = form.instelling_id.data
        begeleider_id = form.begeleider_id.data
        cijfer = form.cijfer.data
        periode = form.periode.data
        new_stage = Stage(student_id=student_id, instelling_id=instelling_id, begeleider_id=begeleider_id, cijfer=cijfer, periode=periode)
        print(new_stage)
        db.session.add(new_stage)
        db.session.commit()
        flash('Stage added successfully')
        return redirect(url_for('users.dashboard'))

    return render_template('add_stage.html', form=form)



@stage.route('/edit_stage/<int:stage_id>', methods=['GET', 'POST'])
@roles_required('begeleider')
def edit_stage(stage_id):
    stage = Stage.query.get(stage_id)
    if not stage:
        return redirect(url_for('begeleider_route'))
    form = UpdateForm()
    if form.validate_on_submit():
        stage.student_id = form.student_id.data
        stage.instelling_id = form.instelling_id.data
        stage.begeleider_id = form.begeleider_id.data
        stage.cijfer = form.cijfer.data
        stage.periode = form.periode.data
        db.session.commit()
        return redirect(url_for('users.dashboard'))
    form.student_id.data = stage.student_id
    form.instelling_id.data = stage.instelling_id
    form.begeleider_id.data = stage.begeleider_id
    form.cijfer.data = stage.cijfer
    form.periode.data = stage.periode
    return render_template('edit_stage.html', form=form, stage=stage)



@stage.route('/delete_stage/<int:stage_id>', methods=['GET', 'POST'])
@roles_required('begeleider')
def delete_stage(stage_id):
    form = DeleteForm()
    if form.validate_on_submit():
        stage = Stage.query.get(stage_id)
        db.session.delete(stage)
        db.session.commit()
        return redirect(url_for('users.dashboard'))
    return render_template('delete_stage.html', form=form)



@stage.route('/apply', methods=["GET", "POST"])
def apply():
    form = ApplyForm()
    if form.validate_on_submit():
         interests = Interesting(interest=form.interest.data, stage_id='stage.id' )
         db.session.add(interests)
         db.session.commit()
         return redirect(url_for('stage.succes'))
    return render_template('list.html',form=form)


@stage.route('/success')
@roles_required('begeleider')
def success():
    interested = Interesting.query.all()
    return render_template('apply.html',interested=interested)
    

@stage.route('/succes')
def succes():
    return "Bedankt voor uw sollicitatie"

@stage.route('/stage-aanbod',methods=['GET','POST'])
def create_post():
    return render_template('create_post.html')


@stage.route('/contacts')

def contacts():
    return render_template('contacts.html')
    




