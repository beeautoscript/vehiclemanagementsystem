import json
from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from vms import app,db,login_manager,bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from vms.models import Users,RegisteredVehicle,VehicleOnPremises,Entryexitime


# Blueprint object
blue = Blueprint('vms_entry_api',__name__,template_folder='templates')

# Vehicle Entry
@blue.route('/vms/api/v.1.0/entry',methods=['POST'])
def vmsentry():
    data = request.get_json()

    # check if tagid is already available in database : VehicleOnPremises DB
    if len(VehicleOnPremises.query.filter(VehicleOnPremises.tagid == data[0]['epc_id']).all()) == 0:
        # new tag vehicle entered premises
        # add new tag entry in database
        new_tag_entry = VehicleOnPremises(tagid=data[0]['epc_id'],entrytime=data[0]['timestamp'],status=True)
        db.session.add(new_tag_entry)
        db.session.commit()
    else:
        # update entry time of on-premise tagged vehicle
        kwargs = {'tagid':str(data[0]['epc_id'])}
        vehicle_table_id = VehicleOnPremises.query.filter_by(**kwargs).first()
        vehicle_table_id.entrytime = str(data[0]['timestamp'])
        vehicle_table_id.status = True
        db.session.commit()

    # check if tag is registered,if yes then add the entry time : Entryexitime DB
    if len(RegisteredVehicle.query.filter(RegisteredVehicle.tagid == data[0]['epc_id']).all()) != 0:
        kwargs = {'tagid':str(data[0]['epc_id'])}
        registered_vehicle_table_id = RegisteredVehicle.query.filter_by(**kwargs).first()
        #add entry time
        add_entry_time = Entryexitime(entrytime=str(data[0]['timestamp']),registeredvehicle_id=registered_vehicle_table_id.id)
        db.session.add(add_entry_time)
        db.session.commit()
        return json.dumps({'result':'entry_time_entryexit_db','status':200})
    else:
        return json.dumps({'result':'entry_time_vehicleonpremises_db','status':200})



# Vehicle Exit
@blue.route('/vms/api/v.1.0/exit',methods=['POST'])
def vmsexit():
    data = request.get_json()

    # check if tagid is already available in database : VehicleOnPremises DB
    if len(VehicleOnPremises.query.filter(VehicleOnPremises.tagid == data[0]['epc_id']).all()) != 0:
        # update exit time of on-premise tagged vehicle
        kwargs = {'tagid':str(data[0]['epc_id'])}
        vehicle_table_id = VehicleOnPremises.query.filter_by(**kwargs).first()
        vehicle_table_id.exitime = str(data[0]['timestamp'])
        vehicle_table_id.status = False
        db.session.commit()

    # check if tag is registered,if yes then add the entry time : Entryexitime DB
    if len(RegisteredVehicle.query.filter(RegisteredVehicle.tagid == data[0]['epc_id']).all()) != 0:
        kwargs = {'tagid':str(data[0]['epc_id'])}
        registered_vehicle_table_id = RegisteredVehicle.query.filter_by(**kwargs).first()
        #add entry time
        add_entry_time = Entryexitime(exitime=str(data[0]['timestamp']),registeredvehicle_id=registered_vehicle_table_id.id)
        db.session.add(add_entry_time)
        db.session.commit()
        return json.dumps({'result':'entry_time_entryexit_db','status':200})
    else:
        return json.dumps({'result':'entry_time_vehicleonpremises_db','status':200})

