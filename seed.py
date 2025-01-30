from random import randint, choice as rc
from faker import Faker
from datetime import datetime
from app import app
from models import db, Doctor, Patient, Appointment, Specialty, PaymentOption

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
            phone_no=f"07{randint(100000000, 999999999)}",  # Ensuring phone number is 10 digits and starts with 07
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
            phone_no=f"07{randint(100000000, 999999999)}",  # Ensuring phone number is 10 digits and starts with 07
            age=randint(1, 90)
        )
        patients.append(patient)
    db.session.add_all(patients)
    db.session.commit()
    return patients

def convert_to_time(time_str):
    return datetime.strptime(time_str, '%I:%M%p').time()

# Convert a string or datetime to a date object
def convert_to_date(date_str):
    if isinstance(date_str, str):
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    return date_str  # already a date object

# Example seed data
def seed_appointments(doctors, patients):
    appointment_data = [
        {
            'date': convert_to_date('2025-01-10'),  # Convert date string to date object
            'status': 'Completed',
            'treatment_plan': 'Inhalers, Avoiding Triggers',
            'notes': 'Patient is advised to avoid all potential triggers.',
            'doctor_id': 4,
            'patient_id': 1,
            'diagnosis': 'Asthma',
            'prev_appointment': convert_to_date('2025-01-01'),  # Convert date string to date object
            'time': convert_to_time('02:53PM')
        },
        {
            'date': convert_to_date('2025-01-01'),
            'status': 'Scheduled',
            'treatment_plan': 'Inhalers, Avoiding Triggers',
            'notes': 'Patient is advised to avoid all potential triggers.',
            'doctor_id': 3,
            'patient_id': 5,
            'diagnosis': 'Asthma',
            'prev_appointment': convert_to_date('2025-01-01'),
            'time': convert_to_time('12:39AM')
        },
        {
            'date': convert_to_date('2025-01-19'),
            'status': 'Canceled',
            'treatment_plan': 'Inhalers, Avoiding Triggers',
            'notes': 'Patient is advised to avoid all potential triggers.',
            'doctor_id': 7,
            'patient_id': 9,
            'diagnosis': 'Asthma',
            'time': convert_to_time('08:12PM'),
            'prev_appointment': None
        },
        {
            'date': convert_to_date('2025-01-25'),
            'status': 'Scheduled',
            'treatment_plan': 'Physical Therapy, Pain Relief Medication',
            'notes': 'Encourage patient to avoid lifting and follow physical therapy routine.',
            'doctor_id': 4,
            'patient_id': 8,
            'diagnosis': 'Back Pain',
            'time': convert_to_time('07:44PM'),
            'prev_appointment': None
        },
        {
            'date': convert_to_date('2025-01-03'),
            'status': 'Canceled',
            'treatment_plan': 'Antibiotics, Rest, Hydration',
            'notes': 'Patient is recovering well with rest. Advised to avoid strenuous activities for a few weeks.',
            'doctor_id': 8,
            'patient_id': 9,
            'diagnosis': 'Pneumonia',
            'time': convert_to_time('01:05AM'),
            'prev_appointment': None
        },
        {
            'date': convert_to_date('2025-01-02'),
            'status': 'Scheduled',
            'treatment_plan': 'Anti-inflammatory Drugs, Joint Exercises',
            'notes': 'Patient advised on medication for pain relief.',
            'doctor_id': 7,
            'patient_id': 8,
            'diagnosis': 'Arthritis',
            'time': convert_to_time('04:47PM'),
            'prev_appointment': None
        },
        {
            'date': convert_to_date('2025-01-14'),
            'status': 'Completed',
            'treatment_plan': 'Physical Therapy, Pain Relief Medication',
            'notes': 'Encourage patient to avoid lifting and follow physical therapy routine.',
            'doctor_id': 6,
            'patient_id': 3,
            'diagnosis': 'Back Pain',
            'time': convert_to_time('05:59PM'),
            'prev_appointment': convert_to_date('2025-01-20')
        },
        {
            'date': convert_to_date('2025-01-15'),
            'status': 'Scheduled',
            'treatment_plan': 'Anti-inflammatory Drugs, Joint Exercises',
            'notes': 'Patient advised on taking prescribed medication for pain relief.',
            'doctor_id': 4,
            'patient_id': 3,
            'diagnosis': 'Arthritis',
            'time': convert_to_time('05:25AM'),
            'prev_appointment': convert_to_date('2025-01-04')
        },
        {
            'date': convert_to_date('2025-01-18'),
            'status': 'Scheduled',
            'treatment_plan': 'Antidepressants, Therapy Sessions',
            'notes': 'Patient is showing improvement and following prescribed medication.',
            'doctor_id': 6,
            'patient_id': 1,
            'diagnosis': 'Depression',
            'time': convert_to_time('03:31AM'),
            'prev_appointment': convert_to_date('2025-01-24')
        },
        {
            'date': convert_to_date('2025-01-02'),
            'status': 'Scheduled',
            'treatment_plan': 'Anti-inflammatory Drugs, Joint Exercises',
            'notes': 'Patient advised on taking prescribed medication for pain relief.',
            'doctor_id': 10,
            'patient_id': 3,
            'diagnosis': 'Arthritis',
            'time': convert_to_time('09:51AM'),
            'prev_appointment': None
        }
    ]

    # Insert each appointment into the database
    for appointment in appointment_data:
        new_appointment = Appointment(**appointment)
        db.session.add(new_appointment)

    db.session.commit()

def seed_payment_options(patients):
    payment_options = []
    
    for patient in patients:
        payment = PaymentOption(
            credit_card=fake.credit_card_number() if randint(0, 1) else None,  # Randomly generate a credit card or None
            debit_card=fake.credit_card_number() if randint(0, 1) else None,   # Randomly generate a debit card or None
            insurance=fake.company() if randint(0, 1) else None,               # Randomly generate an insurance company or None
            angel_donation=fake.word() if randint(0, 1) else None,             # Randomly generate an angel donation or None
            patient_id=patient.id  # Linking the payment option to the patient
        )
        
        payment_options.append(payment)
    
    db.session.add_all(payment_options)
    db.session.commit()
    print(f"Generated {len(payment_options)} payment options.")

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