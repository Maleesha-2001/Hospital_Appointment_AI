import streamlit as st
import sqlite3


# Database connection
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()


# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT,
    department TEXT,
    doctor TEXT,
    appointment_date TEXT
)
""")

conn.commit()


st.title("🏥 Hospital Appointment AI Assistant")

st.write("Welcome to Hospital Appointment System")


# Patient details
patient_name = st.text_input("👤 Patient Name")


# AI Medical Assistant
st.subheader("🤖 AI Medical Assistant")

symptoms = st.text_area("Describe your symptoms")


recommended_department = ""

if symptoms:
    symptoms_lower = symptoms.lower()

    if "heart" in symptoms_lower or "chest pain" in symptoms_lower:
        recommended_department = "Cardiology"

    elif "headache" in symptoms_lower or "brain" in symptoms_lower:
        recommended_department = "Neurology"

    elif "tooth" in symptoms_lower or "dental" in symptoms_lower:
        recommended_department = "Dental"

    else:
        recommended_department = "General Medicine"

    st.info(
        f"AI Recommended Department: {recommended_department}"
    )


# Appointment details

department = st.selectbox(
    "🏥 Department",
    [
        "Cardiology",
        "Neurology",
        "Dental",
        "General Medicine"
    ]
)


doctor = st.text_input("👨‍⚕️ Doctor Name")

date = st.date_input("📅 Appointment Date")


# Save appointment

if st.button("✅ Book Appointment"):

    cursor.execute(
        """
        INSERT INTO appointments 
        (patient_name, department, doctor, appointment_date)
        VALUES (?, ?, ?, ?)
        """,
        (
            patient_name,
            department,
            doctor,
            str(date)
        )
    )

    conn.commit()

    st.success("Appointment booked and saved successfully! 🎉")
# Appointment History

st.subheader("📋 Appointment History")

cursor.execute("SELECT * FROM appointments")
appointments = cursor.fetchall()

if appointments:
    for appointment in appointments:
        st.write(
            f"""
            🆔 ID: {appointment[0]}  
            👤 Patient: {appointment[1]}  
            🏥 Department: {appointment[2]}  
            👨‍⚕️ Doctor: {appointment[3]}  
            📅 Date: {appointment[4]}
            ---
            """
        )
else:
    st.info("No appointments found.")