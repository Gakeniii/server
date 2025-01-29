#!/usr/bin/env python3

# Remote library imports
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from flask import Flask, render_template, redirect, url_for, request, session
from flask import request ,jsonify, session
from flask_restful import Resource
from models import db, Doctor, Patient, Appointment, Specialty, PaymentOption




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# db = SQLAlchemy(app)
db.init_app(app)

migrate = Migrate(app, db)

api = Api(app)

CORS(app,  resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def home():
    return ('Hello there welcome!')

class DoctorResource(Resource):
    def get(self, doctor_id=None):
        if doctor_id:
            doctor = Doctor.query.get(doctor_id)
            if not doctor:
                return ({'message': 'Doctor not found'}), 404
            return {
                'id': doctor.id,
                'name': doctor.name,
                'email': doctor.email,
                'age': doctor.age,
                'phone_no': doctor.phone_no,
                'specialty': doctor.specialty.specialty if doctor.specialty else None,
                'appointments': [{
                    'id': appointment.id,
                    'date': appointment.date.strftime("%m/%d/%Y"),
                    'time': appointment.time.strftime("%I:%M%p"),  
                    'prev_appointment': appointment.prev_appointment.strftime("%m/%d/%Y") if appointment.prev_appointment else None,
                    'status': appointment.status,
                    'treatment_plan': appointment.treatment_plan,
                    'notes': appointment.notes,
                    'diagnosis': appointment.diagnosis,
                    'patient_name': appointment.patient.name if appointment.patient else None,
                    'patient_id': appointment.patient_id
                } for appointment in doctor.appointments]
            }
        doctors = Doctor.query.all()
        return [{
            'id': doctor.id,
            'name': doctor.name,
            'email': doctor.email,
            'age': doctor.age,
            'phone_no': doctor.phone_no,
            'specialty': doctor.specialty.specialty if doctor.specialty else None,
            'appointments': [{
                'id': appointment.id,
                'date': appointment.date.strftime("%m/%d/%Y"),  # Ensure it's a string
                'time': appointment.time.strftime("%I:%M%p"),    # Ensure it's a string
                'diagnosis': appointment.diagnosis,
                'patient_name': appointment.patient.name if appointment.patient else None,
                'patient_id': appointment.patient_id
            } for appointment in doctor.appointments]
        } for doctor in doctors]

    def post(self):
        data = request.get_json()
        specialty = Specialty.query.get(data['specialty_id']) if 'specialty_id' in data else None
        doctor = Doctor(
            name=data['name'],
            email=data['email'],
            age=data['age'],
            phone_no=data['phone_no'],
            specialty=specialty
        )
        db.session.add(doctor)
        db.session.commit()
        return {'message': 'Doctor created', 'doctor': doctor.id}, 201

    def patch(self, doctor_id):
        doctor = Doctor.query.get(doctor_id)
        data = request.get_json()
        if not doctor:
            return {'message': 'Doctor not found'}, 404
        doctor.name = data.get('name', doctor.name)
        doctor.email = data.get('email', doctor.email)
        doctor.age = data.get('age', doctor.age)
        doctor.phone_no = data.get('phone_no', doctor.phone_no)
        doctor.specialty_id = data.get('specialty_id', doctor.specialty_id)
        db.session.commit()
        return {'message': 'Doctor updated', 'doctor': doctor.id}

    def delete(self, doctor_id):
        doctor = Doctor.query.get_or_404(doctor_id)
        db.session.delete(doctor)
        db.session.commit()
        return {'message': 'Doctor deleted'}

class PatientResource(Resource):
    def get(self, patient_id=None):
        if patient_id:
            patient = Patient.query.get(patient_id)
            if not patient:
                return ({'message': 'Patient not found'}), 404
            return {
                'id': patient.id,
                'name': patient.name,
                'phone_no': patient.phone_no,
                'age': patient.age,
                'appointments': [{
                    'id': appointment.id,
                    'date': appointment.date.strftime("%m/%d/%Y"),  # Ensure it's a string
                    'time': appointment.time.strftime("%I:%M%p"),    # Ensure it's a string
                    'prev_appointment': appointment.prev_appointment.strftime("%m/%d/%Y") if appointment.prev_appointment else None,
                    'status': appointment.status,
                    'treatment_plan': appointment.treatment_plan,
                    'notes': appointment.notes,
                    'diagnosis': appointment.diagnosis,
                    'doctor_id': appointment.doctor_id,
                    'doctor': {
                        'id': appointment.doctor.id,
                        'name': appointment.doctor.name,
                        'email': appointment.doctor.email,
                    }
                } for appointment in patient.appointments]
            }
        patients = Patient.query.all()
        return [{
            'id': patient.id,
            'name': patient.name,
            'phone_no': patient.phone_no,
            'age': patient.age
        } for patient in patients]
    

    def post(self):
        data = request.get_json()
        patient = Patient(
            name=data['name'],
            phone_no=data['phone_no'],
            age=data['age']
        )
        db.session.add(patient)
        db.session.commit()
        return {'message': 'Patient created', 'patient': patient.id}, 201

    def patch(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)
        data = request.get_json()
        patient.name = data.get('name', patient.name)
        patient.phone_no = data.get('phone_no', patient.phone_no)
        patient.age = data.get('age', patient.age)
        db.session.commit()
        return {'message': 'Patient updated', 'patient': patient.id}

    def delete(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        return {'message': 'Patient deleted'}

class AppointmentResource(Resource):
    def get(self, appointment_id=None):
        if appointment_id:
            appointment = Appointment.query.get(appointment_id)
            if not appointment:
                return ({'message': 'Appointment not found'}), 404
            return {
                'id': appointment.id,
                'date': appointment.date.strftime("%m/%d/%Y"),  # Ensure it's a string
                'time': appointment.time.strftime("%I:%M%p"), 
                'prev_appointment': appointment.prev_appointment.strftime("%m/%d/%Y") if appointment.prev_appointment else None,
                'status': appointment.status,
                'treatment_plan': appointment.treatment_plan,
                'notes': appointment.notes,
                'diagnosis': appointment.diagnosis,
                'patient_id': appointment.patient_id,
                'patient': {
                    'id': appointment.patient.id,
                    'name': appointment.patient.name,
                    'age': appointment.patient.age
                },
                'doctor_id': appointment.doctor_id,
                'doctor': {
                    'id': appointment.doctor.id,
                    'name': appointment.doctor.name,
                    'email': appointment.doctor.email,
                }
            }       

        appointments = Appointment.query.all()
        return [{
            'id': appointment.id,
            'date': appointment.date.strftime("%m/%d/%Y"),  # Format the date object
            'time': appointment.time.strftime("%I:%M%p"),
            'prev_appointment': appointment.prev_appointment.strftime("%m/%d/%Y") if appointment.prev_appointment else None,
            'status': appointment.status,
            'diagnosis': appointment.diagnosis,
            'patient_id': appointment.patient_id,
            'doctor_id': appointment.doctor_id,
            'doctor': {
                    'id': appointment.doctor.id,
                    'name': appointment.doctor.name,
                    'email': appointment.doctor.email,
                }
        } for appointment in appointments]

    def post(self):
        data = request.get_json()

        date_string = data.get('date')
        if not date_string:
            return {'message': 'Date is required'}, 400
        try:
            date_object = datetime.strptime(date_string, "%m/%d/%y").date()
            
        except ValueError:
            return {'message': 'Invalid date format. Please use MM/DD/YY.'}, 400

        time_string = data.get('time')
    
        if not time_string:
            return {'message': 'Time is required'}, 400

        try:
            time_object = datetime.strptime(time_string, "%I:%M%p").time()
        except ValueError:
            return {'message': 'Invalid time format. Please use HH:MMAM/PM.'}, 400

    
        appointment = Appointment(
            date=date_object,
            time=time_object,
            prev_appointment=date_object,
            status=data.get('status', 'Scheduled'),
            treatment_plan=data.get('treatment_plan'),
            notes=data.get('notes'),
            diagnosis=data.get('diagnosis'),
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id']
        )
        db.session.add(appointment)
        db.session.commit()
        return {
            'message': 'Appointment created',
            'appointment': appointment.id,
            'date': appointment.date.strftime("%m/%d/%Y"),  # Format the date object as a string
            'time': appointment.time.strftime("%I:%M%p")   # Format the time object as a string
        }, 201
    
    def patch(self, appointment_id):
        appointment = Appointment.query.get_or_404(appointment_id)
        data = request.get_json()

        date_string = data.get('date', appointment.date.strftime("%m/%d/%Y"))
        try:
            appointment.date = datetime.strptime(date_string, "%m/%d/%Y").date()
        except ValueError:
            return {'message': 'Invalid date format. Please use MM/DD/YYYY.'}, 400
        time_string = data.get('time', appointment.time.strftime("%I:%M%p"))
        try:
            appointment.time = datetime.strptime(time_string, "%I:%M%p").time()
        except ValueError:
            return {'message': 'Invalid time format. Please use HH:MMAM/PM.'}, 400
        try:
            appointment.prev_appointment = datetime.strptime(date_string, "%m/%d/%Y").date()
        except ValueError:
            return {'message': 'Invalid date format. Please use MM/DD/YYYY.'}, 400
        

        appointment.status = data.get('status', appointment.status)
        appointment.treatment_plan = data.get('treatment_plan', appointment.treatment_plan)
        appointment.notes = data.get('notes', appointment.notes)
        appointment.diagnosis = data.get('diagnosis', appointment.diagnosis)

        db.session.commit()
        
        appointment_data = {
            'message': 'Appointment updated',
            'appointment': {
                'id': appointment.id,
                'date': appointment.date.strftime("%m/%d/%Y"),  # Ensure it's a string
                'time': appointment.time.strftime("%I:%M%p"),    # Ensure it's a string
                'prev_appointment': appointment.prev_appointment.strftime("%m/%d/%Y") if appointment.prev_appointment else None,
                'status': appointment.status,
                'treatment_plan': appointment.treatment_plan,
                'notes': appointment.notes,
                'diagnosis': appointment.diagnosis,
                'patient_id': appointment.patient_id,
                'doctor_id': appointment.doctor_id
            }
        }
        return {'message': 'Appointment updated', 'appointment': appointment_data}

    def delete(self, appointment_id):
        appointment = Appointment.query.get_or_404(appointment_id)
        db.session.delete(appointment)
        db.session.commit()
        return {'message': 'Appointment deleted'}

class SpecialtyResource(Resource):
    def get(self, specialty_id=None):
        if specialty_id:
            specialty = Specialty.query.get(specialty_id)
            if not specialty:
                return ({'message': 'Specialty not found'}), 404
            return {'id': specialty.id, 'specialty': specialty.specialty}
        specialties = Specialty.query.all()
        return [{'id': specialty.id,
                 'specialty': specialty.specialty,
                 'doctors': [{
                        'id': doctor.id,
                        'name': doctor.name,
                        'email': doctor.email,
                        'age': doctor.age,
                        'phone_no': doctor.phone_no
                    } for doctor in specialty.doctors]
                } for specialty in specialties]

    def post(self):
        data = request.get_json()
        specialty = Specialty(
            specialty=data['specialty'])
        db.session.add(specialty)
        db.session.commit()
        return {'message': 'Specialty created', 'specialty': specialty.id}, 201

    def patch(self, specialty_id):
        specialty = Specialty.query.get_or_404(specialty_id)
        data = request.get_json()
        specialty.specialty = data.get('specialty', specialty.specialty)
        db.session.commit()
        return {'message': 'Specialty updated', 'specialty': specialty.id}

    def delete(self, specialty_id):
        specialty = Specialty.query.get_or_404(specialty_id)
        db.session.delete(specialty)
        db.session.commit()
        return {'message': 'Specialty deleted'}

class PaymentOptionResource(Resource):
    def get(self, payment_option_id=None):
        if payment_option_id:
            payment_option = PaymentOption.query.get(payment_option_id)
            if not payment_option:
                return ({'message': 'Payment option not found'}), 404
            return {
                'id': payment_option.id,
                'credit_card': payment_option.credit_card,
                'debit_card': payment_option.debit_card,
                'insurance': payment_option.insurance,
                'angel_donation': payment_option.angel_donation,
                'patient_id': payment_option.patient_id,
                'patient': {
                    'name': payment_option.patient.name,
                    'phone_no': payment_option.patient.phone_no,
                    'age': payment_option.patient.age
                }
            }
            
        payment_options = PaymentOption.query.all()
        return [{
            'id': payment_option.id,
            'credit_card': payment_option.credit_card,
            'debit_card': payment_option.debit_card,
            'insurance': payment_option.insurance,
            'angel_donation': payment_option.angel_donation,
            'patient_id': payment_option.patient_id,
            'patient': {
                'name': payment_option.patient.name,
                'phone_no': payment_option.patient.phone_no,
                'age': payment_option.patient.age
            }
        } for payment_option in payment_options]

    def post(self):
        data = request.get_json()
        payment_option = PaymentOption(
            credit_card=data.get('credit_card'),
            debit_card=data.get('debit_card'),
            insurance=data.get('insurance'),
            angel_donation=data.get('angel_donation'),
            patient_id=data['patient_id']
        )
        db.session.add(payment_option)
        db.session.commit()
        return {'message': 'Payment option created', 'payment_option': payment_option.id}, 201

    def patch(self, payment_option_id):
        payment_option = PaymentOption.query.get(payment_option_id)
        data = request.get_json()
        if not payment_option:
            return {'message': 'Payment option not found'}, 404
        
        payment_option.credit_card = data.get('credit_card', payment_option.credit_card)
        payment_option.debit_card = data.get('debit_card', payment_option.debit_card)
        payment_option.insurance = data.get('insurance', payment_option.insurance)
        payment_option.angel_donation = data.get('angel_donation', payment_option.angel_donation)
        db.session.commit()
        return {'message': 'Payment option updated', 'payment_option': payment_option.id}

    def delete(self, payment_option_id):
        payment_option = PaymentOption.query.get_or_404(payment_option_id)
        db.session.delete(payment_option)
        db.session.commit()
        return {'message': 'Payment option deleted'}

# Add routes to the API
api.add_resource(DoctorResource, '/doctors', '/doctors/<int:doctor_id>')
api.add_resource(PatientResource, '/patients', '/patients/<int:patient_id>')
api.add_resource(AppointmentResource, '/appointments', '/appointments/<int:appointment_id>')
api.add_resource(SpecialtyResource, '/specialties', '/specialties/<int:specialty_id>')
api.add_resource(PaymentOptionResource, '/payment-options', '/payment-options/<int:payment_option_id>')



# @login_manager.user_loader
# def load_user(user_id):
#     return Administrator.query.get(int(user_id))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
        
#         admin = Administrator.query.filter_by(email=email).first()
        
#         if admin and admin.check_password(password):
#             login_user(admin)
#             return redirect(url_for('home'))  # Redirect to dashboard or home page
#         else:
#             return 'Invalid email or password'

#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('login'))  # Redirect to login page after logout




if __name__ == '__main__':
    db.create_all()
    app.run(port=5000, debug=True)

