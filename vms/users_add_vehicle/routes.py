from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from vms import app,db,login_manager,bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from vms.users_add_vehicle.forms import RegisterVehicleForm
from vms.models import Users,RegisteredVehicle


# Blueprint object
blue = Blueprint('users_add_vehicle',__name__,template_folder='templates')

# Registered Vehicle Dashboard
@blue.route('/users/add_vehicle/dashbaord',methods=['GET','POST'])
@login_required
def dashboard():
    page = request.args.get('page',1,type=int)
    registered_vehicle_length = len(RegisteredVehicle.query.filter_by(user_id=current_user.id).all())
    registered_vehicle_record = RegisteredVehicle.query.filter_by(uservehicleregistered=current_user).paginate(page=page,per_page=10)
    return render_template('users_add_vehicle/dashboard.html',title='Vehicle Registration',registered_vehicle_length=registered_vehicle_length,registered_vehicle_record=registered_vehicle_record)

# Register Vehicle
@blue.route('/users/add_vehicle/register',methods=['GET','POST'])
@login_required
def register_vehicle():
    form = RegisterVehicleForm()
    if form.validate_on_submit():
        vehicle = RegisteredVehicle(vehiclenum=form.vehicleno.data,ownername=form.ownername.data,routeno=form.routeno.data,makemodel=form.makemodel.data,uservehicleregistered=current_user)
        db.session.add(vehicle)
        db.session.commit()
        flash(f"Vehicle No. {form.vehicleno.data} registered successfully",'success')
        return redirect(url_for('users_add_vehicle.dashboard'))
    return render_template('users_add_vehicle/registervehicle.html',title='Vehicle Registration',form=form)