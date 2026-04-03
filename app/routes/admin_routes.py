from flask import Blueprint, render_template, redirect, url_for, flash
from app.models.user import User
from app import db
from app.forms.employee_form import EmployeeForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/employees', methods=['GET', 'POST'])
def employees():
    form = EmployeeForm()

    if form.validate_on_submit():
        employee = User(username=form.username.data, role='employee')
        employee.set_password(form.password.data)

        db.session.add(employee)
        db.session.commit()

        flash('Funcionário criado!', 'success')
        return redirect(url_for('admin.employees'))

    employees = User.query.filter_by(role='employee').all()
    return render_template('employees.html', form=form, employees=employees)