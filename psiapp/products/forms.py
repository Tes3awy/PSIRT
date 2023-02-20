from flask_wtf import FlaskForm
from wtforms.fields import SelectField
from wtforms.validators import DataRequired


class ProductSearchForm(FlaskForm):
    product = SelectField(
        coerce=str,
        validate_choice=True,
        validators=[DataRequired()],
        render_kw={"class_": "max-width"},
    )
