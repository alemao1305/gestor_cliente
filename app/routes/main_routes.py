from flask import Blueprint, render_template, redirect, url_for, flash
from app.models.user import User
from app import db
from app.forms.auth_form import LoginForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return redirect(url_for('auth.login'))