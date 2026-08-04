import streamlit as st

st.title("🏥 Hospital Appointment AI Assistant")

st.write("Welcome to Hospital Appointment System")


# Patient details
patient_name = st.text_input("👤 Patient Name")


# AI Symptom Recommendation
st.subheader("🤖 AI Medical Assistant")

symptoms = st.text_area(
    "Describe your symptoms"
)


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


# Appointment booking

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


if st.button("✅ Book Appointment"):
    st.success(
        f"Appointment booked successfully for {patient_name}!"
    )