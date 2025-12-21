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
if 'last_jd_analyzed' not in st.session_state:
    st.session_state['last_jd_analyzed'] = ""
if 'potential_managers' not in st.session_state:
    st.session_state['potential_managers'] = []

# 4. Sidebar: Identity & Metrics
with st.sidebar:
    st.title("🛡️ Jobberly")
    st.markdown("**The Candidate-Centric Employment Protocol**")
    
    st.divider()
    
    st.subheader("🤖 AI Settings")
    selected_model = st.selectbox(
        "Select Model Tier:",
        ["gemini-3-flash-preview", "gemini-3-pro-preview"],
        index=0,
        help="Choose the model for forensic analysis and outreach."
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
    st.caption("Jobberly v2.5.0 (Application Builder)")

# 5. Main Application Interface
st.title("🛡️ Jobseeker Advocate Suite")

tab_onboard, tab_scout, tab_intel, tab_outreach, tab_builder, tab_track = st.tabs([
    "🚀 Discovery Engine", 
    "🕵️ Command Center", 
    "🧠 Strategic Intel", 
    "📧 Outreach Architect",
    "📝 Application Builder",
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
                You are a Career Data Architect. Parse this LinkedIn profile into a verified 'Problem-Solver' profile.
                IDENTIFY: 
                1. Seniority Level and Core Function.
                2. Technical Stack and High-Value Skills.
                3. Top 3 Quantifiable Wins (Metrics, revenue impact, or burn rate reduction).
                4. Strategic Strengths.
                
                TEXT: {full_text}
                """
                response = client.models.generate_content(model=selected_model, contents=prompt)
                st.session_state['career_vault'] = response.text
                st.success("Vault Seeded: Your professional identity is now a 'Problem-Solver' asset.")
            except Exception as e:
                st.error(f"Error seeding vault: {e}")

    if st.session_state['career_vault']:
        st.divider()
        st.subheader("2. AI Interactive Interview")
        st.info("Vault Analysis (Problem-Solver Profile):")
        st.write(st.session_state['career_vault'])
        
        chat_input = st.chat_input("Tell the Advocate about a major win at your last job...")
        if chat_input:
            with st.chat_message("assistant"):
                try:
                    interview_prompt = (
                        f"Context: {st.session_state['career_vault']}. "
                        f"The candidate claims: '{chat_input}'. "
                        "Ask a probing question to find the forensic achievement data."
                    )
                    res = client.models.generate_content(model=selected_model, contents=interview_prompt)
                    st.write(res.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")

# --- Tab 2: Command Center (Forensic Trust Report) ---
with tab_scout:
    st.header("The Deception Decoder")
    st.write("Forensic analysis of job listings to identify intent, trust, and risk.")
    
    jd_text = st.text_area("Paste a Job Description (JD):", height=200, key="scout_jd_input")
    if st.button("Generate Trust Report"):
        if jd_text:
            st.session_state['last_jd_analyzed'] = jd_text
            with st.spinner(f"Decoding Forensic DNA with {selected_model}..."):
                try:
                    scout_prompt = f"""
                    Analyze this Job Description using the Jobberly Protocol. 
                    
                    ### OUTPUT FORMAT:
                    - **Overall Trust Score**: (0-100)
                    - **Red Flags**: (Linguistic artifacts like 'Notice of Filing' or 'Purple Squirrel' conjunctions)
                    - **Likelihood of Internal Pre-Selection**: (Low/Medium/High)
                    - **Ghosting Probability**: (Check RVA and Repost patterns)
                    - **Budget Prediction**: (Factoring candidate context if available)
                    - **Company Name**: (Identify target)

                    JD TEXT: {jd_text}
                    """
                    res = client.models.generate_content(model=selected_model, contents=scout_prompt)
                    st.markdown("---")
                    st.markdown(res.text)
                    
                    if "**Company Name**:" in res.text:
                        st.session_state['detected_company'] = res.text.split("**Company Name**:")[1].strip().split("\n")[0]
                except Exception as e:
                    st.error(f"Analysis Error: {e}")
        else:
            st.warning("Please paste a job description first.")

# --- Tab 3: Strategic Intel (Enhanced Control) ---
with tab_intel:
    st.header("Strategic Intelligence")
    st.write("Deep research to help you control the interview and demonstrate expertise.")
    
    comp_name = st.text_input("Target Company Name:", value=st.session_state['detected_company'], key="intel_comp_name")
    if st.button("Generate Strategic Intel"):
        if comp_name:
            with st.spinner(f"Building Intelligence Map for {comp_name}..."):
                try:
                    intel_prompt = f"""
                    Research {comp_name} to empower the candidate.
                    1. **Company Stage & Lifecycle Analysis**.
                    2. **'Bleeding Neck' Pain Points**.
                    3. **Strategic 'Cheat Sheet' for Applying**:
                       - The Core Bridge: Framing candidate experience against pain points.
                       - Highlight the Friction: Key achievement to mention.
                       - The X-Factor.
                    4. **Strategic Control Questions (Candidate to Ask)**.
                    
                    Candidate context: {st.session_state['career_vault']}
                    """
                    res = client.models.generate_content(model=selected_model, contents=intel_prompt)
                    st.markdown(f"### 🧠 {comp_name} Intelligence Map")
                    st.write(res.text)
                except Exception as e:
                    st.error(f"Research Error: {e}")

# --- Tab 4: Outreach Architect ---
with tab_outreach:
    st.header("LinkedIn Outreach Architect")
    st.write("Identify decision-makers and craft grounded, personal messages.")
    
    outreach_comp = st.text_input("Target Company:", value=st.session_state['detected_company'], key="outreach_comp_name")
    
    if st.button("Identify Potential Hiring Managers by Name"):
        if outreach_comp:
            with st.spinner(f"Searching organizational artifacts for {outreach_comp}..."):
                try:
                    manager_prompt = f"Identify 2 likely hiring managers at {outreach_comp} by NAME and TITLE. Format: Name | Title"
                    res = client.models.generate_content(model=selected_model, contents=manager_prompt)
                    st.session_state['potential_managers'] = [m.strip() for m in res.text.split('\n') if "|" in m]
                    st.success(f"Potential decision-makers identified.")
                except Exception as e:
                    st.error(f"Identification Error: {e}")
    
    selected_target = st.selectbox("Select Outreach Target:", options=st.session_state['potential_managers'] if st.session_state['potential_managers'] else ["(Perform identification first)"])
    
    if st.button("Generate Grounded Outreach Note"):
        if selected_target and "|" in selected_target:
            with st.spinner("Synthesizing 1st person connection..."):
                try:
                    name, title = selected_target.split("|")
                    outreach_prompt = f"""
                    Write a 1st-person LinkedIn note to {name.strip()} ({title.strip()}) at {outreach_comp}.
                    GROUNDING: {st.session_state['career_vault']}
                    Bypass the '75% Wall' by offering a solution to a pain point. Max 300 chars.
                    """
                    res = client.models.generate_content(model=selected_model, contents=outreach_prompt)
                    st.markdown(f"### 📧 Personal Note for {name.strip()}")
                    st.code(res.text, language="markdown")
                except Exception as e:
                    st.error(f"Outreach Error: {e}")

# --- Tab 5: Application Builder (NEW) ---
with tab_builder:
    st.header("📝 Application Builder")
    st.write("Generate high-fidelity, tailored resumes and cover letters grounded in your 'Problem-Solver' profile.")
    
    if not st.session_state['career_vault']:
        st.warning("⚠️ Please seed your Career Vault in the 'Discovery Engine' tab first.")
    elif not st.session_state['last_jd_analyzed']:
        st.warning("⚠️ Please analyze a Job Description in the 'Command Center' tab first.")
    else:
        st.info(f"Building application for: **{st.session_state['detected_company']}**")
        
        if st.button("Generate Tailored Resume & Cover Letter"):
            with st.spinner("Synthesizing tailored application documents..."):
                try:
                    builder_prompt = f"""
                    You are a Jobberly Application Architect. Generate two documents tailored for this role.
                    
                    ### CANDIDATE VAULT (The Source of Truth):
                    {st.session_state['career_vault']}
                    
                    ### TARGET JOB DESCRIPTION:
                    {st.session_state['last_jd_analyzed']}
                    
                    ### DOCUMENT 1: TAILORED RESUME SUMMARY & KEY HIGHLIGHTS
                    - Create a 'Problem-Solver' Professional Summary.
                    - List 5 'High-Impact' Bullet points from the Vault, re-framed to bridge to the JD's specific pain points.
                    - Ensure the 'Core Bridge' is clearly visible to ATS and humans.
                    
                    ### DOCUMENT 2: STRATEGIC COVER LETTER
                    - Write a concise, 1st-person cover letter.
                    - Start by acknowledging a specific friction point or goal of the company (from JD/research).
                    - Explicitly link one of the candidate's verified wins to solving that friction point.
                    - End with a tactical call to action.
                    - DO NOT HALLUCINATE experience.
                    """
                    res = client.models.generate_content(model=selected_model, contents=builder_prompt)
                    st.markdown("---")
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"Builder Error: {e}")

# --- Tab 6: Market Tracking ---
with tab_track:
    st.header("Accountability Ledger")
    st.write("Track status and enforce the 'Feedback Escrow'.")
    tracking_data = pd.DataFrame({
        "Company": ["GlobalCorp", "TechStart"],
        "Status": ["Interview Scheduled", "Ghosted (Claim Filed)"],
        "Feedback Escrow": ["Locked", "Transferred to Seeker ($50)"]
    })
    st.table(tracking_data)
