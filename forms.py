from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
'''from models import Client  # Importação de modelos no início do arquivo'''

class ClientForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    contact = StringField('Contato', validators=[DataRequired()])
    submit = SubmitField('Adicionar Cliente')

class AppointmentForm(FlaskForm):
    client_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    date = StringField('Data', validators=[DataRequired()])
    service = StringField('Serviço', validators=[DataRequired()])
    submit = SubmitField('Agendar')

    '''def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.update_client_choices()

    def update_client_choices(self):
        """Atualiza as opções do SelectField com a lista de clientes"""
        self.client_id.choices = [(client.id, client.name) for client in Client.query.all()]'''