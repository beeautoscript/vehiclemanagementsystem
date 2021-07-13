from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from vms import app,db,login_manager,bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from vms.models import Users,RegisteredVehicle


# Blueprint object
blue = Blueprint('users',__name__,template_folder='templates')


# User Home
@blue.route('/user/home',methods=['GET','POST'])
def home():
    
    return render_template('users/home.html',title='Home')


# User Logout
@blue.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_login.login'))