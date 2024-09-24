from flask import Flask, render_template, redirect, url_for, session, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import ClientForm, AppointmentForm, LoginForm, EmployeeForm
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
'''with app.app_context():
    db.create_all()
'''
# Modelo Client
class Client(db.Model):
    cpf = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)  # Novo campo de email
    address = db.Column(db.String(200), nullable=False)  # Novo campo de endereço
    house_number = db.Column(db.String(20), nullable=False)  # Novo campo de número da casa
    

# Modelo Appointment
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.cpf'), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    client = db.relationship('Client', backref=db.backref('appointments', lazy=True))

# Modelo User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Cria as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Rota inicial para a home
@app.route('/')
def home():
    return render_template('home.html', title='Sistema de Agendamento')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)

    

'''@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')'''

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você saiu com sucesso!', 'success')
    return redirect(url_for('login'))

# Rota de permissões
@app.route('/employees', methods=['GET', 'POST'])
def employees():
    print("Sessão atual:", session)
    if 'user_id' not in session:
        flash('Por favor, faça login primeiro.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('login'))
    if not user.is_admin:
        flash('Acesso não autorizado. Você precisa ser administrador.', 'danger')
        return redirect(url_for('login'))

    print("Usuário logado:", user.username)
    
    form = EmployeeForm()

    if form.validate_on_submit():
            try:
                employee = Employee(username=form.username.data)
                employee.set_password(form.password.data)
                employee.is_admin = form.is_admin.data
                db.session.add(employee)
                db.session.commit()
                flash('Funcionário adicionado com sucesso!', 'success')
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao adicionar funcionário: {e}")
                flash('Erro ao adicionar funcionário.', 'danger')
    
            return redirect(url_for('employees'))

    employees = Employee.query.all()
    return render_template('employees.html', form=form, employees=employees)

@app.route('/create_admin')
def create_admin():
    admin = User(username='admin')
    admin.set_password('admin123')
    admin.is_admin = True
    db.session.add(admin)
    db.session.commit()
    return 'Admin criado com sucesso!'


# Rota para os agendamentos
@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    form = AppointmentForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Pega os dados do formulário e salva o novo agendamento
        client_cpf = form.client_cpf.data
        date = form.date.data
        service = form.service.data
        
        # Verifica se o client é válido
        client = Client.query.get(client_cpf)
        if not client:
            flash('Cliente não encontrado.', 'danger')
            return redirect(url_for('appointments'))

        # Cria e adiciona o agendamento ao banco de dados
        appointment = Appointment(client_id=client_cpf, date=date, service=service)
        db.session.add(appointment)
        db.session.commit()

        return redirect(url_for('appointments'))

    # Lista de agendamentos
    appointments = Appointment.query.all()

    return render_template('appointments.html', form=form, appointments=appointments)

@app.route('/check-client', methods=['POST'])
def check_client():
    client_name = request.json.get('client_name')

    # Procurar cliente no banco de dados
    client = Client.query.filter_by(name=client_name).first()

    if client:
        return jsonify({'exists': True, 'client_id': client.id}), 200
    else:
        return jsonify({'exists': False}), 200

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
                'time': appointment.time,
                'service': appointment.service
            }
            for appointment in appointments
        ]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Excluir agendamento
@app.route('/delete_appointment/<int:appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    try:
        db.session.delete(appointment)
        db.session.commit()
        flash('Agendamento removido com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao remover agendamento: {str(e)}', 'danger')

    return redirect(url_for('appointments'))


# Rota para os clientes
@app.route('/clients', methods=['GET', 'POST'])
def clients():
    form = ClientForm()

    if request.method == 'POST':
        print("Dados enviados:", request.form)  # Verifica o que foi enviado no formulário

    if form.validate_on_submit():
        print("Formulário validado com sucesso")
        new_client = Client(name=form.name.data, contact=form.contact.data, email=form.email.data, address=form.address.data, house_number=form.house_number.data, cpf=form.cpf.data)
        print(f"Novo cliente: {new_client.name}, {new_client.contact}, {new_client.email}, {new_client.address}, {new_client.house_number}, {new_client.cpf}")
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

def format_date(date_str):
    try:
        # Ajuste conforme o formato de data do banco de dados
        date = datetime.strptime(date_str, '%Y-%m-%d')  # Supondo que a data esteja no formato 'YYYY-MM-DD'
        return date.isoformat()  # Converte para o formato ISO 8601
    except ValueError:
        return None

@app.route('/get-events', methods=['GET'])
def get_events():
    start = request.args.get('start')
    end = request.args.get('end')

    if not start or not end:
        return jsonify({'error': 'Datas start e end são necessárias'}), 400

    try:
        # Converter datas de string para datetime
        start_date = datetime.fromisoformat(start)
        end_date = datetime.fromisoformat(end)

        # Filtrar os agendamentos no intervalo de datas
        appointments = Appointment.query.filter(Appointment.date >= start_date, Appointment.date <= end_date).all()

        data = [
            {
                'id': appointment.id,
                'title': f'{appointment.client.name} - {appointment.service}',  # Título do evento
                'start': format_date(appointment.date),  # Formatar data para o formato ISO
                'allDay': True  # Define se o evento é o dia inteiro
            }
            for appointment in appointments
        ]

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
