import streamlit as st
import sqlite3
import pandas as pd

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Hospital Appointment AI Assistant",
    page_icon="🏥"
)


# ---------------- DATABASE ----------------

conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

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

# ---------------- DOCTOR DATABASE ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_name TEXT,
    department TEXT
)
""")

conn.commit()


# Insert doctors only if table is empty

cursor.execute(
    "SELECT COUNT(*) FROM doctors"
)

doctor_count = cursor.fetchone()[0]


if doctor_count == 0:

    doctors = [
        ("Dr. Kasun Perera", "Cardiology"),
        ("Dr. Nimal Fernando", "Neurology"),
        ("Dr. Amal Silva", "Dental"),
        ("Dr. Perera", "General Medicine")
    ]

    cursor.executemany(
        """
        INSERT INTO doctors
        (doctor_name, department)
        VALUES (?, ?)
        """,
        doctors
    )

    conn.commit()


# ---------------- TITLE ----------------

st.title("🏥 Hospital Appointment AI Assistant")
st.write("Welcome to AI-powered Hospital Appointment System")


# ---------------- AI MEDICAL ASSISTANT ----------------

# ---------------- AI CHAT STYLE UI ----------------

st.header("🤖 AI Medical Assistant")

st.write(
    "Chat with our AI assistant to get basic symptom guidance"
)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


symptoms = st.chat_input(
    "Type your symptoms here..."
)


if symptoms:

    st.session_state.chat_history.append(
        ("You", symptoms)
    )


for sender, message in st.session_state.chat_history:

    if sender == "You":

        st.chat_message("user").write(message)

    else:

        st.chat_message("assistant").write(message)


recommended_department = "General Medicine"
recommended_doctor = "Dr. Perera"
confidence = 70
priority = "Low"


if symptoms:

    symptoms_lower = symptoms.lower() if symptoms else ""


    emergency_words = [
        "chest pain",
        "difficulty breathing",
        "unconscious",
        "heavy bleeding"
    ]


    if any(word in symptoms_lower for word in emergency_words):

        priority = "🚨 High"

        st.error(
            "Emergency symptoms detected. Please seek immediate medical attention."
        )


    if (
        "heart" in symptoms_lower
        or "chest pain" in symptoms_lower
        or "palpitation" in symptoms_lower
    ):

        recommended_department = "Cardiology"
        recommended_doctor = "Dr. Kasun Perera"
        confidence = 90


    elif (
        "headache" in symptoms_lower
        or "migraine" in symptoms_lower
        or "dizziness" in symptoms_lower
    ):

        recommended_department = "Neurology"
        recommended_doctor = "Dr. Nimal Fernando"
        confidence = 85


    elif (
        "tooth" in symptoms_lower
        or "dental" in symptoms_lower
        or "gum" in symptoms_lower
    ):

        recommended_department = "Dental"
        recommended_doctor = "Dr. Amal Silva"
        confidence = 90


    elif (
        "fever" in symptoms_lower
        or "cough" in symptoms_lower
        or "cold" in symptoms_lower
    ):

        recommended_department = "General Medicine"
        recommended_doctor = "Dr. Perera"
        confidence = 80

    st.session_state.chat_history.append(
    (
        "AI",
        f"""
🏥 Department: {recommended_department}

👨‍⚕️ Doctor: {recommended_doctor}

📊 Confidence: {confidence}%

⚠️ Priority: {priority}
"""
    )
)    
    st.success("AI Analysis Completed")


    st.write("### 🏥 Recommended Department")
    st.info(recommended_department)


    st.write("### 👨‍⚕️ Recommended Doctor")
    st.info(recommended_doctor)


    # Save AI recommendation
    st.session_state.booking_department = recommended_department
    st.session_state.booking_doctor = recommended_doctor


    st.session_state.recommended_department = recommended_department
    st.session_state.recommended_doctor = recommended_doctor

if st.button("📅 Book This Recommended Appointment"):

    st.success(
        "Recommendation selected. Please complete patient details below."
    )


    st.write("### 📊 AI Confidence")
    st.progress(confidence / 100)
    st.write(str(confidence) + "%")


    st.write("### ⚠️ Priority Level")
    st.warning(priority)



st.divider()


# ---------------- BOOK APPOINTMENT ----------------

st.header("📅 Book Appointment")


patient_name = st.text_input("👤 Patient Name")

default_department = st.session_state.get(
    "booking_department",
    "General Medicine"
)


department_list = [
    "Cardiology",
    "Neurology",
    "Dental",
    "General Medicine"
]


department = st.selectbox(
    "🏥 Department",
    department_list,
    index=department_list.index(default_department) 
    if default_department in department_list else 0
)

default_doctor = st.session_state.get(
    "booking_doctor",
    ""
)


doctor = st.text_input(
    "👨‍⚕️ Doctor Name",
    value=default_doctor
)


date = st.date_input(
    "📅 Appointment Date"
)



if st.button("✅ Book Appointment"):

    if patient_name == "":
        st.warning("Please enter patient name")

    else:

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

        st.success(
            "Appointment booked successfully 🎉"
        )



st.divider()


# ---------------- APPOINTMENT HISTORY ----------------

st.header("📋 Appointment History")


cursor.execute(
    "SELECT * FROM appointments"
)

appointments = cursor.fetchall()


if appointments:

    for a in appointments:

        st.write(
            f"""
            🆔 ID: {a[0]}  
            👤 Patient: {a[1]}  
            🏥 Department: {a[2]}  
            👨‍⚕️ Doctor: {a[3]}  
            📅 Date: {a[4]}
            ---
            """
        )

else:

    st.info("No appointments found")



st.divider()


# ---------------- CANCEL APPOINTMENT ----------------

st.header("❌ Cancel Appointment")


cancel_id = st.number_input(
    "Enter Appointment ID",
    min_value=1
)


if st.button("🗑 Cancel Appointment"):

    cursor.execute(
        "DELETE FROM appointments WHERE id=?",
        (cancel_id,)
    )

    conn.commit()

    st.success(
        "Appointment cancelled successfully"
    )



st.divider()
# ---------------- ADMIN DASHBOARD ----------------

st.subheader("📊 Admin Dashboard")

cursor.execute(
    "SELECT * FROM appointments"
)

data = cursor.fetchall()

if len(data) == 0:
    st.warning("No appointments available")

else:
    df = pd.DataFrame(
        data,
        columns=[
            "Patient Name",
            "Age",
            "Department",
            "Doctor",
            "Appointment Date"
        ]
    )

    st.write("### 📋 Appointment Details")
    st.dataframe(df)

    st.write("### 🏥 Appointments by Department")

    department_count = df["Department"].value_counts()

    st.bar_chart(department_count)
