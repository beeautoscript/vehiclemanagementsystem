from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from vms.models import Users,RegisteredVehicle


# Upload File Form
class ImportDataForm(FlaskForm):
    file = FileField('Excel Data File',validators=[DataRequired()])
    submit = SubmitField('Import')