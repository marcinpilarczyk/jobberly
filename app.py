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

# 3. Session State Initialization (Persistence Logic)
if 'career_vault' not in st.session_state:
    st.session_state['career_vault'] = None
if 'detected_company' not in st.session_state:
    st.session_state['detected_company'] = ""
if 'last_jd_analyzed' not in st.session_state:
    st.session_state['last_jd_analyzed'] = ""
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
        help="Choose the next-generation model for forensic analysis and document generation."
    )
    
    st.divider()
    
    # Persistent Vault Status
    if st.session_state['career_vault']:
        st.status("Career Vault: Active & Persistent", state="complete")
        if st.button("🔄 Wipe Vault (Reset Protocol)"):
            st.session_state['career_vault'] = None
            st.rerun()
    else:
        st.status("Career Vault: Awaiting Initial Seed", state="error")
    
    st.metric("Global Hiring Reputation", "3.8/5", "-0.2")
    
    st.divider()
    st.subheader("💳 Support the Protocol")
    st.markdown("[Pay What You Can (Lemon Squeezy)](#)")
    st.caption("Jobberly v3.0.0 (Grounded Applications)")

# 5. Main Application Interface
st.title("🛡️ Jobseeker Advocate Suite")

tabs = st.tabs([
    "🚀 Discovery Engine", 
    "🕵️ Command Center", 
    "🧠 Strategic Intel", 
    "📧 Outreach Architect",
    "📝 Application Builder",
    "📊 Market Tracking"
])

# --- Tab 1: Discovery Engine (Import Once, Update Often) ---
with tabs[0]:
    st.header("1. Build & Maintain Your Proof-Based Vault")
    
    if not st.session_state['career_vault']:
        st.write("LinkedIn -> More... -> Save to PDF. Seed your vault to begin.")
        label = "Seed Vault with LinkedIn PDF"
    else:
        st.write("Your vault is active. Upload a new PDF to **update** your history and skills.")
        label = "Update Vault with New PDF"
    
    uploaded_file = st.file_uploader(label, type="pdf")
    
    if uploaded_file:
        with st.spinner(f"Processing professional DNA with {selected_model}..."):
            try:
                reader = pypdf.PdfReader(uploaded_file)
                full_text = "".join([page.extract_text() for page in reader.pages])
                
                # Context-aware parsing focusing on wins and seniority
                prompt = f"""
                You are a Career Data Architect. Parse this LinkedIn profile into a structured 'Problem-Solver' profile.
                IDENTIFY: 
                1. Seniority Level and years of experience.
                2. Hard Technical Skills and specific tool stacks.
                3. Quantifiable Achievements (revenue, burn rate impact, or speed efficiency).
                4. Strategic Strengths.
                
                TEXT: {full_text}
                """
                response = client.models.generate_content(model=selected_model, contents=prompt)
                
                # Append or Update logic
                if st.session_state['career_vault']:
                    st.session_state['career_vault'] += f"\n\n--- UPDATED PROFILE DATA ---\n{response.text}"
                    st.success("Vault updated successfully!")
                else:
                    st.session_state['career_vault'] = response.text
                    st.success("Vault seeded. Welcome to the Verification-First protocol.")
            except Exception as e:
                st.error(f"Error processing vault: {e}")

    if st.session_state['career_vault']:
        st.divider()
        st.subheader("2. AI Interactive Interview")
        with st.expander("View Your Current Problem-Solver Profile"):
            st.write(st.session_state['career_vault'])
        
        chat_input = st.chat_input("Tell the Advocate about a major win at your last job...")
        if chat_input:
            with st.chat_message("assistant"):
                try:
                    interview_prompt = (
                        f"Context: {st.session_state['career_vault']}. "
                        f"The candidate claims: '{chat_input}'. "
                        "Ask one probing, evidence-based question to uncover the forensic impact metrics."
                    )
                    res = client.models.generate_content(model=selected_model, contents=interview_prompt)
                    st.write(res.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")

# --- Tab 2: Command Center (Forensic Trust Report) ---
with tabs[1]:
    st.header("The Deception Decoder")
    st.write("Analyze listings for 'Ghost Jobs' and 'Compliance Theater'[cite: 13, 67].")
    
    jd_text = st.text_area("Paste a Job Description (JD):", height=200, key="scout_jd")
    if st.button("Generate Trust Report"):
        if jd_text:
            st.session_state['last_jd_analyzed'] = jd_text
            with st.spinner("Decoding intent signals..."):
                try:
                    scout_prompt = f"""
                    Analyze this JD using the Jobberly Protocol. 
                    - Scan for Internal-Hire DNA (Compliance Theater)[cite: 13].
                    - Predict Budget based on seniority from vault: {st.session_state['career_vault'] if st.session_state['career_vault'] else "No vault data."}
                    - Identify the Company Name.
                    
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
            st.warning("Please paste a job description.")

# --- Tab 3: Strategic Intel (Enhanced Control) ---
with tabs[2]:
    st.header("Strategic Intelligence")
    comp_name = st.text_input("Target Company Name:", value=st.session_state['detected_company'])
    if st.button("Generate Intelligence Map"):
        if comp_name:
            with st.spinner(f"Researching {comp_name}..."):
                try:
                    intel_prompt = f"""
                    Research {comp_name} to empower the candidate. 
                    Identify 'Bleeding Neck' pain points and 5 Strategic Control Questions to lead the interview.
                    Candidate context: {st.session_state['career_vault']}
                    """
                    res = client.models.generate_content(model=selected_model, contents=intel_prompt)
                    st.markdown(f"### 🧠 {comp_name} Intelligence Map")
                    st.write(res.text)
                except Exception as e:
                    st.error(f"Intel Error: {e}")

# --- Tab 4: Outreach Architect (Grounded Name Ident.) ---
with tabs[3]:
    st.header("LinkedIn Outreach Architect")
    outreach_comp = st.text_input("Target Company:", value=st.session_state['detected_company'], key="outreach_comp")
    
    if st.button("Identify Decision Makers by Name"):
        if outreach_comp:
            with st.spinner("Identifying targets..."):
                try:
                    manager_prompt = f"Identify 2 likely hiring managers at {outreach_comp} by NAME and TITLE. Format: Name | Title"
                    res = client.models.generate_content(model=selected_model, contents=manager_prompt)
                    st.session_state['potential_managers'] = [m.strip() for m in res.text.split('\n') if "|" in m]
                    st.success("Targets identified.")
                except Exception as e:
                    st.error(f"Identification Error: {e}")
    
    selected_target = st.selectbox("Select Target:", options=st.session_state['potential_managers'] if st.session_state['potential_managers'] else ["(Perform identification first)"])
    
    if st.button("Generate Grounded Outreach"):
        if selected_target and "|" in selected_target:
            with st.spinner("Synthesizing personal win..."):
                try:
                    name, title = selected_target.split("|")
                    outreach_prompt = f"""
                    Write a 1st-person LinkedIn note (max 300 chars) to {name.strip()} ({title.strip()}).
                    STRICT GROUNDING: Use ONLY wins/skills from this vault: {st.session_state['career_vault']}
                    Address a likely pain point for {outreach_comp}.
                    """
                    res = client.models.generate_content(model=selected_model, contents=outreach_prompt)
                    st.markdown(f"### 📧 Personal Pitch for {name.strip()}")
                    st.code(res.text, language="markdown")
                except Exception as e:
                    st.error(f"Outreach Error: {e}")

# --- Tab 5: Application Builder (NEW: Tailored Application) ---
with tabs[4]:
    st.header("📝 Application Builder")
    st.write("Generate a tailored resume and cover letter grounded in your verified history.")
    
    if not st.session_state['career_vault']:
        st.warning("⚠️ Seed your Career Vault in 'Discovery Engine' first.")
    elif not st.session_state['last_jd_analyzed']:
        st.warning("⚠️ Analyze a Job Description in 'Command Center' first.")
    else:
        st.info(f"Targeting role at: **{st.session_state['detected_company']}**")
        
        if st.button("Generate Tailored Resume & Cover Letter"):
            with st.spinner("Bridging profile to opportunity..."):
                try:
                    builder_prompt = f"""
                    You are a Jobberly Application Architect. Generate two grounded documents.
                    
                    ### CANDIDATE VAULT:
                    {st.session_state['career_vault']}
                    
                    ### TARGET JD:
                    {st.session_state['last_jd_analyzed']}
                    
                    ### INSTRUCTIONS:
                    1. RESUME: Create a 'Problem-Solver' summary and 5 high-impact bullets re-framed for this JD's requirements. Use 1st person.
                    2. COVER LETTER: Write a strategic, personal letter (1st person) starting with the company's 'bleeding neck' and offering your verified win as the solution.
                    3. ZERO HALLUCINATION: Only use skills and experience found in the Vault.
                    """
                    res = client.models.generate_content(model=selected_model, contents=builder_prompt)
                    st.markdown("---")
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"Builder Error: {e}")

# --- Tab 6: Market Tracking ---
with tabs[5]:
    st.header("Accountability Ledger")
    tracking_data = pd.DataFrame({
        "Company": ["GlobalCorp", "TechStart"],
        "Status": ["Interview Scheduled", "Ghosted (Claim Filed)"],
        "Feedback Escrow": ["Locked", "Transferred to Seeker ($50)"]
    })
    st.table(tracking_data)
