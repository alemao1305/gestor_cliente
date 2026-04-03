from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class EmployeeForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Senha', validators=[DataRequired()])
    is_admin = BooleanField('Administrador')
    submit = SubmitField('Adicionar Funcionário')