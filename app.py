import streamlit as st

st.set_page_config(page_title="Batch Timestamp Clipper", layout="centered")

st.title("🎬 Batch Timestamp Clipper")
st.write("Professional multi-link media extraction and batch utility.")

# Multiple YouTube Links Input
video_links = st.text_area(
    "Paste YouTube Links (One link per line for unlimited batch processing):",
    placeholder="https://www.youtube.com/watch?v=...\nhttps://www.youtube.com/watch?v=..."
)

col1, col2 = st.columns(2)
with col1:
    start_time = st.text_input("Default Start Time (Optional):", placeholder="00:00:00")
with col2:
    end_time = st.text_input("Default End Time (Optional):", placeholder="00:00:30")

# Resolution and Quality Selection
resolution = st.selectbox(
    "Select Video Resolution / Quality:",
    ["Best Available (Source)", "1080p (Full HD)", "720p (HD)", "Audio Only (MP3)"]
)

# Custom File Naming Template
naming_template = st.text_input("Naming Template:", placeholder="[Track Name] - [Artist]")

# Action Button
if st.button("Process Batch Queue"):
    if video_links:
        links_list = [line.strip() for line in video_links.split("\n") if line.strip()]
        st.success(f"Successfully queued {len(links_list)} links for batch processing!")
        
        with st.expander("View Queue Details"):
            for idx, link in enumerate(links_list, 1):
                st.write(f"{idx}. `{link}`")
                
        st.write(f"⚙️ **Resolution/Format:** {resolution}")
        st.write(f"📁 **Naming Template:** `{naming_template or 'Default_Output'}`")
        
        st.info("📥 *Trial Mode Active:* Unlimited local batch rendering, multi-threaded queues, and automated file renaming are unlocked in the full $49 desktop version.")
    else:
        # Replaced the harsh red error with a smooth, neutral notice
        st.warning("Please paste at least one video link above to start processing your batch queue.")
