from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, Administrator, Doctor, Patient, Appointment, Specialty, PaymentOption

fake = Faker()

def seed_specialties():
    specialties = [
        "Surgeon", "Neurosurgeon", "Pediatrician", "Cardiologist", "Dermatologist",
        "Orthopedic Surgeon", "Oncologist", "Psychiatrist", "Endocrinologist", "Ophthalmologist"
    ]
    specialty_objects = [Specialty(specialty=s) for s in specialties]
    db.session.add_all(specialty_objects)
    db.session.commit()
    return specialty_objects

def seed_doctors(specialties):
    doctors = []
    for _ in range(10):
        doctor = Doctor(
            name=fake.name(),
            email=fake.email(),
            age=randint(30, 65),
            phone_no=fake.phone_number(),
            specialty_id=rc(specialties).id
        )
        doctors.append(doctor)
    db.session.add_all(doctors)
    db.session.commit()
    return doctors

def seed_patients():
    patients = []
    for _ in range(10):
        patient = Patient(
            name=fake.name(),
            phone_no=fake.phone_number(),
            age=randint(1, 90)
        )
        patients.append(patient)
    db.session.add_all(patients)
    db.session.commit()
    return patients

def seed_appointments(doctors, patients):
    appointments = []
    for _ in range(10):
        appointment = Appointment(
            date=fake.date_this_year(),
            time=fake.time_object(),
            prev_appointment=fake.date_this_year() if randint(0, 1) else None,
            status=rc(["Scheduled", "Completed", "Canceled"]),
            treatment_plan=fake.text(),
            notes=fake.text(),
            diagnosis=fake.sentence(),
            patient_id=rc(patients).id,
            doctor_id=rc(doctors).id
        )
        appointments.append(appointment)
    db.session.add_all(appointments)
    db.session.commit()
    return appointments

def seed_payment_options(patients):
    payment_options = []
    for patient in patients:
        payment = PaymentOption(
            credit_card=fake.credit_card_number() if randint(0, 1) else None,
            debit_card=fake.credit_card_number() if randint(0, 1) else None,
            insurance=fake.company() if randint(0, 1) else None,
            angel_donation=fake.word() if randint(0, 1) else None,
            patient_id=patient.id
        )
        payment_options.append(payment)
    db.session.add_all(payment_options)
    db.session.commit()

def run_seed():
    with app.app_context():
        print("Starting seed...")
        db.drop_all()
        db.create_all()
        
        specialties = seed_specialties()
        doctors = seed_doctors(specialties)
        patients = seed_patients()
        seed_appointments(doctors, patients)
        seed_payment_options(patients)
        
        print("Seeding complete!")

if __name__ == '__main__':
    run_seed()
