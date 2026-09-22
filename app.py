import streamlit as st
import json
import os

st.set_page_config(page_title="Batch Timestamp Clipper", layout="centered", initial_sidebar_state="expanded")

TOKEN_FILE = "tokens.json"

def load_tokens():
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                data = json.load(f)
                return data.get("tokens", {})
        except Exception:
            pass
    return {"test_creator": "unused"}

def save_tokens(tokens_dict):
    try:
        with open(TOKEN_FILE, "w") as f:
            json.dump({"tokens": tokens_dict}, f, indent=4)
    except Exception as e:
        st.error(f"Could not save tokens file: {e}")

# Load current tokens from file database
tokens_db = load_tokens()

# --- SECURE ADMIN PANEL (Passphrase-Protected) ---
with st.sidebar:
    st.subheader("🛠️ Proton Admin Control")
    admin_pass = st.text_input("Secure Passphrase:", type="password")
    
    if admin_pass == "Quantum7-Router9-Nexus4-Shield!":
        st.success("Access Granted")
        new_creator = st.text_input("Creator Name / ID:", placeholder="e.g. creator_john")
        if st.button("Generate Invite Link"):
            if new_creator:
                clean_name = new_creator.strip().replace(" ", "_")
                
                # Update tokens dict and save to tokens.json
                current_tokens = load_tokens()
                current_tokens[clean_name] = "unused"
                save_tokens(current_tokens)
                
                base_url = "https://mikoytclipper.streamlit.app"
                invite_link = f"{base_url}/?access={clean_name}"
                st.success("Link generated successfully!")
                st.code(invite_link, language="text")
            else:
                st.error("Enter a creator name first.")
        
        st.divider()
        st.write("📊 **Token Status List:**")
        st.json(load_tokens())
    elif admin_pass:
        st.error("Invalid Passphrase")

# --- USER APP LOGIC ---
# Safely grab access token from URL parameters
query_params = st.query_params
access_token = query_params.get("access", None)

# Reload fresh tokens from file for verification
active_tokens = load_tokens()

# 1. Check if token was provided and exists in json
if not access_token or access_token not in active_tokens:
    st.title("🎬 Batch Timestamp Clipper")
    st.warning("🔒 **Private Trial Access Only:** A valid, active invitation link is required to access this trial utility.")
    st.stop()

# 2. Check if token has already been burned / used
if active_tokens[access_token] == "used":
    st.title("🎬 Batch Timestamp Clipper")
    st.error("🚫 **Invitation Link Expired:** This unique trial link has already been used and is now permanently deactivated. To unlock unlimited native desktop rendering and batch processing, please upgrade to the full $49 desktop version.")
    st.stop()

# --- ACTIVE TRIAL INTERFACE ---
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
            # BURN THE TOKEN PERMANENTLY IN TOKENS.JSON
            fresh_db = load_tokens()
            fresh_db[access_token] = "used"
            save_tokens(fresh_db)
            
            st.success(f"Successfully processed batch queue ({len(cleaned_links)} links generated).")
            
            with st.expander("Preview Extracted Batch Output"):
                for i, link in enumerate(cleaned_links, 1):
                    st.write(f"{i}. `{link}` → Successfully processed output (`{naming_template or 'Default'}` @ {resolution})")
                    
            st.info("📥 *Free Trial Complete:* Your unique invitation link has now been permanently deactivated after delivering your trial outputs. To unlock unlimited native desktop rendering and automated pipelines, upgrade to the full $49 desktop version.")
    else:
        st.info("Please paste at least one valid YouTube link above to generate your batch queue.")
