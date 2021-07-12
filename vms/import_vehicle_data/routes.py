from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from vms import app,db,login_manager,bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from vms.import_vehicle_data.forms import ImportDataForm
from vms.models import Users,RegisteredVehicle
from werkzeug.utils import secure_filename
import pandas
import json
import os

# Blueprint object
blue = Blueprint('import_vehicle_data',__name__,template_folder='templates')

# File Upload
UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = {'xlsx'}
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# func check the excel extention
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Import Vehicle Data
@blue.route('/import/data',methods=['GET','POST'])
def import_data():
    form = ImportDataForm()
    if form.validate_on_submit():
        data_file = form.file.data
        # check if file is valid
        if data_file and allowed_file(data_file.filename):
            filename = secure_filename(data_file.filename)
            data_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Read excel document
            excel_data_df = pandas.read_excel('/tmp/'+data_file.filename, sheet_name='Sheet1')
            # Convert to Json
            convert_to_json = excel_data_df.to_json(orient='records')
            # Make Json to List Compatible
            data_dict_list = json.loads(convert_to_json)

            # Add Data to Database
            for i in data_dict_list:
                vehicle = RegisteredVehicle(vehiclenum=i['VehicleNo'],tagid=i['TagId'],ownername=i['OwnerName'],routeno=i['RouteNo'],makemodel=i['MakeModel'],uservehicleregistered=current_user)
                db.session.add(vehicle)
                db.session.commit()

            flash(f"Data from {data_file.filename} saved in database successfully",'success')
            return redirect(url_for('users_add_vehicle.dashboard'))
        else:
            flash(f"Invalid file {data_file.filename}",'danger')
            return redirect(url_for('import_vehicle_data.import_data'))

    return render_template('import_vehicle_data/importdata.html',title='Import Vehicle Data',form=form)