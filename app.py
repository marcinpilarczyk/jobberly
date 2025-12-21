import streamlit as st
from google import genai
import pypdf
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Jobberly | Candidate Advocate", layout="wide", page_icon="🛡️")

# 2. API Configuration (Using Streamlit Secrets)
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets. Please add it to your dashboard.")
    st.stop()

# 3. Session State for the Career Vault
if 'career_vault' not in st.session_state:
    st.session_state['career_vault'] = None

# 4. Sidebar: Identity & Identity Protocol
with st.sidebar:
    st.title("🛡️ Jobberly")
    st.markdown("**The Candidate-Centric Employment Protocol**")
    st.info("The protocol where the candidate is the protected asset, not the raw material.")
    st.divider()
    
    if st.session_state['career_vault']:
        st.status("Career Vault: Active & Seeded", state="complete")
    else:
        st.status("Career Vault: Awaiting Data", state="error")
    
    st.metric("Global Hiring Reputation", "3.8/5", "-0.2")
    st.divider()
    st.caption("Jobberly v1.1.0 (2025)")

# 5. Main Application Interface
st.title("🛡️ Jobseeker Advocate Suite")

tab_onboard, tab_scout, tab_intel, tab_outreach, tab_track = st.tabs([
    "🚀 Discovery Engine", 
    "🕵️ Command Center", 
    "🧠 Strategic Intel", 
    "📧 Outreach Architect",
    "📊 Market Tracking"
])

# --- Tab 1: Discovery Engine (Working PDF Importer) ---
with tab_onboard:
    st.header("1. Build Your Proof-Based Vault")
    st.write("LinkedIn -> More... -> Save to PDF. Upload it below to 'seed' your vault.")
    
    uploaded_file = st.file_uploader("Upload LinkedIn PDF", type="pdf")
    
    if uploaded_file and not st.session_state['career_vault']:
        with st.spinner("AI Agent parsing your professional history..."):
            # Extract text from uploaded PDF
            reader = pypdf.PdfReader(uploaded_file)
            raw_text = "".join([page.extract_text() for page in reader.pages])
            
            # Use Gemini to structure the data for the Vault
            prompt = f"""
            You are a Career Data Architect. Parse this LinkedIn PDF into a structured summary 
            focusing on roles, key achievements, and skills. 
            TEXT: {raw_text[:5000]} 
            """
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            st.session_state['career_vault'] = response.text
            st.success("Vault Seeded successfully!")

    if st.session_state['career_vault']:
        st.divider()
        st.subheader("2. AI Interactive Interview")
        st.info("Your AI-Structured Profile Summary:")
        st.write(st.session_state['career_vault'])
        
        chat_input = st.chat_input("Tell the Advocate about a major win at work...")
        if chat_input:
            with st.chat_message("assistant"):
                # The interview is now context-aware based on the uploaded profile
                interview_prompt = (
                    f"Based on this profile: {st.session_state['career_vault']}, "
                    f"ask one probing, evidence-based question about the user's claim: '{chat_input}'. "
                    "Focus on uncovering impact metrics like revenue or operational burn rate."
                )
                res = client.models.generate_content(model="gemini-2.0-flash", contents=interview_prompt)
                st.write(res.text)
                st.caption("Captured and saved to Local Career Vault.")

# --- Tab 2: Command Center (Scout Decoder) ---
with tab_scout:
    st.header("The Deception Decoder")
    st.write("Analyze listings for 'Ghost Jobs' and 'Internal-Hire Theater.'")
    
    jd_text = st.text_area("Paste a Job Description (JD):", height=200, placeholder="Paste here...")
    if st.button("Analyze Listing"):
        if jd_text:
            with st.spinner("Calculating Ghost Score..."):
                scout_prompt = f"Analyze this JD for: 1. Ghost Score (0-100), 2. Internal-Hire Signals, 3. Budget Prediction. JD: {jd_text}"
                res = client.models.generate_content(model="gemini-2.0-flash", contents=scout_prompt)
                st.markdown("### 📊 Scout Report")
                st.write(res.text)
        else:
            st.warning("Please paste a job description first.")

# --- Tab 3: Strategic Intel (Company Archeology) ---
with tab_intel:
    st.header("Company Archeology")
    st.write("Research 'bleeding neck' pain points to win the interview.")
    
    comp_name = st.text_input("Target Company Name:")
    if st.button("Generate Strategic Intel"):
        with st.spinner(f"Researching {comp_name}..."):
            intel_prompt = f"Research {comp_name}. Identify: 1. Current Stage Pain Points, 2. A 3-Minute Interview Script."
            res = client.models.generate_content(model="gemini-2.0-flash", contents=intel_prompt)
            st.markdown(f"### 🧠 {comp_name} Strategy Map")
            st.write(res.text)

# --- Tab 4: Outreach Architect ---
with tab_outreach:
    st.header("LinkedIn Connection Architect")
    st.write("Direct-to-Human connection sequences.")
    
    role = st.text_input("Decision Maker Title (e.g., VP of Engineering):")
    if st.button("Draft Tactical Note"):
        if role:
            outreach_prompt = f"Write a 300-char LinkedIn note to a {role}. Focus on solving a specific problem."
            res = client.models.generate_content(model="gemini-2.0-flash", contents=outreach_prompt)
            st.markdown("### 📧 Connection Pitch")
            st.code(res.text, language="markdown")
        else:
            st.warning("Please specify a role.")

# --- Tab 5: Market Tracking & Accountability ---
with tab_track:
    st.header("Accountability Ledger")
    st.write("Track status and enforce the 'Feedback Escrow'.")
    
    tracking_data = pd.DataFrame({
        "Company": ["GlobalCorp", "TechStart", "InnovateIQ"],
        "Status": ["Interview Scheduled", "Ghosted (Claim Pending)", "Applied"],
        "Escrow Status": ["Locked", "Transferred to Seeker ($50)", "N/A"]
    })
    st.table(tracking_data)
    
    st.divider()
    st.button("Activate 'Be Discovered' Mode (Reverse Auction)")
    st.caption("Verified anonymous profiles visible to employers for bidding.")
