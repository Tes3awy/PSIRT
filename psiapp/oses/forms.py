from flask_wtf import FlaskForm
from wtforms.fields import SelectField, StringField
from wtforms.validators import DataRequired


class OSVersionSearchForm(FlaskForm):
    os = SelectField(
        label="OS",
        coerce=str,
        validate_choice=True,
        choices=[
            ("", "Select an OS"),
            ("ios", "IOS"),
            ("iosxe", "IOS-XE"),
            ("nxos", "NX-OS"),
            ("aci", "NX-OS in ACI mode"),
            ("asa", "ASA"),
            ("ftd", "FTD"),
            ("fmc", "FMC"),
            ("fxos", "FXOS"),
        ],
        validators=[DataRequired()],
        default=["Select an OS"],
        render_kw={"placeholder": "Select an OS"},
    )
    version = StringField(
        label="Version",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter an OS Version"},
    )
