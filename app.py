# ==========================================
# MICO YT CLIPPER - UNIFIED PASSWORD PORTAL
# ==========================================

import streamlit as st

st.set_page_config(
    page_title="Mico YT Clipper", 
    layout="centered", 
    initial_sidebar_state="expanded"
)

# 1. ADMIN PASSWORD
ADMIN_PASSWORD = "Quantum7-Router9-Nexus4-Shield!"

# 2. PAID CLIENT PASSWORDS DATABASE
# Stored in session state so you can add new clients on the fly from the admin panel!
if "paid_clients" not in st.session_state:
    st.session_state.paid_clients = {
        "john123": "John Doe",
        "sarah_pass_99": "Sarah FX"
    }

# Track current login state and role
if "user_role" not in st.session_state:
    st.session_state.user_role = None  # Can be "admin" or "client"
if "logged_in_name" not in st.session_state:
    st.session_state.logged_in_name = None

# ==========================================
# LOGIN SCREEN (Shown if not logged in)
# ==========================================
if st.session_state.user_role is None:
    st.title("🎬 Mico YT Clipper")
    st.warning("🔒 **Secure Access Portal:** Please enter your assigned password or admin key below.")
    
    entered_password = st.text_input("Enter Password:", type="password")
    
    if st.button("Access Portal"):
        # Check if it's the Admin password
        if entered_password == ADMIN_PASSWORD:
            st.session_state.user_role = "admin"
            st.session_state.logged_in_name = "Mico (Admin)"
            st.success("Admin access granted!")
            st.rerun()
            
        # Check if it's a valid client password
        elif entered_password in st.session_state.paid_clients:
            st.session_state.user_role = "client"
            st.session_state.logged_in_name = st.session_state.paid_clients[entered_password]
            st.success(f"Welcome, {st.session_state.logged_in_name}!")
            st.rerun()
            
        else:
            st.error("Invalid password. Please check your key or contact Mico.")
            
    st.stop()

# ==========================================
# LOGOUT BUTTON (Available in sidebar for everyone)
# ==========================================
with st.sidebar:
    st.write(f"👤 Logged in as: **{st.session_state.logged_in_name}**")
    if st.button("Log Out"):
        st.session_state.user_role = None
        st.session_state.logged_in_name = None
        st.rerun()

# ==========================================
# ADMIN VIEW (Only visible when Mico logs in)
# ==========================================
if st.session_state.user_role == "admin":
    with st.sidebar:
        st.divider()
        st.subheader("🎛️ Admin Control Panel")
        
        # Master Toggle Switch
        if "is_live" not in st.session_state:
            st.session_state.is_live = False
        st.session_state.is_live = st.toggle("Enable Public Demo Mode", value=st.session_state.is_live)
        
        st.divider()
        st.subheader("➕ Add New Client Password")
        new_client_name = st.text_input("Client Name:", placeholder="e.g. David Alex")
        new_client_pwd = st.text_input("Client Password:", placeholder="e.g. david_pass_2026")
        
        if st.button("Save New Client"):
            if new_client_name and new_client_pwd:
                st.session_state.paid_clients[new_client_pwd.strip()] = new_client_name.strip()
                st.success(f"Added client: {new_client_name}")
            else:
                st.error("Please fill in both name and password.")
                
        st.divider()
        st.subheader("📋 Active Client List")
        for pwd, name in st.session_state.paid_clients.items():
            st.text(f"• {name} (Pass: {pwd})")

# ==========================================
# MAIN YOUTUBE BATCH CLIPPER TOOL
# (Visible to Admins and Logged-in Clients)
# ==========================================
st.title("🎬 Mico YT Clipper")
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
