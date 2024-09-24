from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField,  PasswordField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, D

class ClientForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=11)])  # Campo CPF
    contact = StringField('Contato', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    address = StringField('Endereço', validators=[DataRequired()])
    house_number = StringField('Numero da Casa', validators=[DataRequired()])
    submit = SubmitField('Adicionar Cliente')

class AppointmentForm(FlaskForm):
    client_cpf = StringField('CPF do Cliente', validators=[DataRequired()])
    date = StringField('Data', validators=[DataRequired()])
    time = DateTimeField('Time', validators=[DataRequired()])
    service = StringField('Serviço', validators=[DataRequired()])
    submit = SubmitField('Agendar')

class LoginForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class EmployeeForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Senha', validators=[DataRequired()])
    is_admin = BooleanField('Admin')
    submit = SubmitField('Adicionar Funcionário')

