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
                message="A CVE ID must be in the format of CVE-YYYY-NNNN!",
            ),
        ],
        render_kw={"placeholder": "Enter a CVE ID"},
    )
