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

import re

from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import DataRequired, Length, Regexp


class CVESearchForm(FlaskForm):
    cve_id = StringField(
        label="CVE ID",
        validators=[
            DataRequired(),
            Length(
                min=13,
                max=15,
                message="A CVE ID is %(min)d to %(max)d characters long!",
            ),
            Regexp(
                regex=r"^CVE-\d{4}-\d{3,5}$",
                flags=re.IGNORECASE,
                message="A CVE ID must be in the format of CVE-YYYY-NNNN where N is an integer!",
            ),
        ],
        render_kw={"placeholder": "Enter a CVE ID"},
    )
