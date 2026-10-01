import streamlit as st
import pandas as pd
import json
import os
from PIL import Image

# Set Streamlit Page Config
st.set_page_config(
    page_title="Pakistan Navy Polytechnic Institute (PNPI) - Examination Portal",
    page_icon="🎓",
    layout="wide"
)

# ---------------------------------------------------------
# CONSTANTS & CONFIGURATION
# ---------------------------------------------------------
DATA_FILE = "students.json"
SETTINGS_FILE = "settings.json"
LOGO_FILE = "logo.png"

TECHNOLOGIES = [
    "Electrical Technology",
    "Electronics Technology",
    "Mechatronics Technology",
    "Mechanical Technology",
    "Ship Construction Technology"
]

DEFAULT_SUBJECTS = {
    "Electrical Technology": ["Electrical Circuits", "Power Electronics", "AC Machines", "Electrical Instruments", "Industrial Automation"],
    "Electronics Technology": ["Basic Electronics", "Digital Systems", "Microcontrollers", "Communication Systems", "Circuit Design"],
    "Mechatronics Technology": ["Robotics & Automation", "Sensors & Actuators", "PLCs & Control Systems", "Embedded Systems", "CAD/CAM"],
    "Mechanical Technology": ["Thermodynamics", "Fluid Mechanics", "Engineering Drawing", "Manufacturing Processes", "Mechanics of Materials"],
    "Ship Construction Technology": ["Naval Architecture", "Ship Stability", "Shipbuilding Materials", "Marine Engineering", "Ship Systems"]
}

DEFAULT_SETTINGS = {
    "portal_active": True,
    "theme": "Navy Blue Official"
}

# ---------------------------------------------------------
# HELPER FUNCTIONS FOR DATA MANAGEMENT
# ---------------------------------------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            try:
                return json.load(f)
            except Exception:
                return DEFAULT_SETTINGS
    return DEFAULT_SETTINGS

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def calculate_grade_and_status(percentage):
    if percentage >= 80:
        return "A-1 (Excellent)", "PASS"
    elif percentage >= 70:
        return "A (Very Good)", "PASS"
    elif percentage >= 60:
        return "B (Good)", "PASS"
    elif percentage >= 50:
        return "C (Fair)", "PASS"
    elif percentage >= 40:
        return "D (Satisfactory)", "PASS"
    else:
        return "F (Fail)", "FAIL"

# Load initial state
students_data = load_data()
settings = load_settings()

# ---------------------------------------------------------
# CUSTOM THEME STYLING
# ---------------------------------------------------------
current_theme = settings.get("theme", "Navy Blue Official")

if current_theme == "Navy Blue Official":
    primary_color = "#002147"
    accent_color = "#0056b3"
    bg_gradient = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
elif current_theme == "Emerald Green Academic":
    primary_color = "#0f5132"
    accent_color = "#198754"
    bg_gradient = "linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)"
else:  # Dark Modern Slate
    primary_color = "#1e293b"
    accent_color = "#0f172a"
    bg_gradient = "linear-gradient(135deg, #e2e8f0 0%, #94a3b8 100%)"

st.markdown(f"""
<style>
    .main-header {{
        background-color: {primary_color};
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
    }}
    .main-header h1 {{
        color: #ffffff !important;
        font-family: 'Arial', sans-serif;
        font-weight: 700;
        margin-bottom: 5px;
    }}
    .main-header h3 {{
        color: #e2e8f0 !important;
        font-weight: 400;
        margin-top: 0px;
    }}
    .sub-title {{
        color: #f8fafc !important;
        font-size: 16px;
    }}
    .card {{
        background-color: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border-left: 5px solid {primary_color};
    }}
    .result-badge-pass {{
        background-color: #d1e7dd;
        color: #0f5132;
        font-weight: bold;
        padding: 6px 16px;
        border-radius: 20px;
        display: inline-block;
    }}
    .result-badge-fail {{
        background-color: #f8d7da;
        color: #842029;
        font-weight: bold;
        padding: 6px 16px;
        border-radius: 20px;
        display: inline-block;
    }}
    .footer {{
        text-align: center;
        padding: 20px;
        font-size: 14px;
        color: #64748b;
        margin-top: 40px;
        border-top: 1px solid #e2e8f0;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR NAVIGATION & LOGO
# ---------------------------------------------------------
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        try:
            logo_img = Image.open(LOGO_FILE)
            st.image(logo_img, use_container_width=True)
        except Exception:
            pass
    
    st.title("Navigation Menu")
    nav_option = st.radio("Select Portal Area:", ["Public Result Search", "Administrative Portal"])
    
    st.markdown("---")
    st.info("PNPI Examination Automation System v2.0")

# ---------------------------------------------------------
# HEADER SECTION
# ---------------------------------------------------------
st.markdown(f"""
<div class="main-header">
    <h1>PAKISTAN NAVY POLYTECHNIC INSTITUTE</h1>
    <h3>Board of Technical Examinations & Assessment</h3>
    <p class="sub-title">Official Online Result Portal & Academic Transcript System</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 1: PUBLIC RESULT SEARCH
# ---------------------------------------------------------
if nav_option == "Public Result Search":
    st.subheader("🔍 Student Result Verification")
    
    if not settings.get("portal_active", True):
        st.warning("⚠️ The Result Portal is currently offline for maintenance or official processing. Please check back later.")
    else:
        search_tab1, search_tab2 = st.tabs(["Search by Roll / Reg No.", "Search by Student Name"])
        
        found_student = None
        
        # Search Option 1: Roll No
        with search_tab1:
            with st.form("search_roll_form"):
                query_roll = st.text_input("Enter Roll Number / Registration Number:", placeholder="e.g., PNPI-2024-101")
                btn_roll = st.form_submit_button("Search Result")
                if btn_roll and query_roll:
                    for s in students_data:
                        if str(s.get("roll_no", "")).strip().lower() == query_roll.strip().lower():
                            found_student = s
                            break
                    if not found_student:
                        st.error("No record found matching the provided Roll / Registration Number.")
        
        # Search Option 2: Student Name
        with search_tab2:
            with st.form("search_name_form"):
                query_name = st.text_input("Enter Candidate Full Name:", placeholder="e.g., Muhammad Ali")
                btn_name = st.form_submit_button("Search Candidates")
                if btn_name and query_name:
                    matches = [s for s in students_data if query_name.strip().lower() in s.get("name", "").strip().lower()]
                    if len(matches) == 1:
                        found_student = matches[0]
                    elif len(matches) > 1:
                        st.info(f"Multiple candidates found ({len(matches)}). Please select from below:")
                        selected_roll = st.selectbox("Select Candidate:", [f"{s['name']} (Roll: {s['roll_no']})" for s in matches])
                        sel_roll_no = selected_roll.split("(Roll: ")[1].replace(")", "")
                        for s in matches:
                            if s["roll_no"] == sel_roll_no:
                                found_student = s
                                break
                    else:
                        st.error("No candidate found matching the entered name.")

        # DISPLAY MARKSHEET / RESULT
        if found_student:
            st.markdown("---")
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"### **PROVISIONAL RESULT CARD**")
                st.write(f"**Candidate Name:** {found_student.get('name')}")
                st.write(f"**Father's Name:** {found_student.get('father_name')}")
                st.write(f"**Roll Number:** {found_student.get('roll_no')}")
                st.write(f"**Technology:** {found_student.get('technology')}")
                st.write(f"**Session / Year:** {found_student.get('session')}")
            
            # Subject Breakdown Table
            subjects = found_student.get("subjects", {})
            total_max = 0
            total_obt = 0
            
            table_data = []
            for sub_name, marks in subjects.items():
                max_m = marks.get("max_marks", 100)
                obt_m = marks.get("obtained_marks", 0)
                total_max += max_m
                total_obt += obt_m
                
                sub_status = "Pass" if obt_m >= (max_m * 0.4) else "Fail"
                table_data.append({
                    "Subject Title": sub_name,
                    "Total Marks": max_m,
                    "Obtained Marks": obt_m,
                    "Status": sub_status
                })
            
            percentage = (total_obt / total_max * 100) if total_max > 0 else 0
            grade, overall_status = calculate_grade_and_status(percentage)
            
            with c2:
                st.markdown("#### **Overall Status**")
                if overall_status == "PASS":
                    st.markdown(f'<div class="result-badge-pass">STATUS: {overall_status}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="result-badge-fail">STATUS: {overall_status}</div>', unsafe_allow_html=True)
                
                st.metric("Total Obtained", f"{total_obt} / {total_max}")
                st.metric("Percentage", f"{percentage:.2f}%")
                st.metric("Grade", grade)

            st.markdown("---")
            st.markdown("#### **Detailed Marks Distribution**")
            df_marks = pd.DataFrame(table_data)
            st.dataframe(df_marks, use_container_width=True, hide_index=True)
            
            st.caption("Note: This provisional transcript is computer-generated and does not require a manual signature. Official certificates will be issued separately.")
            st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 2: ADMINISTRATIVE PORTAL
# ---------------------------------------------------------
elif nav_option == "Administrative Portal":
    st.subheader("🔒 Administrative Control Panel")
    
    # Simple Admin Authentication
    admin_user = st.text_input("Admin Username:", type="default")
    admin_pass = st.text_input("Admin Password:", type="password")
    
    if admin_user == "admin" and admin_pass == "PNPI@123":
        st.success("Authentication Successful! Welcome, Administrator.")
        
        admin_tab1, admin_tab2, admin_tab3 = st.tabs(["System & Portal Controls", "Add New Student Record", "Manage Existing Records"])
        
        # TAB 1: PORTAL CONTROLS & THEME SWITCHER
        with admin_tab1:
            st.markdown("### **Portal Configuration & Status**")
            
            col_a, col_b = st.columns(2)
            with col_a:
                portal_status = st.toggle("Public Result Portal Active", value=settings.get("portal_active", True))
            
            with col_b:
                selected_theme = st.selectbox("Select Official UI Theme:", ["Navy Blue Official", "Emerald Green Academic", "Dark Modern Slate"], index=["Navy Blue Official", "Emerald Green Academic", "Dark Modern Slate"].index(settings.get("theme", "Navy Blue Official")))
            
            if st.button("Save Configuration Changes"):
                settings["portal_active"] = portal_status
                settings["theme"] = selected_theme
                save_settings(settings)
                st.success("System configurations updated successfully! Please refresh to view changes.")
        
        # TAB 2: ADD NEW STUDENT
        with admin_tab2:
            st.markdown("### **Enroll Candidate & Add Examination Marks**")
            
            with st.form("add_student_form"):
                f_name = st.text_input("Candidate Full Name:")
                f_father = st.text_input("Father's Name:")
                f_roll = st.text_input("Roll / Registration Number:")
                f_session = st.selectbox("Academic Session:", ["2023-2026", "2024-2027", "2025-2028"])
                f_tech = st.selectbox("Technology / Field:", TECHNOLOGIES)
                
                st.markdown("#### **Enter Marks for Subjects**")
                tech_subjects = DEFAULT_SUBJECTS[f_tech]
                
                subj_marks_input = {}
                cols = st.columns(len(tech_subjects))
                for idx, subj in enumerate(tech_subjects):
                    with cols[idx % len(cols)]:
                        st.markdown(f"**{subj}**")
                        max_m = st.number_input(f"Max Marks ({subj}):", min_value=1, max_value=200, value=100, key=f"max_{idx}")
                        obt_m = st.number_input(f"Obtained ({subj}):", min_value=0, max_value=200, value=0, key=f"obt_{idx}")
                        subj_marks_input[subj] = {"max_marks": max_m, "obtained_marks": obt_m}
                
                submit_student = st.form_submit_button("Save Student Record")
                
                if submit_student:
                    if not f_name or not f_roll:
                        st.error("Student Name and Roll Number are required fields.")
                    else:
                        new_record = {
                            "roll_no": f_roll,
                            "name": f_name,
                            "father_name": f_father,
                            "session": f_session,
                            "technology": f_tech,
                            "subjects": subj_marks_input
                        }
                        students_data.append(new_record)
                        save_data(students_data)
                        st.success(f"Record for {f_name} ({f_roll}) created successfully!")

        # TAB 3: MANAGE RECORDS
        with admin_tab3:
            st.markdown("### **Registered Students Database**")
            if students_data:
                df_all = pd.DataFrame(students_data)
                st.dataframe(df_all[["roll_no", "name", "father_name", "technology", "session"]], use_container_width=True)
                
                roll_to_delete = st.selectbox("Select Roll No to Delete Record:", [s["roll_no"] for s in students_data])
                if st.button("Delete Record"):
                    students_data = [s for s in students_data if s["roll_no"] != roll_to_delete]
                    save_data(students_data)
                    st.success(f"Record {roll_to_delete} deleted successfully.")
                    st.rerun()
            else:
                st.info("No student records available in database.")
    elif admin_pass or admin_user:
        st.error("Invalid Username or Password.")

# ---------------------------------------------------------
# FOOTER SECTION
# ---------------------------------------------------------
st.markdown("""
<div class="footer">
    <p>© 2026 Pakistan Navy Polytechnic Institute (PNPI). All Rights Reserved.</p>
    <p>Prepared by Muhammad Farooq | System Administrator</p>
</div>
""", unsafe_allow_html=True)