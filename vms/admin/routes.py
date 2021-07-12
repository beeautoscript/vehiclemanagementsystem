from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from vms import app,db,login_manager,bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from vms.models import Users


# Blueprint object
blue = Blueprint('admin',__name__,template_folder='templates')


# User Home
@blue.route('/admin/home',methods=['GET','POST'])
def user_home():
    return render_template('admin/home.html',title='Home')