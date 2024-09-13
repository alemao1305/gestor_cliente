from flask import Flask, render_template, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from forms import ClientForm, AppointmentForm
from datetime import datetime
import os
'''from models import Client, Appointment'''

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Modelo Client
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)

# Modelo Appointment
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    client = db.relationship('Client', backref=db.backref('appointments', lazy=True))

# Cria as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Rota inicial para a home
@app.route('/')
def home():
    return render_template('home.html', title='Sistema de Agendamento')

# Rota para os agendamentos
@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(
            client_id=form.client_id.data,
            date=form.date.data,
            service=form.service.data
        )
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for('appointments'))
    '''form.update_client_choices()'''
    appointments = Appointment.query.all()
    return render_template('appointments.html', form=form, appointments=appointments)

# Rota para os clientes
@app.route('/clients', methods=['GET', 'POST'])
def clients():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(name=form.name.data, contact=form.contact.data)
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('clients'))
    clients = Client.query.all()
    return render_template('clients.html', form=form, clients=clients)

# Rota para exibir o calendário nativo
@app.route('/calendar')
def calendar():
    appointments = Appointment.query.order_by(Appointment.date).all()
    return render_template('calendar.html', appointments=appointments)

if __name__ == '__main__':
    app.run(debug=True)
