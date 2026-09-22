import streamlit as st

st.set_page_config(page_title="Batch Timestamp Clipper", layout="centered")

st.title("🎬 Batch Timestamp Clipper")
st.write("Professional media extraction and custom-named clipping utility.")

# User Inputs
video_link = st.text_input("YouTube / Video Link:", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns(2)
with col1:
    start_time = st.text_input("Start Time:", placeholder="00:00:00")
with col2:
    end_time = st.text_input("End Time:", placeholder="00:00:30")

# Resolution and Quality Selection
resolution = st.selectbox(
    "Select Video Resolution / Quality:",
    ["Best Available (Source)", "1080p (Full HD)", "720p (HD)", "Audio Only (MP3)"]
)

# Custom File Naming
custom_name = st.text_input("Custom Output File Name:", placeholder="[Track Name] - [Artist]")

# Action Button
if st.button("Process & Generate Clip"):
    if video_link:
        st.success("Processing started successfully!")
        st.info(f"Target: `{video_link}`")
        st.write(f"⏱️ **Duration:** {start_time or 'Start'} to {end_time or 'End'}")
        st.write(f"⚙️ **Resolution/Format:** {resolution}")
        st.write(f"📁 **Naming Format:** `{custom_name or 'Default_Output'}`")
        
        st.warning("📥 *Trial Mode Active:* To unlock full native desktop batch rendering and automated local file saving, upgrade to the full $49 desktop version.")
    else:
        st.error("Please enter a valid video link to proceed.")
