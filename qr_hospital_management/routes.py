from flask import Blueprint, render_template, redirect, url_for, flash, request
from create_app import db
from forms import PatientForm
from models import Patient
import qrcode
from io import BytesIO
from flask import send_file

main = Blueprint('main', __name__)

@main.route('/')
def index():
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)

@main.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(name=form.name.data, age=form.age.data, condition=form.condition.data)
        db.session.add(patient)
        db.session.commit()
        flash('Patient added successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_patient.html', form=form)

@main.route('/patient/<int:patient_id>')
def view_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('view_patient.html', patient=patient)

@main.route('/qrcode')
def generate_qrcode():
    text = request.args.get('text')
    if not text:
        flash('No text for QR code provided', 'danger')
        return redirect(url_for('main.index'))
    
    img = qrcode.make(text)
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png')
