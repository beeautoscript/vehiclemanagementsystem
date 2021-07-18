import json
from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from vms import app,db,login_manager,bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from vms.models import Users,RegisteredVehicle,VehicleOnPremises


# Blueprint object
blue = Blueprint('vms_entry_api',__name__,template_folder='templates')

# Vehicle Entry
@blue.route('/vms/api/v.1.0/entry',methods=['POST'])
def vmsentry():
    data = request.get_json()
    # check if tagid is already available in database
    if len(VehicleOnPremises.query.filter(VehicleOnPremises.tagid == data[0]['tagid']).all()) == 0:
        # new tag vehicle entered premises
        # add new tag entry in database
        new_tag_entry = VehicleOnPremises(tagid=data[0]['tagid'],entrytime=data[0]['timestamp'],on_premise=True,off_premise=False)
        db.session.add(new_tag_entry)
        db.session.commit()
        return json.dumps({'result':'successfully_added_new_tag','status':200})
    else:
        # update entry time of on-premise tagged vehicle
        kwargs = {'tagid':str(data[0]['tagid'])}
        vehicle_table_id = VehicleOnPremises.query.filter_by(**kwargs).first()
        vehicle_table_id.entrytime = str(data[0]['timestamp'])
        vehicle_table_id.on_premise = True
        vehicle_table_id.off_premise = False
        db.session.commit()
        return json.dumps({'result':'successfully_updated_entry_data','status':200})

# Vehicle Exit
@blue.route('/vms/api/v.1.0/exit',methods=['POST'])
def vmsexit():
    data = request.get_json()
    # update exit time and entry-exit boolean
    kwargs = {'tagid':str(data[0]['tagid'])}
    vehicle_table_id = VehicleOnPremises.query.filter_by(**kwargs).first()
    vehicle_table_id.exitime = str(data[0]['timestamp'])
    vehicle_table_id.on_premise = False
    vehicle_table_id.off_premise = True
    db.session.commit()
    return json.dumps({'result':'successfully_updated_exit_data','status':200})


