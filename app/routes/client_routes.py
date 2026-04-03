from flask import Blueprint, render_template, redirect, url_for, flash
from app.models.client import Client
from app import db
from app.forms.client_form import ClientForm

client_bp = Blueprint('client', __name__)

@client_bp.route('/clients', methods=['GET', 'POST'])
def clients():
    form = ClientForm()

    if form.validate_on_submit():
        client = Client(
            cpf=form.cpf.data,
            name=form.name.data,
            contact=form.contact.data,
            email=form.email.data,
            address=form.address.data,
            house_number=form.house_number.data
        )

        db.session.add(client)
        db.session.commit()

        flash('Cliente criado!', 'success')
        return redirect(url_for('client.clients'))

    clients = Client.query.all()
    return render_template('clients.html', form=form, clients=clients)