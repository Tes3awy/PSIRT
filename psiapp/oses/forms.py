from flask_wtf import FlaskForm
from wtforms.fields import SelectField, StringField
from wtforms.validators import DataRequired

from psiapp.oses.enums import SelectOptions


class OSVersionSearchForm(FlaskForm):
    os = SelectField(
        label="OS",
        coerce=str,
        validate_choice=True,
        choices=[(option.value[0], option.value[1]) for option in SelectOptions],
        validators=[DataRequired()],
        default=["Select an OS type"],
        render_kw={"placeholder": "Select an OS type", "class_": "select"},
    )
    version = StringField(
        label="Version",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter an OS version"},
    )
