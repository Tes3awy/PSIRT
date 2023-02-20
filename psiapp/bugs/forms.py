import re

from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import DataRequired, Length, Regexp


class BugSearchForm(FlaskForm):
    bug_id = StringField(
        label="Cisco Bug ID",
        validators=[
            DataRequired(),
            Length(
                min=9,
                max=10,
                message="Cisco Bug ID is %(min)d to %(max)d characters long!",
            ),
            Regexp(
                regex=r"^CSC\S{2}\d{4,5}$",
                flags=re.IGNORECASE,
                message="Cisco Bug ID uses a pattern of CSCxxNNNN, where x is any letter (a-z) and N is any number (0-9)",
            ),
        ],
        render_kw={"placeholder": "Enter a Cisco Bug ID"},
    )
