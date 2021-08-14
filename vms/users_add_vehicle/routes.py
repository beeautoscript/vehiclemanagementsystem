from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from vms import app,db,login_manager,bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from vms.users_add_vehicle.forms import RegisterVehicleForm,UpdateVehicleForm,TagVehicleForm
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

# Delete Registered Vehicle
@blue.route('/users/delete/vehicle/<int:uid>',methods=['GET','POST'])
@login_required
def delete_vehicle(uid):
    userid = RegisteredVehicle.query.get_or_404(uid)
    if userid.uservehicleregistered != current_user:
        abort(404)
    db.session.delete(userid)
    db.session.commit()
    flash(f"Vehicle No. {userid.vehiclenum} removed successfully",'success')
    return redirect(url_for('users_add_vehicle.dashboard'))


# Edit Registered Vehicle Data
@blue.route('/update/vehicle/<int:uid>',methods=['GET','POST'])
@login_required
def update_vehicle(uid):
    form = UpdateVehicleForm()
    user_vehicle = RegisteredVehicle.query.get_or_404(uid)
    if form.validate_on_submit():
        user_vehicle.ownername = form.ownername.data
        user_vehicle.routeno = form.routeno.data
        user_vehicle.makemodel = form.makemodel.data
        db.session.commit()
        flash(f"Vehicle No. {user_vehicle.vehiclenum} details updated successfully",'success')
        return redirect(url_for('users_add_vehicle.dashboard'))
        
    return render_template('users_add_vehicle/update_vehicle.html',title="Vehicle Registration",user_vehicle=user_vehicle,form=form)


# Tag Vehicle
@blue.route('/vehicle/tag/<string:vehiclenum>',methods=['POST','GET'])
@login_required
def vehicle_tag(vehiclenum):
    form = TagVehicleForm()
    if form.validate_on_submit():
        user_vehicle = RegisteredVehicle.query.filter_by(user_id=current_user.id,vehiclenum=vehiclenum).first()
        user_vehicle.tagid = form.tagid.data
        db.session.commit()
        flash(f"Vehicle No. {user_vehicle.vehiclenum} tagged successfully",'success')
        return redirect(url_for('users_add_vehicle.dashboard'))

    return render_template('users_add_vehicle/tag.html',title="Vehicle Registration",form=form,vehiclenum=vehiclenum)