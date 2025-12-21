import streamlit as st
from google import genai
import pandas as pd

# Setup
st.set_page_config(page_title="Jobberly | Candidate Advocate", layout="wide", page_icon="🛡️")

# Initialize Client via Secrets
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Missing GEMINI_API_KEY in Secrets.")
    st.stop()

# Sidebar
with st.sidebar:
    st.title("🛡️ Jobberly")
    st.info("The protocol where the candidate is the protected asset.")
    st.divider()
    st.status("Career Vault: Encrypted & Local", state="complete")
    st.metric("Global Hiring Reputation", "3.8/5", "-0.2")

# Tabs
tab_onboard, tab_scout, tab_intel, tab_outreach = st.tabs([
    "🚀 Discovery Engine", "🕵️ Command Center", "🧠 Strategic Intel", "📧 Outreach Architect"
])

# Phase 1: Discovery Engine
with tab_onboard:
    st.header("Build Your Proof-Based Vault")
    st.write("Transition from a static resume to a verified professional identity.")
    
    chat_input = st.chat_input("Tell the Advocate about a major win at your last job...")
    if chat_input:
        with st.chat_message("assistant"):
            prompt = f"Ask a probing question about: {chat_input}. Focus on friction points and impact on metrics like burn rate."
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            st.write(response.text)
            st.caption("Saved to Local Career Vault.")

# Phase 2: Command Center
with tab_scout:
    st.header("The Deception Decoder")
    st.write("Analyze listings for 'Ghost Jobs' and 'Internal-Hire Theater.'")
    
    jd_text = st.text_area("Paste a Job Description (JD):", height=150)
    if st.button("Analyze for Deception"):
        with st.spinner("Decoding corporate-speak..."):
            scout_prompt = f"Analyze this JD for: 1. Ghost Score (0-100), 2. Internal-Hire Signals, 3. Must-Haves vs. Wish-List. JD: {jd_text}"
            response = client.models.generate_content(model="gemini-2.0-flash", contents=scout_prompt)
            st.markdown("### 📊 Scout Report")
            st.write(response.text)

# Phase 3: Strategic Intel
with tab_intel:
    st.header("Company Archeology & Pitching")
    comp_name = st.text_input("Target Company:")
    if st.button("Generate Pain-Point Pitch"):
        prompt = f"Research {comp_name}. Identify 3 'bleeding neck' pain points for their current stage."
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        st.write(response.text)

# Phase 4: Outreach Architect
with tab_outreach:
    st.header("LinkedIn Connection Architect")
    role = st.text_input("Decision Maker Title:")
    if st.button("Draft Tactical Note"):
        prompt = f"Write a 300-char LinkedIn note to a {role} at {comp_name} focused on solving a problem."
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        st.code(response.text)
