from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from vms import app,db,login_manager,bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from vms.models import Users,RegisteredVehicle,VehicleOnPremises
import datetime
from datetime import timedelta
from datetime import datetime

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
    
    # average time of vehicles inside premises
    if vehicle_inside_premises == 0:
        average_time = 0
    else:
        total_vehicle_on_premises_query = VehicleOnPremises.query.all()
        total_time_inside_premises_list = [ i.entrytime.split(' ')[1] for i in  total_vehicle_on_premises_query]
        average_time = str(timedelta(seconds=sum(map(lambda f: int(f[0])*3600 + int(f[1])*60 + int(f[2]),map(lambda f: f.split(':'),total_time_inside_premises_list)))/len(total_time_inside_premises_list)))
        # average_time_split = average_time.split(':')
        # average_time_in_minutes = int(average_time_split[0])*60 + int(average_time_split[1])*1 + int(average_time_split[2])/60
        # hours = int(average_time_in_minutes)
        # minutes = (average_time_in_minutes*60) % 60
        # seconds = (average_time_in_minutes*3600) % 60
        # avrerage_time = ("%d:%02d.%02d" % (hours, minutes, seconds))

    return render_template('users/home.html',title='Home',count_untagged=untagged_vehicles,count_tagged=tagged_vehicles,count_vehicle_inside_premises=vehicle_inside_premises,count_vehicle_exit_premises=vehicle_exited_premises,average_time=average_time)


# User Logout
@blue.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_login.login'))