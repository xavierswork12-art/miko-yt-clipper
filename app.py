import streamlit as st

st.title("Batch Timestamp Clipper - Free Trial")
st.write("Test out the high-speed video clipping utility below.")

video_link = st.text_input("Paste a public video link (YouTube, TikTok, etc.):")
timestamps = st.text_input("Enter timestamp (optional, e.g., 00:12 - 00:45):")

if st.button("Process Trial Clip"):
    if video_link:
        st.success("Success! (Trial simulation active). Ready for full version desktop license ($49).")
        st.info("To unlock full batch processing, multi-platform queues, and local desktop execution, contact Miko Xavier.")
    else:
        st.warning("Please paste a link first.")
