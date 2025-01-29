from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Doctor(db.Model, SerializerMixin):
    __tablename__ = 'doctor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialty.id'))

    specialty = relationship('Specialty', back_populates='doctors')
    appointments = relationship('Appointment', back_populates='doctor', cascade='all, delete-orphan')

    # Define serialization rules
    serialize_rules = ('-appointments.doctor', '-specialty.doctors')

class Patient(db.Model, SerializerMixin):
    __tablename__ = 'patient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    appointments = relationship('Appointment', back_populates='patient', cascade='all, delete-orphan')
    payment_options = relationship('PaymentOption', back_populates='patient', cascade='all, delete-orphan')

    serialize_rules = ('-appointments.patient', '-payment_options.patient')

class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointment'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    prev_appointment = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), default='Scheduled', nullable=False)
    treatment_plan = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    diagnosis = db.Column(db.String(255), nullable=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))

    patient = relationship('Patient', back_populates='appointments')
    doctor = relationship('Doctor', back_populates='appointments')

    serialize_rules = ('-patient.appointments', '-doctor.appointments')

class Specialty(db.Model, SerializerMixin):
    __tablename__ = 'specialty'

    id = db.Column(db.Integer, primary_key=True)
    specialty = db.Column(db.String(100), nullable=False)

    doctors = relationship('Doctor', back_populates='specialty', cascade='all, delete-orphan')

    serialize_rules = ('-doctors.specialty',)

class PaymentOption(db.Model, SerializerMixin):
    __tablename__ = 'payment_option'

    id = db.Column(db.Integer, primary_key=True)
    credit_card = db.Column(db.String(100), nullable=True)
    debit_card = db.Column(db.String(100), nullable=True)
    insurance = db.Column(db.String(100), nullable=True)
    angel_donation = db.Column(db.String(100), nullable=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

    patient = relationship('Patient', back_populates='payment_options')

    serialize_rules = ('-patient.payment_options',)