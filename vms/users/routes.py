from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from vms import app,db,login_manager,bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from vms.models import Users,RegisteredVehicle,VehicleOnPremises


# Blueprint object
blue = Blueprint('users',__name__,template_folder='templates')


# User Home
@blue.route('/user/home',methods=['GET','POST'])
@login_required
def home():
    untagged_vehicles = len(RegisteredVehicle.query.filter_by(user_id=current_user.id,tagid=None).all())
    tagged_vehicles = len(RegisteredVehicle.query.filter(RegisteredVehicle.user_id==current_user.id,RegisteredVehicle.tagid != None).all())
    vehicle_inside_premises = len(VehicleOnPremises.query.filter(VehicleOnPremises.on_premise != False).all())
    vehicle_exited_premises = len(VehicleOnPremises.query.filter(VehicleOnPremises.off_premise != False).all())
    return render_template('users/home.html',title='Home',count_untagged=untagged_vehicles,count_tagged=tagged_vehicles,count_vehicle_inside_premises=vehicle_inside_premises,count_vehicle_exit_premises=vehicle_exited_premises)


# User Logout
@blue.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_login.login'))