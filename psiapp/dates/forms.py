from datetime import date

from flask_wtf import FlaskForm
from wtforms.fields import DateField, SelectField
from wtforms.validators import DataRequired, StopValidation, ValidationError


class DateRangeSearchForm(FlaskForm):
    date_sort = SelectField(
        label="Published by",
        coerce=str,
        validate_choice=True,
        choices=[
            ("firstpublished", "First Published"),
            ("lastpublished", "Last Published"),
        ],
        validators=[DataRequired()],
        default=["firstpublished"],
        render_kw={"placeholder": "First Published", "class_": "focus"},
    )
    start_date = DateField(
        label="Start Date",
        validators=[DataRequired()],
        render_kw={"placeholder": "Start Date", "min": date(1999, 9, 1)},
        format="%Y-%m-%d",
    )
    end_date = DateField(
        label="End Date",
        validators=[DataRequired()],
        render_kw={"placeholder": "End Date"},
        format="%Y-%m-%d",
    )

    def validate_end_date(self, end_date):
        if self.start_date.data is None:
            self.start_date.errors = ["You must set start date"]
            raise StopValidation()

        if end_date.data is None:
            raise StopValidation("You must set end date")

        if self.start_date.data > end_date.data:
            raise ValidationError("End Date must be greater than Start Date")

        if end_date.data > date.today():
            raise ValidationError("Cannot get advisories of future dates")
