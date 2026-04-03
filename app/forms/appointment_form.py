from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TimeField, DateField
from wtforms.validators import DataRequired

class AppointmentForm(FlaskForm):
    client_cpf = StringField('CPF do Cliente', validators=[DataRequired()])
    date = DateField('Data', validators=[DataRequired()])
    time = TimeField('Horário', validators=[DataRequired()])

    service = SelectField(
        'Serviço',
        choices=[
            ('massagem', 'Massagem'),
            ('fisioterapia', 'Fisioterapia'),
            ('consulta', 'Consulta')
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField('Agendar')