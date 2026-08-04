import streamlit as st

st.title("🏥 Hospital Appointment AI Assistant")

st.write("Welcome to Hospital Appointment System")

patient_name = st.text_input("Patient Name")

department = st.selectbox(
    "Department",
    ["Cardiology", "Neurology", "Dental", "General Medicine"]
)

doctor = st.text_input("Doctor Name")

date = st.date_input("Appointment Date")

if st.button("Book Appointment"):
    st.success("Appointment booked successfully!")