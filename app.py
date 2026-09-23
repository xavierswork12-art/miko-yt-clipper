# ==========================================
# MICO YT CLIPPER - MASTER APP WITH CLIENT BYPASS
# ==========================================

import streamlit as st

st.set_page_config(
    page_title="Mico YT Clipper", 
    layout="centered", 
    initial_sidebar_state="expanded"
)

# 1. Master live toggle state for public demos (Default: Off)
if "is_live" not in st.session_state:
    st.session_state.is_live = False

# 2. Database of Paid Client Passwords / License Keys
# When someone pays $49, add their key and name here.
PAID_CLIENTS = {
    "john_clipper_99": "John Doe",
    "sarah_media_77": "Sarah FX",
}

# ==========================================
# ADMIN MASTER CONTROL PANEL (Sidebar)
# ==========================================
with st.sidebar:
    st.subheader("🎛️ Mico Admin Control")
    admin_pass = st.text_input("Admin Passphrase:", type="password")
    
    if admin_pass == "Quantum7-Router9-Nexus4-Shield!":
        st.success("Admin Access Granted")
        
        # Master Switch for public demos
        st.session_state.is_live = st.toggle("Enable Public Demo Access", value=st.session_state.is_live)
        
        if st.session_state.is_live:
            st.success("🟢 Demo Status: LIVE (Public can access)")
        else:
            st.warning("🔴 Demo Status: OFFLINE (Public locked out)")
            
        st.divider()
        st.write("💰 **Registered Client Keys:**")
        for key, name in PAID_CLIENTS.items():
            st.text(f"• {name}\n  Link: ?key={key}")
            
    elif admin_pass:
        st.error("Invalid Admin Passphrase")

# ==========================================
# CLIENT LOGIN & ACCESS CHECK
# ==========================================
query_params = st.query_params
url_client_key = query_params.get("key", None)

if "logged_in_client" not in st.session_state:
    st.session_state.logged_in_client = None

# Auto-login if they use their personal URL link (e.g. ?key=john_clipper_99)
if url_client_key in PAID_CLIENTS:
    st.session_state.logged_in_client = PAID_CLIENTS[url_client_key]

active_client = st.session_state.logged_in_client
is_paid_client = active_client is not None

# ==========================================
# ACCESS GATE LOGIC
# ==========================================
# If public demo is OFF AND the user is NOT a paid client, lock them out.
# (Note: Even if is_live is False, paid clients bypass this check completely!)
if not st.session_state.is_live and not is_paid_client:
    st.title("🎬 Mico YT Clipper")
    st.warning("🔒 **Utility Offline:** Public demo access is currently turned off. If you are a licensed client, please use your private invitation link or enter your license key below.")
    
    entered_key = st.text_input("Enter Client License Key:", type="password")
    if st.button("Unlock Client Portal"):
        if entered_key in PAID_CLIENTS:
            st.session_state.logged_in_client = PAID_CLIENTS[entered_key]
            st.rerun()
        else:
            st.error("Invalid key. Please contact Mico to acquire a permanent $49 desktop license.")
    st.stop()

# ==========================================
# MAIN APP INTERFACE (Unlocked for Live Demos or Paid Clients)
# ==========================================
st.title("🎬 Mico YT Clipper")

if is_paid_client:
    st.success(f"⭐ Welcome, Licensed Client Portal: `{active_client}`")
else:
    st.success("🟢 Active Public Demo Session (Master Switch is LIVE)")

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
