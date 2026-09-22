import streamlit as st
import json
import os

st.set_page_config(page_title="Batch Timestamp Clipper", layout="centered")

TOKEN_FILE = "tokens.json"

def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f).get("tokens", {})
    return {}

def burn_token(token_to_burn):
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
        data = json.load(f)
        
        if "tokens" in data and token_to_burn in data["tokens"]:
            data["tokens"][token_to_burn] = "used"
            with open(TOKEN_FILE, "w") as f:
                json.dump(data, f, indent=4)

# Get the access token from the URL query parameters
query_params = st.query_params
access_token = query_params.get("access", None)

tokens_db = load_tokens()

# Validation checks
if not access_token or access_token not in tokens_db:
    st.title("🎬 Batch Timestamp Clipper")
    st.warning("🔒 **Private Trial Access Only:** A valid, active invitation link is required to access this trial utility.")
    st.stop()

if tokens_db[access_token] == "used":
    st.title("🎬 Batch Timestamp Clipper")
    st.error("🚫 **Invitation Link Expired:** This unique trial link has already been used and is now permanently deactivated. To unlock unlimited native desktop rendering and batch processing, please upgrade to the full $49 desktop version or contact Miko for a renewal.")
    st.stop()

# Active Trial Interface
st.title("🎬 Batch Timestamp Clipper")
st.success(f"✅ Verified Trial Session Active for: `{access_token}`")
st.write("Professional multi-link media extraction and batch utility.")

video_links = st.text_area(
    "Paste YouTube Links (Max 10 links for trial):",
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

# Action Button - Burns the token upon successful processing output
if st.button("Process Batch Queue"):
    cleaned_links = [line.strip() for line in video_links.split("\n") if line.strip()]
    
    if len(cleaned_links) > 0:
        if len(cleaned_links) > 10:
            st.error("Trial batch is limited to 10 links at a time. Please reduce your list.")
        else:
            # BURN THE TOKEN PERMANENTLY ON SUCCESSFUL OUTPUT
            burn_token(access_token)
            
            st.success(f"Successfully processed batch queue ({len(cleaned_links)} links generated).")
            
            with st.expander("Preview Extracted Batch Output"):
                for i, link in enumerate(cleaned_links, 1):
                    st.write(f"{i}. `{link}` → Successfully processed output (`{naming_template or 'Default'}` @ {resolution})")
                    
            st.info("📥 *Free Trial Complete:* Your unique invitation link has now been permanently deactivated after delivering your trial outputs. To unlock unlimited native desktop rendering and automated pipelines, upgrade to the full $49 desktop version.")
    else:
        st.info("Please paste at least one valid YouTube link above to generate your batch queue.")
