from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from vms import app,db,login_manager,bcrypt
from vms.user_login.forms import LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from vms.models import Users


# Blueprint object
blue = Blueprint('user_login',__name__,template_folder='templates')

# Login
@blue.route('/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        # check if username and password is correct
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            # check if admin is trying to login
            if user.username == 'admin':
                # if user has checked remember me
                login_user(user,remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('admin.home'))
            else:
                print('USERS LOGIN')
                # if user has checked remember me
                login_user(user,remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('users.home'))
        else:
            flash(f'Invalid username or password','danger')
            return redirect(url_for('user_login.login'))

    return render_template('user_login/login.html',title="Login",form=form)


