from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from vms import app,db,login_manager,bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from vms.tag_rfid.forms import TagRegisteredVehicleForm
from vms.models import Users,RegisteredVehicle

# Blueprint object
blue = Blueprint('tag_rfid',__name__,template_folder='templates')

# Tag RFID to Registered Vehicles
@blue.route('/tag/rfid',methods=['GET','POST'])
def tag_rfid():
    form = TagRegisteredVehicleForm()
    registered_vehicle_length = len(RegisteredVehicle.query.filter_by(user_id=current_user.id).all())
    untag_vehicle_length = len(RegisteredVehicle.query.filter_by(tagid=None).all())
    if form.validate_on_submit():
        kwargs = {'vehiclenum':str(form.registered_vehicle.data)}
        user_vehicle = RegisteredVehicle.query.filter_by(**kwargs).first()
        user_vehicle.tagid = form.tagid.data
        db.session.commit()
        flash(f"Vehicle No. {user_vehicle.vehiclenum} tagged successfully",'success')
        return redirect(url_for('users_add_vehicle.dashboard'))
    return render_template('tag_rfid/tagrfid.html',title='Tag RFID',form=form,registered_vehicle_length=registered_vehicle_length,untag_vehicle_length=untag_vehicle_length)