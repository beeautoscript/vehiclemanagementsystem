from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from vms import app,db,login_manager,bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from vms.models import Users,RegisteredVehicle,VehicleOnPremises
import datetime
import calendar
import json
# from datetime import datetime
# from datetime import timedelta


# Blueprint object
blue = Blueprint('users',__name__,template_folder='templates')

# func count occurence
def occurencex(xlist,xsearch):
    count = 0
    for i in xlist:
        if i == xsearch:
            count = count +1
    return count

# User Home
@blue.route('/user/home',methods=['GET','POST'])
@login_required
def home():
    untagged_vehicles = len(RegisteredVehicle.query.filter_by(user_id=current_user.id,tagid=None).all())
    tagged_vehicles = len(RegisteredVehicle.query.filter(RegisteredVehicle.user_id==current_user.id,RegisteredVehicle.tagid != None).all())
    vehicle_inside_premises = len(VehicleOnPremises.query.filter(VehicleOnPremises.status != False).all())
    vehicle_exited_premises = len(VehicleOnPremises.query.filter(VehicleOnPremises.status != True).all())
    
    # average time of vehicles inside premises
    if len(db.session.query(VehicleOnPremises).filter(VehicleOnPremises.entrytime != None,VehicleOnPremises.exitime != None).all()) == 0:
        average_time = 0
    else:
        average_time_list = []
        total_avergae_time = 0
        query_db = db.session.query(VehicleOnPremises).filter(VehicleOnPremises.entrytime != None,VehicleOnPremises.exitime != None).all()
        for i in query_db:
            exitime = i.exitime
            entrytime = i.entrytime
            exitformat = datetime.datetime.strptime(exitime,'%d-%m-%Y %I:%M:%S %p')
            entryformat = datetime.datetime.strptime(entrytime,'%d-%m-%Y %I:%M:%S %p')
            td = exitformat - entryformat
            average_time_list.append(int(td.total_seconds()))

        for i in average_time_list:
            total_avergae_time += i

        total_seconds = int(total_avergae_time/len(average_time_list))
        average_time_format = datetime.timedelta(seconds=total_seconds)
        average_time=str(average_time_format)

    # Vechile trips in last 5 days
    # sorted list of all the vehicles which have completed trip
    dbq = db.session.query(VehicleOnPremises).filter(VehicleOnPremises.status == False).all()
    trip_list = []
    uniq_list = []
    trip_dict = {}

    if len(dbq) == 0:
        print("Vehicle Trips not available")
        trip_dict = {}
    else:
        for i in dbq:
            trip_list.append(i.exitime.split(' ')[0])
        # sort list
        sorted_list = sorted(trip_list,key=lambda x: datetime.datetime.strptime(x,'%d-%m-%Y'))
        # unique list
        for i in sorted_list:
            if i not in uniq_list:
                uniq_list.append(i)
        # unique list should be = 5
        if len(uniq_list) != 5:
            trip_dict = {}
        else:
            for i in range(0,len(uniq_list)-1):
                trip_dict[uniq_list[i]] = occurencex(trip_list,uniq_list[i])    
    # Last Vehicle Entered
    last_entered_vehicle = VehicleOnPremises.query.filter(VehicleOnPremises.status != False).order_by(VehicleOnPremises.id.desc()).first()
    # Last Vehicle Exited
    last_exited_vehicle = VehicleOnPremises.query.filter(VehicleOnPremises.status != True).order_by(VehicleOnPremises.id.desc()).first()

    return render_template('users/home.html',title='Home',count_untagged=untagged_vehicles,count_tagged=tagged_vehicles,count_vehicle_inside_premises=vehicle_inside_premises,
    count_vehicle_exit_premises=vehicle_exited_premises,average_time=average_time,trip_dict=json.dumps(trip_dict),len_trip=len(trip_dict),last_entered_vehicle=last_entered_vehicle,last_exited_vehicle=last_exited_vehicle)

# Total Vehicle inside premises
@blue.route('/user/onpremises',methods=['GET','POST'])
@login_required
def onpremises():
    page = request.args.get('page',1,type=int)
    vehicle_inside_premises = len(VehicleOnPremises.query.filter(VehicleOnPremises.status != False).all())
    onpremises_vehicle_record = VehicleOnPremises.query.filter_by(status=True).paginate(page=page,per_page=10)
    return render_template('users/onpremises.html',title='Vehicle on premises',count_vehicle_inside_premises=vehicle_inside_premises,onpremises_vehicle_record=onpremises_vehicle_record)

# Total Vehice exited premises
@blue.route('/user/offpremises',methods=['GET','POST'])
@login_required
def offpremises():
    page = request.args.get('page',1,type=int)
    vehicle_outside_premises = len(VehicleOnPremises.query.filter(VehicleOnPremises.status != True).all())
    offpremises_vehicle_record = VehicleOnPremises.query.filter_by(status=False).paginate(page=page,per_page=10)
    return render_template('users/offpremises.html',title='Vehicles exited premises',count_vehicle_outside_premises=vehicle_outside_premises,offpremises_vehicle_record=offpremises_vehicle_record)
# User Logout
@blue.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_login.login'))