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
    st.caption("Jobberly v1.8.0 (Trust Protocol)")

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
                
                # Context-aware parsing
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

# --- Tab 2: Command Center (Trust Protocol Scout) ---
with tab_scout:
    st.header("The Deception Decoder")
    st.write("Generate a Forensic Trust Report based on the Jobberly Protocol.")
    
    jd_text = st.text_area("Paste a Job Description (JD):", height=200)
    if st.button("Generate Trust Report"):
        if jd_text:
            with st.spinner(f"Executing Forensic Protocol with {selected_model}..."):
                try:
                    # IMPLEMENTING THE SPECIFIC USER PROTOCOL
                    scout_prompt = f"""
                    Analyze this Job Description using the Jobberly Analysis Protocol.
                    
                    ### CANDIDATE CONTEXT (From Vault):
                    {st.session_state['career_vault'] if st.session_state['career_vault'] else "No vault data available."}

                    ### 1. INTERNAL-HIRE / COMPLIANCE DETECTION:
                    - Scan for Regulatory Boilerplate: 'Notice of Filing,' 'Prevailing Wage,' or 'Labor Certification'.
                    - Analyze Specificity: Check for 'kitchen sink' hyper-specific conjunctions (AND statements) designed to exclude others.
                    - Check for Lack of 'Selling' Language: Is it clinical and devoid of culture/benefits?

                    ### 2. GHOSTING & DATA HARVESTING RISK:
                    - Scan for Evergreen Language: Vague titles or phrases implying a 'continuous pipeline'.
                    - Check for Reposting Artifacts: Flag dates that are months old or 'rolling' intake language.
                    - Reputation Check: Factor in general responsive employer trends for companies of this type.

                    ### 3. SCAM & ECONOMIC ANOMALY DETECTION:
                    - Wage-to-Value Ratio: Compare Salary vs Title/Requirements. Identify Scam Risk (High pay/Low skill) or Title Deflation (Low pay/High skill).
                    - Scan for Urgency & Payment Signals: Flag 'Immediate Start,' 'Wire Transfer,' or non-corporate emails.

                    ### 4. BUDGET PREDICTION (Keep existing logic):
                    - Research local market for this role/location.
                    - Factor in candidate seniority and skills from the Vault.

                    ### OUTPUT FORMAT (MANDATORY):
                    - **Overall Trust Score**: (0-100) - Color code: 0-30 :red[], 31-60 :orange[], 61-100 :green[]
                    - **Red Flags**: (Bullet points of suspicious phrases)
                    - **Likelihood of Internal Pre-Selection**: (Low/Medium/High) + Explanation.
                    - **Ghosting Probability**: (Low/Medium/High) + Explanation.
                    - **Budget Prediction**: (Forensic Estimate)
                    - **Worth Applying?**: (Yes/Proceed with Caution/Avoid)

                    DO NOT HALLUCINATE.

                    JD TEXT: {jd_text}
                    """
                    res = client.models.generate_content(model=selected_model, contents=scout_prompt)
                    st.markdown("---")
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"Protocol Execution Error: {e}")
        else:
            st.warning("Please paste a job description first.")

# --- Tab 3: Strategic Intel (Includes Cheat Sheet) ---
with tab_intel:
    st.header("Strategic Intelligence")
    comp_name = st.text_input("Target Company Name:")
    if st.button("Generate Strategy Map"):
        if comp_name:
            with st.spinner(f"Building Intelligence Map..."):
                try:
                    intel_prompt = f"""
                    Research {comp_name}. 
                    Provide:
                    1. **Company Stage & Lifecycle Analysis**.
                    2. **'Bleeding Neck' Pain Points**.
                    3. **Strategic 'Cheat Sheet' for Applying**:
                       - The Core Bridge: Framing your experience.
                       - Highlight the Friction: Key achievement to mention.
                       - The X-Factor: Standing out from 'Purple Squirrel' hunts.
                    4. **3-Minute Interview Script**.
                    
                    Candidate Context: {st.session_state['career_vault']}
                    """
                    res = client.models.generate_content(model=selected_model, contents=intel_prompt)
                    st.markdown(f"### 🧬 {comp_name} Intelligence Map")
                    st.write(res.text)
                except Exception as e:
                    st.error(f"Intel Error: {e}")

# --- Tab 4: Outreach Architect ---
with tab_outreach:
    st.header("LinkedIn Outreach")
    role = st.text_input("Decision Maker Title:")
    if st.button("Generate Note"):
        if role:
            try:
                outreach_prompt = f"Write a 300-char LinkedIn note to a {role} at {comp_name} solving a specific problem."
                res = client.models.generate_content(model=selected_model, contents=outreach_prompt)
                st.code(res.text, language="markdown")
            except Exception as e:
                st.error(f"Error: {e}")

# --- Tab 5: Market Tracking ---
with tab_track:
    st.header("Accountability Ledger")
    tracking_data = pd.DataFrame({
        "Company": ["GlobalCorp", "TechStart"],
        "Status": ["Interview Scheduled", "Ghosted (Claim Filed)"],
        "Feedback Escrow": ["Locked", "Transferred to Seeker ($50)"]
    })
    st.table(tracking_data)
