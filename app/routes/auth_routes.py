from flask import Blueprint, render_template, redirect, url_for, session, flash
from app.models.user import User
from app import db
from app.forms.auth_form import LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            session['user_id'] = user.id

            if user.role == 'admin':
                return redirect(url_for('admin.employees'))

            return redirect(url_for('client.clients'))

        flash('Login inválido', 'danger')

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))