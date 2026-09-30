import streamlit as st
import pandas as pd
import os
import base64

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="PNPI Apprentices Result Portal",
    page_icon="🎓",
    layout="centered"
)

RESULT_FILE = "results.csv"
LOGO_FILE = "logo.png"

# Admin credentials setup
try:
    ADMIN_USERNAME = st.secrets["ADMIN_USERNAME"]
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
except:
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "PNPI@123"


# Helper function to convert local image to base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

logo_base64 = get_base64_image(LOGO_FILE)
logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="header-logo">' if logo_base64 else ''


# ==========================================
# DATABASE FUNCTIONS
# ==========================================

def load_results():
    if not os.path.exists(RESULT_FILE):
        df = pd.DataFrame(
            columns=[
                "p_no",
                "name",
                "trade",
                "marks",
                "status"
            ]
        )
        df.to_csv(
            RESULT_FILE,
            index=False
        )
    return pd.read_csv(RESULT_FILE)


def save_results(df):
    df.to_csv(
        RESULT_FILE,
        index=False
    )


# ==========================================
# CUSTOM NAVY BLUE CSS THEME
# ==========================================

st.markdown("""
<style>

/* App Background */
.stApp {
    background: #eef2f6;
}

/* Header Styling */
.header-container {
    background: linear-gradient(135deg, #0a192f, #1e3a8a);
    color: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}

.header-container h1 {
    margin: 0;
    font-size: 24px;
    color: #ffffff;
    font-weight: 700;
}

.header-container p {
    margin: 4px 0 0 0;
    font-size: 14px;
    color: #cbd5e1;
}

/* Card Container */
.card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    border-top: 4px solid #1e3a8a;
    margin-bottom: 20px;
}

/* Marksheet Styling */
.marksheet {
    background: white;
    padding: 25px;
    border-radius: 10px;
    border: 2px solid #1e3a8a;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-top: 20px;
}

.result-header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 15px;
    margin-bottom: 20px;
}

.header-logo {
    height: 60px;
    width: auto;
    object-fit: contain;
}

.result-title {
    color: #0a192f;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
}

.result-subtitle {
    color: #475569;
    font-size: 13px;
    text-align: center;
}

/* Table Styling */
.info-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}

.info-table td {
    border: 1px solid #cbd5e1;
    padding: 10px 14px;
    font-size: 15px;
}

.info-label {
    background: #f1f5f9;
    font-weight: 600;
    color: #0a192f;
    width: 35%;
}

/* Status Badges */
.pass-status {
    background: #dcfce7;
    color: #15803d;
    padding: 10px;
    text-align: center;
    border-radius: 6px;
    font-size: 18px;
    font-weight: bold;
    margin-top: 15px;
}

.fail-status {
    background: #fee2e2;
    color: #b91c1c;
    padding: 10px;
    text-align: center;
    border-radius: 6px;
    font-size: 18px;
    font-weight: bold;
    margin-top: 15px;
}

/* Footer Styling */
.footer {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    margin-top: 40px;
    padding: 20px;
    border-top: 1px solid #e2e8f0;
}

.footer-credit {
    margin-top: 6px;
    font-weight: 600;
    color: #1e3a8a;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR (LOGO AT THE VERY TOP)
# ==========================================

if os.path.exists(LOGO_FILE):
    st.sidebar.image(LOGO_FILE, use_container_width=True)

st.sidebar.title("📌 Portal Menu")

page = st.sidebar.radio(
    "Select Page",
    [
        "Student Result",
        "Admin Panel"
    ]
)


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="header-container">
    <h1>PNPI Apprentices Result Portal</h1>
    <p>Apprenticeship Result Verification System</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# STUDENT RESULT
# ==========================================

if page == "Student Result":

    st.markdown("""
    <div class="card">
        <h3>🔎 Check Your Result</h3>
        <p>Enter your P.No to view your apprenticeship result.</p>
    </div>
    """, unsafe_allow_html=True)

    p_no = st.text_input(
        "Enter P.No",
        placeholder="Example: PNPI001",
        max_chars=30
    )

    if st.button(
        "🔍 Check Result",
        type="primary",
        use_container_width=True
    ):
        if not p_no.strip():
            st.warning("⚠️ Please enter your P.No.")
        else:
            df = load_results()

            result = df[
                df["p_no"]
                .astype(str)
                .str.strip()
                .str.upper()
                ==
                p_no.strip().upper()
            ]

            if result.empty:
                st.error("❌ Result not found. Please check your P.No.")
            else:
                student = result.iloc[0]
                status = str(student["status"]).strip().upper()

                st.success("✅ Result found successfully!")

                st.markdown(f"""
                <div class="marksheet">
                    <div class="result-header">
                        {logo_html}
                        <div>
                            <div class="result-title">PAKISTAN NAVY POLYTECHNIC INSTITUTE</div>
                            <div class="result-subtitle">OFFICIAL APPRENTICESHIP RESULT CARD</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown(
                    f"""
                    <table class="info-table">
                        <tr>
                            <td class="info-label">P.No</td>
                            <td>{student["p_no"]}</td>
                        </tr>
                        <tr>
                            <td class="info-label">Apprentice Name</td>
                            <td>{student["name"]}</td>
                        </tr>
                        <tr>
                            <td class="info-label">Trade</td>
                            <td>{student["trade"]}</td>
                        </tr>
                        <tr>
                            <td class="info-label">Marks Obtained</td>
                            <td><strong>{student["marks"]}</strong></td>
                        </tr>
                    </table>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if status == "PASS":
                    st.markdown(
                        '<div class="pass-status">🎉 PASS</div>',
                        unsafe_allow_html=True
                    )
                elif status == "FAIL":
                    st.markdown(
                        '<div class="fail-status">❌ FAIL</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.warning(f"Status: {student['status']}")

                st.divider()
                st.info("Result print/save karne ke liye browser ka Print option use karein.")


# ==========================================
# ADMIN PANEL
# ==========================================

elif page == "Admin Panel":

    st.subheader("🔐 Admin Panel")

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        st.info("Admin panel access ke liye login karein.")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button(
            "🔐 Login",
            type="primary",
            use_container_width=True
        ):
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Incorrect username or password.")

    else:
        st.success("🟢 Admin logged in")

        if st.button("🚪 Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

        df = load_results()
        st.divider()

        # Dashboard
        st.subheader("📊 Dashboard")
        total_students = len(df)
        pass_count = len(df[df["status"].astype(str).str.upper() == "PASS"]) if not df.empty else 0
        fail_count = len(df[df["status"].astype(str).str.upper() == "FAIL"]) if not df.empty else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total", total_students)
        with col2:
            st.metric("Pass", pass_count)
        with col3:
            st.metric("Fail", fail_count)

        st.divider()

        # Add Result
        st.subheader("➕ Add New Result")

        with st.form("add_result"):
            new_p_no = st.text_input("P.No")
            new_name = st.text_input("Name")
            new_trade = st.text_input("Trade")
            new_marks = st.number_input("Marks", min_value=0, max_value=100, value=0)
            new_status = st.selectbox("Status", ["Pass", "Fail"])

            add = st.form_submit_button("➕ Add Result", use_container_width=True)

            if add:
                if not new_p_no.strip():
                    st.error("P.No required hai.")
                elif not new_name.strip():
                    st.error("Name required hai.")
                else:
                    exists = df[df["p_no"].astype(str).str.upper() == new_p_no.strip().upper()] if not df.empty else []
                    if not exists.empty:
                        st.error("Ye P.No already exist karta hai.")
                    else:
                        new_row = pd.DataFrame([{
                            "p_no": new_p_no.strip(),
                            "name": new_name.strip(),
                            "trade": new_trade.strip(),
                            "marks": new_marks,
                            "status": new_status
                        }])
                        df = pd.concat([df, new_row], ignore_index=True)
                        save_results(df)
                        st.success("✅ Result added successfully.")
                        st.rerun()

        st.divider()

        # Edit Result
        st.subheader("✏️ Edit / Update Result")
        df = load_results()

        if df.empty:
            st.info("Edit karne ke liye koi result nahi.")
        else:
            edit_p_no = st.selectbox("Select P.No to Edit", df["p_no"].astype(str).tolist(), key="edit_select")
            selected = df[df["p_no"].astype(str) == edit_p_no]

            if not selected.empty:
                row_index = selected.index[0]
                current = df.loc[row_index]

                edit_name = st.text_input("Name", value=str(current["name"]), key="edit_name")
                edit_trade = st.text_input("Trade", value=str(current["trade"]), key="edit_trade")

                try:
                    current_marks = int(float(current["marks"]))
                except:
                    current_marks = 0

                edit_marks = st.number_input("Marks", min_value=0, max_value=100, value=current_marks, key="edit_marks")
                current_status = str(current["status"]).strip().title()

                if current_status not in ["Pass", "Fail"]:
                    current_status = "Pass"

                edit_status = st.selectbox(
                    "Status",
                    ["Pass", "Fail"],
                    index=["Pass", "Fail"].index(current_status),
                    key="edit_status"
                )

                if st.button("💾 Save Changes", type="primary", use_container_width=True):
                    df.loc[row_index, "name"] = edit_name.strip()
                    df.loc[row_index, "trade"] = edit_trade.strip()
                    df.loc[row_index, "marks"] = edit_marks
                    df.loc[row_index, "status"] = edit_status
                    save_results(df)
                    st.success("✅ Result updated successfully.")
                    st.rerun()

        st.divider()

        # Bulk Upload
        st.subheader("📤 Bulk CSV Upload")
        template = pd.DataFrame([{
            "p_no": "PNPI006",
            "name": "Test Student",
            "trade": "Electrical",
            "marks": 75,
            "status": "Pass"
        }])

        template_csv = template.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download CSV Template",
            data=template_csv,
            file_name="pnpi_results_template.csv",
            mime="text/csv",
            use_container_width=True
        )

        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file)
                required = ["p_no", "name", "trade", "marks", "status"]
                missing = [col for col in required if col not in uploaded_df.columns]

                if missing:
                    st.error("Missing columns: " + ", ".join(missing))
                else:
                    st.success("✅ CSV ready for import.")
                    st.dataframe(uploaded_df, use_container_width=True, hide_index=True)

                    if st.button("⬆️️ Import Results", type="primary", use_container_width=True):
                        uploaded_df = uploaded_df[required]
                        uploaded_df["p_no"] = uploaded_df["p_no"].astype(str).str.strip()
                        uploaded_df = uploaded_df.drop_duplicates(subset=["p_no"], keep="last")
                        save_results(uploaded_df)
                        st.success(f"🎉 {len(uploaded_df)} results imported.")
                        st.rerun()
            except Exception as e:
                st.error(f"❌ CSV Error: {e}")

        st.divider()

        # Current Database & Delete
        st.subheader("📋 Current Results")
        df = load_results()
        if df.empty:
            st.info("No results available.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()

        st.subheader("🗑️ Delete Result")
        df = load_results()
        if not df.empty:
            delete_p_no = st.selectbox("Select P.No", df["p_no"].astype(str).tolist(), key="delete_select")
            if st.button("🗑️ Delete Selected Result"):
                df = df[df["p_no"].astype(str) != delete_p_no]
                save_results(df)
                st.success("✅ Result deleted successfully.")
                st.rerun()

        st.divider()

        st.subheader("📥 Download Database")
        df = load_results()
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Current Results",
            data=csv_data,
            file_name="pnpi_results_backup.csv",
            mime="text/csv",
            use_container_width=True
        )

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">
    PNPI Apprentices Result Portal<br>
    © 2026 PNPI — All Rights Reserved<br>
    <div class="footer-credit">Prepared by Muhammad Farooq</div>
</div>
""", unsafe_allow_html=True)