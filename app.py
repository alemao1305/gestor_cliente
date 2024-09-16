from flask import Flask, render_template, redirect, url_for, session, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from forms import ClientForm, AppointmentForm
from datetime import datetime
import os
'''from models import Client, Appointment'''

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
print(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Importar modelos após a configuração do banco de dados
from models import Client, Appointment

# Cria as tabelas no banco de dados
with app.app_context():
    db.create_all()

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

    if request.method == 'POST' and form.validate_on_submit():
        # Pega os dados do formulário e salva o novo agendamento
        client_id = form.client_id.data
        date = form.date.data
        service = form.service.data
        
        # Cria e adiciona o agendamento ao banco de dados
        appointment = Appointment(client_id=client_id, date=date, service=service)
        db.session.add(appointment)
        db.session.commit()

        return redirect(url_for('appointments'))

    # Lista de agendamentos
    appointments = Appointment.query.all()

    return render_template('appointments.html', form=form, appointments=appointments)

# Rota para json
@app.route('/appointments/json', methods=['GET'])
def appointments_json():
    start = request.args.get('start')
    end = request.args.get('end')

    # Certifique-se de que as datas sejam válidas
    if not start or not end:
        return jsonify({'error': 'Datas start e end são necessárias'}), 400

    try:
        appointments = Appointment.query.filter(Appointment.date >= start, Appointment.date <= end).all()
        data = [
            {
                'id': appointment.id,
                'client': appointment.client.name,
                'date': appointment.date,
                'service': appointment.service
            }
            for appointment in appointments
        ]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota para os clientes
@app.route('/clients', methods=['GET', 'POST'])
def clients():
    form = ClientForm()

    if request.method == 'POST':
        print("Dados enviados:", request.form)  # Verifica o que foi enviado no formulário

    if form.validate_on_submit():
        print("Formulário validado com sucesso")
        new_client = Client(name=form.name.data, contact=form.contact.data)
        print(f"Novo cliente: {new_client.name}, {new_client.contact}")
        try:
            db.session.add(new_client)
            db.session.commit()
            print("Cliente salvo no banco de dados")
            flash('Cliente adicionado com sucesso!', 'success')
            return redirect(url_for('clients'))
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao adicionar cliente: {e}")
            flash(f'Erro ao adicionar cliente: {str(e)}', 'danger')
    else:
        print("Formulário não validado")
        print(form.errors)  # Exibe os erros de validação do formulário

    clients = Client.query.all()  # Carrega todos os clientes
    return render_template('clients.html', form=form, clients=clients)

@app.route('/delete_client/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    try:
        db.session.delete(client)  # Remove o cliente do banco
        db.session.commit()  # Salva as alterações
        flash('Cliente removido com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()  # Faz rollback em caso de erro
        flash(f'Erro ao remover cliente: {str(e)}', 'danger')

    return redirect(url_for('clients'))  # Redireciona para a página de clientes

# Rota para exibir o calendário nativo
@app.route('/calendar')
def calendar():
    appointments = Appointment.query.order_by(Appointment.date).all()
    return render_template('calendar.html', appointments=appointments)

if __name__ == '__main__':
    app.run(debug=True)
