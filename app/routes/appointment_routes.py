from flask import Blueprint, render_template, redirect, url_for, flash
from app.models.appointment import Appointment
from app.models.client import Client
from app import db
from app.forms.appointment_form import AppointmentForm

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/appointments', methods=['GET', 'POST'])
def appointments():
    form = AppointmentForm()

    if form.validate_on_submit():
        client = Client.query.get(form.client_cpf.data)

        if not client:
            flash('Cliente não encontrado', 'danger')
            return redirect(url_for('appointment.appointments'))

        appointment = Appointment(
            client_id=client.cpf,
            date=form.date.data,
            time=form.time.data,
            service=form.service.data
        )

        db.session.add(appointment)
        db.session.commit()

        flash('Agendamento criado!', 'success')
        return redirect(url_for('appointment.appointments'))

    appointments = Appointment.query.all()
    return render_template('appointments.html', form=form, appointments=appointments)

@appointment_bp.route('/calendar')
def calendar():
    return render_template('calendar.html')