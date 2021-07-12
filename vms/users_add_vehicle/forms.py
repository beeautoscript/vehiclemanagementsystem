from flask_wtf import FlaskForm
from sqlalchemy.orm import query
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from vms.models import Users,RegisteredVehicle



# Register Vehicle
class RegisterVehicleForm(FlaskForm):
    vehicleno = StringField('Vehicle No.',validators=[DataRequired()])
    ownername = StringField('Owner Name',validators=[DataRequired()])
    routeno = StringField('Route No.',validators=[DataRequired()])
    makemodel = StringField('Make/Model',validators=[DataRequired()])
    submit = SubmitField('Register Vehicle')

    # check if vehicle no. is already registered
    def validate_vehicleno(self, vehicleno):
        vehicle = RegisteredVehicle.query.filter_by(vehiclenum=vehicleno.data).first()
        if vehicle:
            raise ValidationError(f'Vehicle number {vehicleno.data} is already registered')
