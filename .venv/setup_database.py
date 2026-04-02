import sqlite3        # built into Python - lets us work with SQLite databases
import random         # for generating random data
from datetime import datetime, timedelta  # for working with dates

# --- CONNECT TO DATABASE ---
# This creates a file called clinic.db in your project folder
# Think of it like creating a new Excel file
conn = sqlite3.connect("clinic.db")
cursor = conn.cursor()  # cursor is like a pen that writes to the database

# --- CREATE TABLES ---
cursor.executescript("""
    DROP TABLE IF EXISTS invoices;
    DROP TABLE IF EXISTS treatments;
    DROP TABLE IF EXISTS appointments;
    DROP TABLE IF EXISTS doctors;
    DROP TABLE IF EXISTS patients;

    CREATE TABLE patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        date_of_birth DATE,
        gender TEXT,
        city TEXT,
        registered_date DATE
    );

    CREATE TABLE doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        department TEXT,
        phone TEXT
    );

    CREATE TABLE appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        appointment_date DATETIME,
        status TEXT,
        notes TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients(id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(id)
    );

    CREATE TABLE treatments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        treatment_name TEXT,
        cost REAL,
        duration_minutes INTEGER,
        FOREIGN KEY (appointment_id) REFERENCES appointments(id)
    );

    CREATE TABLE invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        invoice_date DATE,
        total_amount REAL,
        paid_amount REAL,
        status TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    );
""")

print("Tables created successfully!")

# --- INSERT DOCTORS ---
doctors_data = [
    ("Dr. Anjali Sharma",  "Dermatology", "Skin & Hair",  "9876543201"),
    ("Dr. Rohan Mehta",    "Dermatology", "Skin & Hair",  "9876543202"),
    ("Dr. Priya Nair",     "Dermatology", "Skin & Hair",  None),
    ("Dr. Vikram Singh",   "Cardiology",  "Heart Care",   "9876543204"),
    ("Dr. Sunita Patel",   "Cardiology",  "Heart Care",   "9876543205"),
    ("Dr. Amit Joshi",     "Cardiology",  "Heart Care",   None),
    ("Dr. Kavitha Rao",    "Orthopedics", "Bone & Joint", "9876543207"),
    ("Dr. Deepak Verma",   "Orthopedics", "Bone & Joint", "9876543208"),
    ("Dr. Meera Iyer",     "Orthopedics", "Bone & Joint", None),
    ("Dr. Arun Kumar",     "General",     "General OPD",  "9876543210"),
    ("Dr. Sneha Desai",    "General",     "General OPD",  "9876543211"),
    ("Dr. Rahul Gupta",    "General",     "General OPD",  None),
    ("Dr. Pooja Reddy",    "Pediatrics",  "Child Care",   "9876543213"),
    ("Dr. Nikhil Bansal",  "Pediatrics",  "Child Care",   "9876543214"),
    ("Dr. Divya Pillai",   "Pediatrics",  "Child Care",   None),
]

cursor.executemany(
    "INSERT INTO doctors (name, specialization, department, phone) VALUES (?, ?, ?, ?)",
    doctors_data
)
print(f"Inserted {len(doctors_data)} doctors.")

# --- INSERT PATIENTS ---
first_names = ["Aarav","Aditi","Akash","Ananya","Arjun","Bhavna","Chetan","Deepa",
               "Farhan","Geeta","Harsh","Isha","Jayesh","Kavya","Lokesh","Meera",
               "Nikhil","Pooja","Rahul","Riya","Sachin","Shruti","Tarun","Uma",
               "Vishal","Yogita","Zara","Kiran","Mohit","Naina"]

last_names  = ["Sharma","Verma","Patel","Singh","Mehta","Joshi","Nair","Rao",
               "Iyer","Gupta","Desai","Reddy","Kumar","Pillai","Bansal","Mishra",
               "Agarwal","Chopra","Malhotra","Pandey"]

cities = ["Mumbai","Pune","Nagpur","Nashik","Aurangabad","Kolhapur","Solapur","Thane"]

patients_data = []
for i in range(200):
    fn    = random.choice(first_names)
    ln    = random.choice(last_names)
    email = f"{fn.lower()}.{ln.lower()}{i}@email.com" if random.random() > 0.2 else None
    phone = f"98{random.randint(10000000, 99999999)}" if random.random() > 0.15 else None
    dob   = datetime(random.randint(1950,2005), random.randint(1,12), random.randint(1,28)).strftime("%Y-%m-%d")
    gender     = random.choice(["M","F"])
    city       = random.choice(cities)
    reg_date   = (datetime.now() - timedelta(days=random.randint(0,730))).strftime("%Y-%m-%d")
    patients_data.append((fn, ln, email, phone, dob, gender, city, reg_date))

cursor.executemany(
    "INSERT INTO patients (first_name,last_name,email,phone,date_of_birth,gender,city,registered_date) VALUES (?,?,?,?,?,?,?,?)",
    patients_data
)
print(f"Inserted {len(patients_data)} patients.")

# --- INSERT APPOINTMENTS ---
statuses        = ["Scheduled","Completed","Cancelled","No-Show"]
status_weights  = [0.2, 0.55, 0.15, 0.10]
frequent_patients = random.sample(range(1,201), 30)

appointments_data = []
for _ in range(500):
    if random.random() < 0.4:
        patient_id = random.choice(frequent_patients)
    else:
        patient_id = random.randint(1,200)
    doctor_id  = random.randint(1,15)
    appt_date  = (datetime.now() - timedelta(days=random.randint(0,365))).strftime("%Y-%m-%d %H:%M:%S")
    status     = random.choices(statuses, weights=status_weights)[0]
    notes      = random.choice(["Follow-up needed","Routine checkup","First visit",None,None,None])
    appointments_data.append((patient_id, doctor_id, appt_date, status, notes))

cursor.executemany(
    "INSERT INTO appointments (patient_id,doctor_id,appointment_date,status,notes) VALUES (?,?,?,?,?)",
    appointments_data
)
print(f"Inserted {len(appointments_data)} appointments.")

# --- INSERT TREATMENTS ---
treatment_names = {
    "Dermatology": ["Skin biopsy","Acne treatment","Laser therapy","Chemical peel","Mole removal"],
    "Cardiology":  ["ECG","Stress test","Echocardiogram","BP monitoring","Angiography"],
    "Orthopedics": ["X-ray","Physiotherapy","Joint injection","Bone density scan","Plaster cast"],
    "General":     ["Blood test","Urine test","General consultation","Vaccination","BP check"],
    "Pediatrics":  ["Growth assessment","Vaccination","Fever management","Nutrition counseling","Allergy test"],
}

cursor.execute("""
    SELECT a.id, d.specialization
    FROM appointments a
    JOIN doctors d ON a.doctor_id = d.id
    WHERE a.status = 'Completed'
    LIMIT 350
""")
completed = cursor.fetchall()

treatments_data = []
for appt_id, specialization in completed:
    t_name   = random.choice(treatment_names.get(specialization, ["General treatment"]))
    cost     = round(random.uniform(50,5000), 2)
    duration = random.randint(10,120)
    treatments_data.append((appt_id, t_name, cost, duration))

cursor.executemany(
    "INSERT INTO treatments (appointment_id,treatment_name,cost,duration_minutes) VALUES (?,?,?,?)",
    treatments_data
)
print(f"Inserted {len(treatments_data)} treatments.")

# --- INSERT INVOICES ---
inv_statuses = ["Paid","Pending","Overdue"]
inv_weights  = [0.55, 0.25, 0.20]

invoices_data = []
for _ in range(300):
    patient_id   = random.randint(1,200)
    invoice_date = (datetime.now() - timedelta(days=random.randint(0,365))).strftime("%Y-%m-%d")
    total        = round(random.uniform(100,8000), 2)
    status       = random.choices(inv_statuses, weights=inv_weights)[0]
    paid         = total if status == "Paid" else round(random.uniform(0, total*0.8), 2)
    invoices_data.append((patient_id, invoice_date, total, paid, status))

cursor.executemany(
    "INSERT INTO invoices (patient_id,invoice_date,total_amount,paid_amount,status) VALUES (?,?,?,?,?)",
    invoices_data
)
print(f"Inserted {len(invoices_data)} invoices.")

# --- SAVE AND CLOSE ---
conn.commit()  # saves everything to the file
conn.close()   # closes the connection

print("\nDone! clinic.db is ready.")
print("Summary: 200 patients | 15 doctors | 500 appointments | treatments | 300 invoices")