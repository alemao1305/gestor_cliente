from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Tabela de usuários (para login)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

# Tabela de papéis (permissões)
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)

# Tabela de funcionários
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

# Tabela de clientes
class Client(db.Model):
    cpf = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=False)
    house_number = db.Column(db.String(10), nullable=False)
    

# Tabela de agendamentos
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.cpf'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    time = db.Column(db.Time(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    client = db.relationship('Client', backref=db.backref('appointments', lazy=True))
    employee = db.relationship('Employee', backref='appointments', lazy=True)