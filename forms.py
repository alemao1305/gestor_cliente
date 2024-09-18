from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField,  PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email
'''from models import Client  # Importação de modelos no início do arquivo'''

class ClientForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    contact = StringField('Contato', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    address = StringField('Endereço', validators=[DataRequired()])
    house_number = StringField('Numero da Casa', validators=[DataRequired()])
    submit = SubmitField('Adicionar Cliente')

class AppointmentForm(FlaskForm):
    client_id = IntegerField('ID do Cliente', validators=[DataRequired()])
    date = StringField('Data', validators=[DataRequired()])
    service = StringField('Serviço', validators=[DataRequired()])
    submit = SubmitField('Agendar')

    '''def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.update_client_choices()

    def update_client_choices(self):
        """Atualiza as opções do SelectField com a lista de clientes"""
        self.client_id.choices = [(client.id, client.name) for client in Client.query.all()]'''

class LoginForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class EmployeeForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Senha', validators=[DataRequired()])
    is_admin = BooleanField('Admin')
    submit = SubmitField('Adicionar Funcionário')

