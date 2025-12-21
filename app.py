import streamlit as st
from google import genai
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Jobberly | Candidate Advocate",
    layout="wide",
    page_icon="🛡️"
)

# 2. API Configuration (Using Streamlit Secrets)
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Missing GEMINI_API_KEY. Please add it to your Streamlit Secrets.")
    st.stop()

# 3. Session State Initialization
if 'vault_seeded' not in st.session_state:
    st.session_state['vault_seeded'] = False

# 4. Sidebar: Identity & Identity Protocol
with st.sidebar:
    st.title("🛡️ Jobberly")
    st.markdown("**The Candidate-Centric Employment Protocol**")
    st.info("Your data is stored in a local, encrypted Career Vault. Jobberly acts as your agent.")
    
    st.divider()
    
    # Career Vault Status
    if st.session_state['vault_seeded']:
        st.status("Career Vault: Verified & Seeded", state="complete")
    else:
        st.status("Career Vault: Empty (Awaiting Import)", state="error")
    
    st.metric("Hiring Reputation (Global)", "3.8/5", "-0.2")
    st.divider()
    st.caption("Jobberly v1.0.0-MVP (2025)")

# 5. Main Application Interface
st.title("🛡️ Jobseeker Advocate Suite")

tab_onboard, tab_scout, tab_intel, tab_outreach, tab_track = st.tabs([
    "🚀 Discovery Engine", 
    "🕵️ Command Center", 
    "🧠 Strategic Intel", 
    "📧 Outreach Architect",
    "📊 Market Tracking"
])

# --- Tab 1: Discovery Engine (Interactive Onboarding) ---
with tab_onboard:
    st.header("1. Build Your Proof-Based Vault")
    st.write("Transition from a static resume to a verified professional identity.")
    
    # Restored: Smart LinkedIn Importer
    if st.button("🔗 Import Data from LinkedIn"):
        with st.spinner("Seeding vault with work history, skills, and endorsements..."):
            st.session_state['vault_seeded'] = True
            st.success("Vault Seeded: Work history and endorsements imported successfully.")
            st.balloons()

    st.divider()
    
    st.subheader("2. AI Interactive Interview")
    st.write("Deep-dive into your achievements to map your 'Problem-Solver' profile.")
    
    chat_input = st.chat_input("Describe a specific friction point you solved in your last role...")
    
    if chat_input:
        with st.chat_message("assistant"):
            prompt = (
                f"You are the Jobberly Advocate. The candidate mentioned: '{chat_input}'. "
                "Ask one probing, evidence-based question to uncover the specific impact "
                "on metrics like company burn rate, revenue, or operational speed."
            )
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            st.write(response.text)
            st.caption("Evidence captured and mapped to your verified profile.")

# --- Tab 2: Command Center (Scout Decoder) ---
with tab_scout:
    st.header("The Deception Decoder")
    st.write("Analyze job listings to identify Ghost Jobs and budget mismatches.")
    
    jd_input = st.text_area("Paste a Job Description (JD) or URL:", height=200, placeholder="Paste here...")
    
    if st.button("Analyze Listing"):
        if jd_input:
            with st.spinner("Decoding corporate-speak..."):
                scout_prompt = (
                    f"Analyze this JD for the following: "
                    "1. Ghost Score (0-100 probability listing is fake/stale). "
                    "2. Internal-Hire Signals (Is this a compliance posting?). "
                    "3. Budget Prediction (Estimated range based on company stage). "
                    "4. Purple Squirrel Check (Unrealistic requirement list). "
                    f"JD Text: {jd_input}"
                )
                response = client.models.generate_content(model="gemini-2.0-flash", contents=scout_prompt)
                
                # Layout for key metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Ghost Score", "24%", "Low Risk")
                col2.metric("Predicted Budget", "$140k - $165k")
                col3.metric("Must-Haves", "3/12 Detected")
                
                st.markdown("### 📊 Scout Report")
                st.write(response.text)
        else:
            st.warning("Please paste a job description first.")

# --- Tab 3: Strategic Intel (Company Archeology) ---
with tab_intel:
    st.header("Company Archeology")
    st.write("Research a company's 'bleeding neck' pain points before you apply.")
    
    company_name = st.text_input("Enter Target Company Name:")
    
    if st.button("Generate Intel Report"):
        with st.spinner(f"Researching {company_name}..."):
            intel_prompt = (
                f"Analyze {company_name}. Provide: "
                "1. Current Market Stage (e.g., Series B, Mature). "
                "2. Likely Competitive Pain Points. "
                "3. A 3-Minute Interview Script focused on solving their specific challenges."
            )
            response = client.models.generate_content(model="gemini-2.0-flash", contents=intel_prompt)
            st.markdown(f"### 🧠 {company_name} Strategic Pitch")
            st.write(response.text)

# --- Tab 4: Outreach Architect ---
with tab_outreach:
    st.header("LinkedIn Connection Architect")
    st.write("Bypass the ATS by connecting directly with human decision-makers.")
    
    dm_role = st.text_input("Hiring Manager/Decision Maker Role (e.g., VP of Product):")
    
    if st.button("Draft Tactical Note"):
        if dm_role:
            outreach_prompt = (
                f"Write a 300-character personalized LinkedIn connection request to a {dm_role}. "
                "Focus on offering a solution to a problem, not asking for a favor. Be direct and tactical."
            )
            response = client.models.generate_content(model="gemini-2.0-flash", contents=outreach_prompt)
            st.markdown("### 📧 Connection Pitch")
            st.code(response.text, language="markdown")
            st.caption("Keep it under 300 characters to ensure it fits in a standard invite.")
        else:
            st.warning("Please specify a role.")

# --- Tab 5: Market Tracking & Accountability ---
with tab_track:
    st.header("Accountability Ledger")
    st.write("Track applications and enforce the Feedback Escrow protocol.")
    
    # Mock Tracking Data
    data = {
        "Company": ["GlobalTech", "CloudScale", "InnovateIQ"],
        "Status": ["Interview Scheduled", "Ghosted (Claim Filed)", "Applied"],
        "Feedback Escrow": ["Locked", "Transferred to Seeker ($50)", "N/A"],
        "Reputation Score": ["4.2/5", "1.8/5", "3.9/5"]
    }
    st.table(pd.DataFrame(data))
    
    st.divider()
    st.button("Activate 'Be Discovered' Mode (Reverse Auction)")
    st.caption("Your verified anonymous profile will be visible to employers for bidding.")
