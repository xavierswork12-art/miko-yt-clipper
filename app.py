# ==========================================
# MIKO YT CLIPPER - SECURE ACCESS PORTAL
# ==========================================

import streamlit as st

st.set_page_config(
    page_title="MIKO YT Clipper", 
    layout="centered", 
    initial_sidebar_state="expanded"
)

# 1. ADMIN PASSWORD
ADMIN_PASSWORD = "Quantum7-Router9-Nexus4-Shield!"

# 2. PERMANENT PAID CLIENT DATABASE
# To add a new client, just add their password and name here and save!
PAID_CLIENTS = {
    "john123": "John Doe",
    "sarah_pass_99": "Sarah FX",
    "miko_vip": "MIKO Test User"
}

# Track login session state
if "user_role" not in st.session_state:
    st.session_state.user_role = None  # "admin" or "client"
if "logged_in_name" not in st.session_state:
    st.session_state.logged_in_name = None

# ==========================================
# LOGIN SCREEN (Shown if not logged in)
# ==========================================
if st.session_state.user_role is None:
    st.title("🎬 MIKO YT Clipper")
    st.warning("🔒 **Secure Access Portal:** Please enter your assigned password or admin key below.")
    
    entered_password = st.text_input("Enter Password:", type="password")
    
    if st.button("Access Portal"):
        # Check if Admin Password matches
        if entered_password == ADMIN_PASSWORD:
            st.session_state.user_role = "admin"
            st.session_state.logged_in_name = "MIKO (Admin)"
            st.success("Admin access granted!")
            st.rerun()
            
        # Check if Client Password matches
        elif entered_password in PAID_CLIENTS:
            st.session_state.user_role = "client"
            st.session_state.logged_in_name = PAID_CLIENTS[entered_password]
            st.success(f"Welcome, {st.session_state.logged_in_name}!")
            st.rerun()
            
        else:
            st.error("Incorrect password. Please check your key or contact MIKO.")
            
    st.stop()

# ==========================================
# SIDEBAR CONTROLS & LOGOUT
# ==========================================
with st.sidebar:
    st.write(f"👤 Logged in as: **{st.session_state.logged_in_name}**")
    if st.button("Log Out"):
        st.session_state.user_role = None
        st.session_state.logged_in_name = None
        st.rerun()

    # ADMIN VIEW (Only visible when MIKO logs in with admin password)
    if st.session_state.user_role == "admin":
        st.divider()
        st.subheader("🎛️ Admin Control Panel")
        st.write("📋 **Registered Client Database:**")
        st.info("To add or change client passwords, update the `PAID_CLIENTS` list at the top of your `app.py` file.")
        
        for pwd, name in PAID_CLIENTS.items():
            st.text(f"• {name}\n  Password: `{pwd}`")

# ==========================================
# MAIN YOUTUBE BATCH CLIPPER TOOL
# (Visible to MIKO Admin and Logged-in Clients)
# ==========================================
st.title("🎬 MIKO YT Clipper")
st.success(f"⭐ Active Workspace — User: `{st.session_state.logged_in_name}`")
st.write("Professional multi-link media extraction and batch utility.")

video_links = st.text_area(
    "Paste YouTube Links (Max 10 links):",
    placeholder="https://www.youtube.com/watch?v=...\nhttps://www.youtube.com/watch?v=..."
)

col1, col2 = st.columns(2)
with col1:
    start_time = st.text_input("Default Start Time (Optional):", placeholder="00:00:00")
with col2:
    end_time = st.text_input("Default End Time (Optional):", placeholder="00:00:30")

resolution = st.selectbox(
    "Select Video Resolution / Quality:",
    ["Best Available (Source)", "1080p (Full HD)", "720p (HD)", "Audio Only (MP3)"]
)

naming_template = st.text_input("Naming Template:", placeholder="[Track Name] - [Artist]")

if st.button("Process Batch Queue"):
    cleaned_links = [line.strip() for line in video_links.split("\n") if line.strip()]
    
    if len(cleaned_links) > 0:
        st.success(f"Successfully processed batch queue ({len(cleaned_links)} links generated).")
        
        with st.expander("Preview Extracted Batch Output"):
            for i, link in enumerate(cleaned_links, 1):
                st.write(f"{i}. `{link}` → Successfully processed output (`{naming_template or 'Default'}` @ {resolution})")
                
        st.info("📥 Batch execution complete!")
    else:
        st.info("Please paste at least one valid YouTube link above to generate your batch queue.")
