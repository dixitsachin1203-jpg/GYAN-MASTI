import streamlit as st
import random
import string
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="CBSE Results 2025", layout="centered")

# ------------------- STYLING -------------------
st.markdown("""
<style>
.header {
    background-color: #00a6a6;
    padding: 15px;
    color: white;
    font-size: 22px;
    font-weight: bold;
    text-align:center;
}
.title {
    text-align: center;
    font-size: 26px;
    font-weight: bold;
    margin-top: 10px;
}
.box {
    border: 1px solid #ccc;
    padding: 25px;
    border-radius: 10px;
    background-color: #f9f9f9;
}
.captcha {
    font-size: 20px;
    font-weight: bold;
    background-color: navy;
    color: white;
    padding: 5px 10px;
    display: inline-block;
}
.result-box {
    padding:20px;
    border-radius:10px;
    background-color:white;
    border:2px solid #ddd;
}
.pass {
    color:green;
    font-weight:bold;
}
.fail {
    color:red;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ------------------- HEADER -------------------
st.markdown(
    '<div class="header">Central Board of Secondary Education</div>',
    unsafe_allow_html=True
)

# ------------------- EXCEL FILE -------------------
EXCEL_FILE = "searched_results.xlsx"

# ------------------- SUBJECTS -------------------
subjects = [
    "English Core",
    "Physics",
    "Chemistry",
    "Mathematics",
    "Computer Science"
]

# ------------------- CAPTCHA -------------------
def generate_captcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def normalize_dob(dob):
    return dob.replace(".", "/").replace("-", "/").strip()

# ------------------- RANDOM RESULT -------------------
def generate_result():

    marks_data = []

    overall_pass = True
    total = 0

    for sub in subjects:

        theory = random.randint(20, 70)
        practical = random.randint(15, 30)

        obtained = theory + practical

        status = "PASS"

        if obtained < 33:
            status = "FAIL"
            overall_pass = False

        total += obtained

        marks_data.append({
            "Subject": sub,
            "Theory": theory,
            "Practical": practical,
            "Total": obtained,
            "Status": status
        })

    percentage = round(total / 5, 2)

    final_status = "PASS" if overall_pass else "FAIL"

    return marks_data, total, percentage, final_status

# ------------------- SAVE TO EXCEL -------------------
def save_to_excel(roll, school, admit, dob, percentage, final_status):

    data = {
        "Roll Number": [roll],
        "School Number": [school],
        "Admit Card ID": [admit],
        "DOB": [dob],
        "Percentage": [percentage],
        "Result": [final_status],
        "Search Time": [datetime.now().strftime("%d-%m-%Y %H:%M:%S")]
    }

    df_new = pd.DataFrame(data)

    if os.path.exists(EXCEL_FILE):
        df_old = pd.read_excel(EXCEL_FILE)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new

    df_final.to_excel(EXCEL_FILE, index=False)

# ------------------- SESSION STATE -------------------
if "captcha" not in st.session_state:
    st.session_state.captcha = generate_captcha()

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "result_data" not in st.session_state:
    st.session_state.result_data = None

# ------------------- RESULT PAGE -------------------
if st.session_state.submitted:

    marks_data, total, percentage, final_status = st.session_state.result_data

    st.markdown(
        '<div class="title">Senior School Certificate Examination (Class XII) Results 2025</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="result-box">', unsafe_allow_html=True)

    st.write("### Candidate Details")
    st.write("**Name :** Candidate")
    st.write("**Roll Number :**", st.session_state.roll)
    st.write("**School Number :**", st.session_state.school)

    st.write("---")

    st.write("### Marks Statement")

    table_data = []

    for item in marks_data:
        table_data.append({
            "Subject": item["Subject"],
            "Theory": item["Theory"],
            "Practical": item["Practical"],
            "Total": item["Total"],
            "Result": item["Status"]
        })

    df = pd.DataFrame(table_data)

    st.table(df)

    st.write("---")

    st.write(f"### Total Marks : {total} / 500")
    st.write(f"### Percentage : {percentage}%")

    if final_status == "PASS":
        st.markdown(
            '<h2 class="pass">RESULT : PASS ✅</h2>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<h2 class="fail">RESULT : FAIL ❌</h2>',
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔙 Search Another Result"):
        st.session_state.submitted = False
        st.session_state.captcha = generate_captcha()
        st.rerun()

# ------------------- FORM PAGE -------------------
else:

    st.markdown(
        '<div class="title">Senior School Certificate Examination (Class XII) Results 2025</div>',
        unsafe_allow_html=True
    )

    with st.container():

        st.markdown('<div class="box">', unsafe_allow_html=True)

        roll = st.text_input("Your Roll Number")
        school = st.text_input("Your School Number")
        admit = st.text_input("Admit Card ID")
        dob = st.text_input("Date of Birth (DD/MM/YYYY)")
        pin_input = st.text_input("Enter Security Pin (case sensitive)")

        col1, col2 = st.columns([1, 4])

        with col1:
            st.markdown(
                f'<div class="captcha">{st.session_state.captcha}</div>',
                unsafe_allow_html=True
            )

        with col2:
            if st.button("🔄 Refresh"):
                st.session_state.captcha = generate_captcha()

        col3, col4 = st.columns(2)

        with col3:
            submit = st.button("Submit")

        with col4:
            reset = st.button("Reset")

        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------- VALIDATION -------------------
    if submit:

        dob_clean = normalize_dob(dob)

        if (
            roll.strip() != "" and
            school.strip() != "" and
            admit.strip() != "" and
            dob_clean != "" and
            pin_input.strip() == st.session_state.captcha
        ):

            # Generate random marks
            result_data = generate_result()

            # Save in session
            st.session_state.result_data = result_data

            # Save student details
            st.session_state.roll = roll
            st.session_state.school = school

            # Save to Excel
            save_to_excel(
                roll,
                school,
                admit,
                dob_clean,
                result_data[2],
                result_data[3]
            )

            st.session_state.submitted = True
            st.rerun()

        else:
            st.error("❌ Please fill all details correctly and enter valid captcha.")

    if reset:
        st.session_state.captcha = generate_captcha()
        st.rerun()

# ------------------- DISCLAIMER -------------------
st.markdown("""
---
**Disclaimer:** Neither NIC nor CBSE is responsible for any inadvertent
error that may have crept in the results being published on Net.
The results published on net are for immediate information to the examinees.
These cannot be treated as original mark sheets.
""")
