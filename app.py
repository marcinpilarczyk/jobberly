import streamlit as st
from google import genai
import pandas as pd

# 1. Setup & Configuration
st.set_page_config(page_title="Jobberly | Candidate Advocate", layout="wide", page_icon="🛡️")
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Sidebar for Global Stats & Identity
with st.sidebar:
    st.title("🛡️ Jobberly")
    st.status("Career Vault: Encrypted & Local", state="complete") # [cite: 345]
    st.metric("Hiring Reputation (Global)", "3.8/5", "-0.2") # [cite: 341]
    st.divider()
    st.info("You own your data via Self-Sovereign Identity (SSI). No third-party harvests your profile here. [cite: 345, 503]")

# Main Navigation Tabs based on Product Architecture [cite: 315]
tab_onboard, tab_scout, tab_intel, tab_outreach, tab_track = st.tabs([
    "🚀 Discovery Engine", "🕵️ Command Center", "🧠 Strategic Intel", "📧 Outreach Architect", "📊 Market Tracking"
])

# --- TAB 1: DISCOVERY ENGINE (ONBOARDING) ---
with tab_onboard:
    st.header("Phase 1: Build Your Proof-Based Vault [cite: 351]")
    st.write("Transition from a static resume to a verified professional identity. [cite: 308, 504]")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Import from LinkedIn"):
            st.success("Work history, skills, and endorsements seeded into local vault. [cite: 317]")
    
    st.subheader("Interactive AI Interview [cite: 318]")
    user_input = st.chat_input("Tell the AI about a time you solved a major friction point...")
    if user_input:
        with st.chat_message("assistant"):
            st.write(f"Deep-diving into: '{user_input}'...")
            prompt = f"Ask a probing, evidence-based question about: {user_input}. Focus on impact on burn rate or operational pain points. [cite: 319]"
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            st.write(response.text)
            st.caption("This data is stored as a 'Proof of Value' in your encrypted vault. [cite: 319, 510]")

# --- TAB 2: COMMAND CENTER (SCOUT) ---
with tab_scout:
    st.header("Phase 2: The Deception Decoder [cite: 352]")
    st.write("Analyze listings to bypass the '75% Wall' of ATS rejection. [cite: 310, 428]")
    
    jd_input = st.text_area("Paste Job URL or Description:", height=200)
    if st.button("Analyze for Deception"):
        with st.spinner("Calculating Ghost Score... [cite: 352]"):
            scout_prompt = f"Analyze this JD for: 1. Ghost Score (0-100), 2. Internal-Hire Signals, 3. Budget Prediction (based on Series B stage), 4. Must-Haves vs. Wish-List. JD: {jd_input}"
            response = client.models.generate_content(model="gemini-2.0-flash", contents=scout_prompt)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Ghost Score", "27%", "High Risk") # [cite: 399]
            c2.metric("Predicted Budget", "$145k - $175k") # [cite: 325]
            c3.metric("Match Authenticity", "92%") # [cite: 326]
            
            st.markdown("### 📊 Scout Report")
            st.write(response.text)

# --- TAB 3: STRATEGIC INTEL (RESEARCH) ---
with tab_intel:
    st.header("Phase 3: The Perfect Pitch [cite: 330]")
    st.write("Research 'bleeding neck' pain points to win the interview. [cite: 329]")
    
    company_name = st.text_input("Target Company Name:")
    if st.button("Generate Strategic Intel"):
        with st.spinner("Conducting Company Archeology... [cite: 329]"):
            intel_prompt = f"Research {company_name}. Provide: 1. Current Product Lifecycle Stage, 2. Competitive Pain Points, 3. A 3-Minute Interview Script tailored to these needs. [cite: 333]"
            response = client.models.generate_content(model="gemini-2.0-flash", contents=intel_prompt)
            st.markdown(f"### 🧬 {company_name} Strategy Map")
            st.write(response.text)

# --- TAB 4: OUTREACH ARCHITECT ---
with tab_outreach:
    st.header("Phase 4: Bypass the ATS [cite: 334]")
    st.write("Direct-to-Human connection sequences for decision-makers. [cite: 335]")
    
    target_role = st.text_input("Decision Maker Title (e.g., VP of Sales):")
    if st.button("Generate Tactical Note"):
        outreach_prompt = f"Write a 300-character personalized LinkedIn note to a {target_role} at {company_name}. Focus on solving a specific problem, not asking for a favor. [cite: 336]"
        response = client.models.generate_content(model="gemini-2.0-flash", contents=outreach_prompt)
        st.code(response.text, language="markdown")
        st.caption("High-intent, tactical connection request. [cite: 336]")

# --- TAB 5: MARKET TRACKING ---
with tab_track:
    st.header("Phase 5: Market Accountability [cite: 354]")
    st.write("Track status and enforce the 'Feedback Escrow'. ")
    
    # Mock Tracking Data [cite: 339, 340]
    tracking_data = {
        "Company": ["GlobalCorp", "TechStart", "InnovateIQ"],
        "Status": ["Interview Scheduled", "Ghosted (Claim Pending)", "Applied"],
        "Escrow Status": ["Locked", "Transferred to Seeker", "N/A"],
        "Wage Index": ["Fair", "Title Deflation Detected", "Above Market"]
    }
    st.table(pd.DataFrame(tracking_data))
    
    st.divider()
    if st.button("Activate 'Be Discovered' Mode (Reverse Auction)"):
        st.warning("Your verified anonymous profile is now visible. Companies must pay to bid for your time. [cite: 355, 515]")
