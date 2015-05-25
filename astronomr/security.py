###########
# Deal with authentication and authorization

from astronomr import app
from astronomr import login_manager
from fask.ext.login import login_user, UserMixin
import astronomr.model.User
from flask.ext.wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import Email

######

class User(UserMixin):

    def __init__(self, _user):
        self._user = _user

    


######


@login_manager.user_loader
def load_user(id):
    db_user = astronomr.model.User.query.get(id)
    if db_user is None:
        return None
    return User(db_user)


######

class LoginForm(Form):

    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password')


######


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        if not next_is_valid(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)
    
    
