from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class ClientForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=11)])
    contact = StringField('Contato', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    address = StringField('Endereço', validators=[DataRequired()])
    house_number = StringField('Número da Casa', validators=[DataRequired()])
    submit = SubmitField('Adicionar Cliente')