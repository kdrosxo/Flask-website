from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash #encrypt passwords,hash function is a one way function
from website.models import User #blueprint of some routes defined
from . import db 
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint('auth', __name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully!',category = 'success')
                login_user(user,remember = True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password,try again',category='error')
        else:
            flash ('Email does not exist',category = 'error')
    return render_template("login.html",user = current_user)

@auth.route ('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        passsword1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()

        if user:
            flash('Email already exists',category = 'error')
        elif len(email) <= 4 :
            flash('Email must be greater than 4 characters',category = 'error')
        elif len(firstName) <=2 :
            flash('First name must be greater than 2 characters',category = 'error')
        elif password1 !=password2:
            flash('Passwords dont match',category = 'error')
        elif len(passsword1) < 7:
            flash('Password must be greater than 6 characters',category = 'error')
        else:
            new_user = User(email=email,firstName = firstName,password = generate_password_hash(passsword1,method = 'sha256') )
            db.session.add(new_user)
            db.session.commit()
            login_user(user,remember=True)
            flash('Your account has been created',category = 'success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html",user = current_user)
