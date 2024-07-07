from flask import Blueprint, render_template, request, url_for, flash, redirect 
from forms import UserLoginForm
from models import User, db, check_password_hash

from flask_login import login_user, logout_user, LoginManager, current_user, login_required


auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods = ['GET','POST'])
def signup():
    form = UserLoginForm()

    try: 
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            user = User(email, password = password)

            db.session.add(user)
            db.session.commit()


            flash(f'You have successfully created a user account {email}', 'User-Created')
            return redirect(url_for('home.profile'))
    except:
        raise Exception('Inavalid form data: Please check your form')
    return render_template('signup.html', form=form)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You are now signed in.', 'auth-sucess')
                return redirect(url_for('home.profile'))
            else:
                flash('You have failed in your attempt to access this content.', 'auth-failed')
                return redirect(url_for('auth.login'))
    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('signin.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))