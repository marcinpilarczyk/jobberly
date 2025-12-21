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
    st.error("Missing GEMINI_API_KEY. Please add it to your Streamlit Secrets.")
    st.stop()

# 3. Session State Initialization
if 'career_vault' not in st.session_state:
    st.session_state['career_vault'] = None
if 'detected_company' not in st.session_state:
    st.session_state['detected_company'] = ""
if 'potential_managers' not in st.session_state:
    st.session_state['potential_managers'] = []

# 4. Sidebar: Identity, Metrics, and Support
with st.sidebar:
    st.title("🛡️ Jobberly")
    st.markdown("**The Candidate-Centric Employment Protocol**")
    
    st.divider()
    
    st.subheader("🤖 AI Settings")
    selected_model = st.selectbox(
        "Select Model Tier:",
        ["gemini-3-flash-preview", "gemini-3-pro-preview"],
        index=0,
        help="Choose the next-generation model for forensic analysis."
    )
    
    st.divider()
    
    if st.session_state['career_vault']:
        st.status("Career Vault: Verified & Populated", state="complete")
    else:
        st.status("Career Vault: Awaiting Data", state="error")
    
    st.metric("Global Hiring Reputation", "3.8/5", "-0.2")
    
    st.divider()
    st.subheader("💳 Support the Protocol")
    st.markdown("[Pay What You Can (Lemon Squeezy)](#)")
    st.caption("Jobberly v2.2.0 (Automated Outreach)")

# 5. Main Application Interface
st.title("🛡️ Jobseeker Advocate Suite")

tab_onboard, tab_scout, tab_intel, tab_outreach, tab_track = st.tabs([
    "🚀 Discovery Engine", 
    "🕵️ Command Center", 
    "🧠 Strategic Intel", 
    "📧 Outreach Architect",
    "📊 Market Tracking"
])

# --- Tab 1: Discovery Engine ---
with tab_onboard:
    st.header("1. Build Your Proof-Based Vault")
    st.write("LinkedIn -> More... -> Save to PDF. Upload it below to seed your vault.")
    
    uploaded_file = st.file_uploader("Upload LinkedIn PDF", type="pdf")
    
    if uploaded_file and not st.session_state['career_vault']:
        with st.spinner(f"Analyzing history with {selected_model}..."):
            try:
                reader = pypdf.PdfReader(uploaded_file)
                full_text = "".join([page.extract_text() for page in reader.pages])
                
                prompt = f"""
                You are a Career Data Architect. Parse this LinkedIn profile.
                IDENTIFY: 
                1. Seniority Level (Junior, Mid, Senior, Executive).
                2. Hard Technical Skills & Soft Competencies.
                3. Quantifiable Achievements.
                4. Estimated Years of Relevant Experience.
                
                TEXT: {full_text}
                """
                response = client.models.generate_content(model=selected_model, contents=prompt)
                st.session_state['career_vault'] = response.text
                st.success("Vault Seeded with Seniority and Skill Benchmarks!")
            except Exception as e:
                st.error(f"Error seeding vault: {e}")

    if st.session_state['career_vault']:
        st.divider()
        st.subheader("2. AI Interactive Interview")
        st.info("Vault Analysis (Problem-Solver Profile):")
        st.write(st.session_state['career_vault'])
        
        chat_input = st.chat_input("Tell the Advocate about a major win at work...")
        if chat_input:
            with st.chat_message("assistant"):
                try:
                    interview_prompt = (
                        f"Context: {st.session_state['career_vault']}. "
                        f"The candidate claims: '{chat_input}'. "
                        "Ask an evidence-based question to uncover impact metrics."
                    )
                    res = client.models.generate_content(model=selected_model, contents=interview_prompt)
                    st.write(res.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")

# --- Tab 2: Command Center (Forensic Trust Report) ---
with tab_scout:
    st.header("The Deception Decoder")
    st.write("Forensic analysis of job listings to identify intent, trust, and risk.")
    
    jd_text = st.text_area("Paste a Job Description (JD):", height=200)
    if st.button("Generate Trust Report"):
        if jd_text:
            with st.spinner(f"Decoding Forensic DNA with {selected_model}..."):
                try:
                    scout_prompt = f"""
                    Analyze this Job Description using the Jobberly Protocol. 
                    
                    ### ANALYSIS PROTOCOLS:
                    1. INTERNAL-HIRE/COMPLIANCE DETECTION:
                       - Scan for Regulatory Boilerplate: 'Notice of Filing,' 'Prevailing Wage,' or 'Labor Certification'. [cite: 64]
                       - Analyze Specificity: Identify 'kitchen sink' hyper-specific conjunctions (AND statements). [cite: 38]
                    2. GHOSTING & DATA HARVESTING RISK:
                       - Scan for Evergreen Language: Vague titles or pipeline phrases. [cite: 71]
                       - Check for Reposting Artifacts: Flag old dates or 'rolling' intake language. [cite: 81]
                    3. SCAM & ECONOMIC ANOMALY DETECTION:
                       - Wage-to-Value Ratio: Compare Salary vs Requirements. Detect Scam Risk or Title Deflation. [cite: 112]
                    
                    ### OUTPUT FORMAT (MANDATORY):
                    Use color coding: Red (Bad), Orange (Medium), Green (Good).
                    - **Overall Trust Score**: (0-100)
                    - **Red Flags**: (Specific suspicious phrases)
                    - **Likelihood of Internal Pre-Selection**: (Low/Medium/High)
                    - **Ghosting Probability**: (Low/Medium/High)
                    - **Budget Prediction**: (Forensic estimate)
                    - **Company Name**: (Identify the company name)

                    DO NOT HALLUCINATE.
                    JD TEXT: {jd_text}
                    """
                    res = client.models.generate_content(model=selected_model, contents=scout_prompt)
                    st.markdown("---")
                    st.markdown("### 🕵️ Forensic Trust Report")
                    st.markdown(res.text)
                    
                    # Store company name and trigger manager search
                    if "**Company Name**:" in res.text:
                        st.session_state['detected_company'] = res.text.split("**Company Name**:")[1].strip().split("\n")[0]
                        # Reset potential managers when a new company is detected
                        st.session_state['potential_managers'] = []
                except Exception as e:
                    st.error(f"Analysis Error: {e}")
        else:
            st.warning("Please paste a job description first.")

# --- Tab 3: Strategic Intel (Enhanced Control) ---
with tab_intel:
    st.header("Strategic Intelligence")
    st.write("Deep research to help you control the interview and demonstrate expertise.")
    
    comp_name = st.text_input("Target Company Name:", value=st.session_state['detected_company'])
    if st.button("Generate Strategic Intel"):
        if comp_name:
            with st.spinner(f"Building Intelligence Map for {comp_name}..."):
                try:
                    intel_prompt = f"""
                    Research {comp_name} to empower the candidate.
                    1. **Company Stage & Lifecycle Analysis**. [cite: 171]
                    2. **'Bleeding Neck' Pain Points**. [cite: 10]
                    3. **Strategic 'Cheat Sheet' for Applying**. [cite: 250]
                    4. **Strategic Control Questions (To ask on Interview)**:
                       - A set of 5 questions to demonstrate expertise and understand pain points.
                    
                    Candidate context: {st.session_state['career_vault']}
                    """
                    res = client.models.generate_content(model=selected_model, contents=intel_prompt)
                    st.markdown(f"### 🧠 {comp_name} Intelligence Map")
                    st.write(res.text)
                except Exception as e:
                    st.error(f"Research Error: {e}")

# --- Tab 4: Outreach Architect (Automated Manager Identification) ---
with tab_outreach:
    st.header("LinkedIn Outreach Architect")
    st.write("Identify potential hiring managers and craft high-intent messages.")
    
    comp_name = st.text_input("Company:", value=st.session_state['detected_company'])
    
    if st.button("Research Potential Hiring Managers"):
        if comp_name:
            with st.spinner(f"Identifying decision-makers at {comp_name}..."):
                try:
                    manager_prompt = f"""
                    Identify 1-2 potential hiring manager roles/personas for a role at {comp_name}. 
                    Base your search on common organizational structures for this company's size and stage.
                    Provide ONLY the titles (e.g., 'Director of Engineering' or 'Head of Marketing').
                    """
                    res = client.models.generate_content(model=selected_model, contents=manager_prompt)
                    # Simple split to list titles
                    st.session_state['potential_managers'] = [m.strip() for m in res.text.split('\n') if m.strip()]
                    st.success("Potential hiring manager roles identified.")
                except Exception as e:
                    st.error(f"Manager Research Error: {e}")
    
    # Selection of identified managers
    selected_role = st.selectbox("Select Target Manager Role:", 
                                 options=st.session_state['potential_managers'] if st.session_state['potential_managers'] else ["(Perform research first)"])
    
    if st.button("Generate Tactical Outreach Note"):
        if selected_role and selected_role != "(Perform research first)":
            with st.spinner("Crafting high-intent outreach..."):
                try:
                    outreach_prompt = f"""
                    Write a 300-char LinkedIn note to the '{selected_role}' at {comp_name}. 
                    Focus on solving a specific corporate friction point identified in the Intel phase. 
                    Be direct, tactical, and bypass the '75% Wall' of ATS rejection. 
                    """
                    res = client.models.generate_content(model=selected_model, contents=outreach_prompt)
                    st.markdown("### 📧 Tactical Connection Note")
                    st.code(res.text, language="markdown")
                    st.caption("Designed to fit in a 300-character LinkedIn invite.")
                except Exception as e:
                    st.error(f"Outreach Error: {e}")

# --- Tab 5: Market Tracking ---
with tab_track:
    st.header("Accountability Ledger")
    st.write("Track status and enforce the 'Feedback Escrow'.")
    tracking_data = pd.DataFrame({
        "Company": ["GlobalCorp", "TechStart"],
        "Status": ["Interview Scheduled", "Ghosted (Claim Filed)"],
        "Feedback Escrow": ["Locked", "Transferred to Seeker ($50)"]
    })
    st.table(tracking_data)
