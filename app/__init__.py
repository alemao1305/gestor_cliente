from flask import Flask

from app.extensions import db
from app.routes.main_routes import main_bp



def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importar e registrar rotas
    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.client_routes import client_bp
    from app.routes.appointment_routes import appointment_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app