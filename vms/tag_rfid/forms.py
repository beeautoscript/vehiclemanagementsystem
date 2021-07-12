from flask_wtf import FlaskForm
from sqlalchemy.orm import query
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from vms.models import Users,RegisteredVehicle


# func: query all the  registerd vehicle which are not tagged
def query_untag_vehicle():
    return RegisteredVehicle.query.filter_by(tagid=None)

# Tag Untaged Vehicle
class TagRegisteredVehicleForm(FlaskForm):
    tagid = StringField('Tag Id',validators=[DataRequired()])
    registered_vehicle = QuerySelectField(query_factory=query_untag_vehicle,allow_blank=False)
    submit = SubmitField('Tag')

    # check if tag id is already assigned
    def validate_tagid(self,tagid):
        tag = RegisteredVehicle.query.filter_by(tagid=tagid.data).first()
        if tag:
            raise ValidationError('RFID Tag is already assigned')