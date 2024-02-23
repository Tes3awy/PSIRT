from datetime import date, timedelta

from flask_wtf import FlaskForm
from wtforms.fields import DateField, SelectField, SubmitField
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
        render_kw={"placeholder": "First Published"},
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
        default=date.today() - timedelta(days=1),
    )
    search = SubmitField()

    def validate_start_date(self, start_date):
        if start_date.data is None:
            start_date.errors = ["You must set the start date"]
            raise StopValidation()

        if self.end_date.data is None:
            raise StopValidation("You must set end date")

        if start_date.data > self.end_date.data:
            raise ValidationError("End Date must be greater than Start Date")

        if self.end_date.data > date.today():
            raise ValidationError("Cannot get advisories of future dates")
