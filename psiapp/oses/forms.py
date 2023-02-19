"""Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
            https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from random import choices

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
