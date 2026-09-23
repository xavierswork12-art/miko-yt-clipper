# ==========================================
# MIKO YT CLIPPER - STABLE STREAMLIT BUILD
# ==========================================

import streamlit as st
import yt_dlp
import os

st.set_page_config(
    page_title="MIKO YT Clipper", 
    layout="centered", 
    initial_sidebar_state="expanded"
)

# Custom Styling for white text and dark inputs
st.markdown("""
    <style>
    html, body, [class*="css"], .stMarkdown, p, label {
        color: #FFFFFF !important;
    }
    input, textarea, select {
        color: #FFFFFF !important;
        background-color: #1E1E1E !important;
    }
    </style>
""", unsafe_allow_html=True)

# 1. ADMIN PASSWORD
ADMIN_PASSWORD = "Quantum7-Router9-Nexus4-Shield!"

# 2. PERMANENT PAID CLIENT DATABASE
PAID_CLIENTS = {
    "john123": "John Doe",
    "sarah_pass_99": "Sarah FX",
    "miko_vip": "MIKO Test User"
}

# Session State Initialization
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "logged_in_name" not in st.session_state:
    st.session_state.logged_in_name = None

# ==========================================
# LOGIN SCREEN
# ==========================================
if st.session_state.user_role is None:
    st.title("🎬 MIKO YT Clipper")
    st.warning("🔒 **Secure Access Portal:** Please enter your assigned password or admin key below.")
    
    entered_password = st.text_input("Enter Password:", type="password")
    
    if st.button("Access Portal"):
        if entered_password == ADMIN_PASSWORD:
            st.session_state.user_role = "admin"
            st.session_state.logged_in_name = "MIKO (Admin)"
            st.rerun()
        elif entered_password in PAID_CLIENTS:
            st.session_state.user_role = "client"
            st.session_state.logged_in_name = PAID_CLIENTS[entered_password]
            st.rerun()
        else:
            st.error("Incorrect password. Please check your key or contact MIKO.")
    st.stop()

# ==========================================
# SIDEBAR NAVIGATION & ADMIN CONTROLS
# ==========================================
with st.sidebar:
    st.write(f"👤 Logged in as: **{st.session_state.logged_in_name}**")
    if st.button("Log Out"):
        st.session_state.user_role = None
        st.session_state.logged_in_name = None
        st.rerun()

    if st.session_state.user_role == "admin":
        st.divider()
        st.subheader("🎛️ Admin Control Panel")
        st.write("📋 **Registered Client Database:**")
        for pwd, name in PAID_CLIENTS.items():
            st.text(f"• {name}\n  Password: `{pwd}`")

# ==========================================
# MAIN APPLICATION INTERFACE
# ==========================================
st.title("🎬 MIKO YT Clipper")
st.success(f"⭐ Active Workspace — User: `{st.session_state.logged_in_name}`")
st.write("Extract and clip YouTube videos with per-link timestamps.")

st.info("💡 **Format per line:** `URL | START_TIME | END_TIME` (Example: `https://www.youtube.com/watch?v=dQw4w9WgXcQ | 00:00:10 | 00:00:25`)")

raw_input = st.text_area("Paste YouTube Links (Max 10 links):", height=150)

col1, col2 = st.columns(2)
with col1:
    resolution = st.selectbox(
        "Select Resolution / Format:",
        ["Best Video Quality (MP4)", "Audio Only (MP3/M4A)"]
    )
with col2:
    naming_template = st.text_input("Naming Template (Optional):", placeholder="[Track Name] - [Artist]")

# Helper function to convert time formats (HH:MM:SS, MM:SS, SS) to seconds
def parse_time_to_seconds(time_str):
    if not time_str:
        return None
    parts = time_str.strip().split(":")
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 1:
            return int(parts[0])
    except ValueError:
        return None
    return None

if st.button("Process & Generate Video Downloads"):
    lines = [line.strip() for line in raw_input.split("\n") if line.strip()]
    
    if not lines:
        st.warning("The input box is empty. Please paste at least one YouTube link.")
    elif len(lines) > 10:
        st.error(f"⚠️ Limit Exceeded: You submitted {len(lines)} links. The maximum allowed per batch is 10.")
    else:
        st.divider()
        st.subheader("📥 Processed Downloads")
        
        for idx, line in enumerate(lines, 1):
            parts = [p.strip() for p in line.split("|")]
            url = parts[0]
            start_str = parts[1] if len(parts) > 1 else None
            end_str = parts[2] if len(parts) > 2 else None
            
            start_sec = parse_time_to_seconds(start_str)
            end_sec = parse_time_to_seconds(end_str)
            
            st.markdown(f"### Video {idx}: `{url}`")
            if start_str or end_str:
                st.caption(f"⏱️ Trimming: `{start_str or '00:00:00'}` ➔ `{end_str or 'End'}` | Format: `{resolution}`")
            
            is_audio = "Audio" in resolution
            ext = "m4a" if is_audio else "mp4"
            output_filename = f"miko_clip_{idx}.{ext}"
            
            ydl_opts = {
                'format': 'bestaudio/best' if is_audio else 'bestvideo+bestaudio/best',
                'outtmpl': output_filename,
                'overwrites': True,
                'quiet': True,
                'no_warnings': True,
            }
            
            if start_sec is not None and end_sec is not None:
                ydl_opts['download_ranges'] = yt_dlp.utils.download_range_func(None, [(start_sec, end_sec)])
                ydl_opts['force_keyframes_at_cuts'] = True

            with st.spinner(f"Processing video {idx}..."):
                try:
                    if os.path.exists(output_filename):
                        os.remove(output_filename)
                        
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    
                    if os.path.exists(output_filename):
                        if not is_audio:
                            st.video(output_filename)
                        else:
                            st.audio(output_filename)
                        
                        file_title = f"{naming_template}_{idx}.{ext}" if naming_template else f"miko_clip_{idx}.{ext}"
                        
                        with open(output_filename, "rb") as file:
                            st.download_button(
                                label=f"📥 Download Clip #{idx}",
                                data=file,
                                file_name=file_title,
                                mime=f"audio/{ext}" if is_audio else f"video/{ext}",
                                key=f"dl_{idx}"
                            )
                        st.success(f"Video #{idx} ready for download!")
                    else:
                        st.error(f"Failed to generate clip file for Video #{idx}.")
                        
                except Exception as e:
                    st.error(f"Error processing video #{idx}: {str(e)}")
            st.divider()
