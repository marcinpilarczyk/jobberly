import streamlit as st
from google import genai
import pypdf
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Jobberly | Candidate Advocate", layout="wide", page_icon="🛡️")

# 2. API Configuration
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Missing GEMINI_API_KEY. Please add it to your Streamlit Secrets.")
    st.stop()

# 3. Session State Initialization
if 'career_vault' not in st.session_state:
    st.session_state['career_vault'] = None

# 4. Sidebar: Identity, Metrics, and Model Selection
with st.sidebar:
    st.title("🛡️ Jobberly")
    st.markdown("**The Candidate-Centric Employment Protocol**")
    
    st.divider()
    
    st.subheader("🤖 AI Settings")
    selected_model = st.selectbox(
        "Select Model Tier:",
        ["gemini-3-flash-preview", "gemini-3-pro-preview"],
        index=0,
        help="Choose the next-generation model for discovery and analysis."
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
    st.caption("Jobberly v1.7.0 (Forensic Intelligence)")

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
                You are a Career Data Architect. Parse this FULL LinkedIn history 
                into a structured summary. Identify:
                1. Years of experience and seniority level.
                2. Quantifiable achievements and metrics.
                3. High-value skills and technical stack.
                4. Map these to potential corporate 'pain points'.
                
                TEXT: {full_text} 
                """
                response = client.models.generate_content(model=selected_model, contents=prompt)
                st.session_state['career_vault'] = response.text
                st.success("Vault Seeded with Full Profile Data!")
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
                        "Ask a probing, evidence-based question to uncover deep achievements "
                        "or impact on metrics (burn rate, revenue) not explicitly in the PDF."
                    )
                    res = client.models.generate_content(model=selected_model, contents=interview_prompt)
                    st.write(res.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")

# --- Tab 2: Command Center (Forensic Scout) ---
with tab_scout:
    st.header("The Deception Decoder")
    st.write("Forensic analysis of job listings to identify intent and risk.")
    
    jd_text = st.text_area("Paste a Job Description (JD):", height=200)
    if st.button("Analyze Listing"):
        if jd_text:
            with st.spinner(f"Decoding Forensic DNA with {selected_model}..."):
                try:
                    # Forensic prompt based on Job Ad Analysis research
                    scout_prompt = f"""
                    You are the Jobberly Candidate Advocate. Analyze this Job Description (JD) using the following research-backed forensic markers.
                    
                    ### CANDIDATE CONTEXT (From Vault):
                    {st.session_state['career_vault'] if st.session_state['career_vault'] else "No vault data. Use general market benchmarks."}

                    ### REQUIREMENTS FOR THE REPORT:
                    1. **Ghost Score**: Calculate the probability this is a 'Phantom Vacancy'. Look for Reposting Cycles and Relative Vacancy Age (RVA)[cite: 81, 85].
                    2. **Internal-Hire Signals**: Identify 'Compliance DNA'. Look for high-granularity skill conjunctions (AND statements) that perfectly match a pre-selected person[cite: 22, 38].
                    3. **Trust Indicators**: Check for 'Active Promotion' and 'Named Managers' as positive signals.
                    4. **Wage-to-Value Ratio**: Compare the offered salary against the complexity of requirements. Flag outliers where requirements are high but pay is low (Title Deflation) or vice-versa (Scam Risk)[cite: 123, 134].
                    5. **Budget Prediction**: Research the local market for this role and location. Factor in the candidate's seniority and skills from the Vault.
                    
                    ### OUTPUT FORMAT:
                    Use color-coded markdown for scores:
                    - **0-30**: :green[Low Risk]
                    - **31-60**: :orange[Moderate Risk]
                    - **61-100**: :red[High Risk]

                    DO NOT HALLUCINATE. If data is missing (e.g. location or salary), provide a range based on detected markers and state the assumption.

                    JD TEXT: {jd_text}
                    """
                    res = client.models.generate_content(model=selected_model, contents=scout_prompt)
                    st.markdown("---")
                    st.markdown("### 🕵️ Forensic Scout Report")
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"Analysis Error: {e}")
        else:
            st.warning("Please paste a job description first.")

# --- Tab 3: Strategic Intel (Enhanced Archeology) ---
with tab_intel:
    st.header("Company Archeology")
    st.write("Deep research on company pain points and strategic alignment.")
    comp_name = st.text_input("Target Company Name:")
    if st.button("Generate Strategic Intel"):
        if comp_name:
            with st.spinner(f"Researching {comp_name}..."):
                try:
                    intel_prompt = f"""
                    Research {comp_name}.
                    1. **Company Stage**: Analyze current product lifecycle and funding[cite: 75].
                    2. **'Bleeding Neck' Pain Points**: Identify 3 competitive friction points.
                    3. **The Strategic Cheat Sheet**: 
                        - **The Core Bridge**: How to frame candidate experience.
                        - **Highlight the Friction**: Key achievement to mention.
                        - **The X-Factor**: How to stand out from 'Purple Squirrel' hunts[cite: 33].
                    4. **3-Minute Interview Script**: Tailored to these pain points.
                    
                    Candidate context from Vault: {st.session_state['career_vault']}
                    """
                    res = client.models.generate_content(model=selected_model, contents=intel_prompt)
                    st.markdown(f"### 🧠 {comp_name} Strategy Map")
                    st.write(res.text)
                except Exception as e:
                    st.error(f"Research Error: {e}")

# --- Tab 4: Outreach Architect ---
with tab_outreach:
    st.header("LinkedIn Connection Architect")
    role = st.text_input("Decision Maker Title:")
    if st.button("Draft Tactical Note"):
        if role:
            try:
                outreach_prompt = f"Write a 300-char LinkedIn note to a {role}. Focus on solving a specific corporate friction point[cite: 10]."
                res = client.models.generate_content(model=selected_model, contents=outreach_prompt)
                st.code(res.text, language="markdown")
            except Exception as e:
                st.error(f"Drafting Error: {e}")

# --- Tab 5: Market Tracking ---
with tab_track:
    st.header("Accountability Ledger")
    st.write("Track status and enforce the 'Feedback Escrow'[cite: 66].")
    tracking_data = pd.DataFrame({
        "Company": ["GlobalCorp", "TechStart"],
        "Status": ["Interview Scheduled", "Ghosted (Claim Pending)"],
        "Escrow Status": ["Locked", "Transferred to Seeker ($50)"]
    })
    st.table(tracking_data)
