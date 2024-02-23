import re

from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
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
                regex=r"^.*$",
                flags=re.IGNORECASE,
                message="Cisco Bug ID uses a pattern of CSCxxNNNN, where xx are any two letter (a-z) and NNNN are any four numbers (0-9)",
            ),
        ],
        render_kw={"placeholder": "Enter a Cisco Bug ID"},
    )
    search = SubmitField()
