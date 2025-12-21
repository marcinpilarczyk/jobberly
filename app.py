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

# 3. Session State Initialization (Persistence & Cross-Tab Intelligence)
if 'career_vault' not in st.session_state:
    st.session_state['career_vault'] = None
if 'detected_company' not in st.session_state:
    st.session_state['detected_company'] = ""
if 'last_jd_analyzed' not in st.session_state:
    st.session_state['last_jd_analyzed'] = ""
if 'strategic_intel' not in st.session_state:
    st.session_state['strategic_intel'] = ""
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
        index=0
    )
    st.divider()
    
    if st.session_state['career_vault']:
        st.status("Career Vault: Active", state="complete")
        if st.button("🔄 Reset Vault"):
            st.session_state['career_vault'] = None
            st.rerun()
    else:
        st.status("Vault: Awaiting Seed", state="error")
    
    st.metric("Global Hiring Reputation", "3.8/5", "-0.2")
    st.divider()
    st.subheader("💳 Support")
    st.markdown("[Pay What You Can (Lemon Squeezy)](#)")
    st.caption("Jobberly v3.1.0 (Integrated Forensics)")

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

# --- Tab 1: Discovery Engine ---
with tabs[0]:
    st.header("1. Build Your Proof-Based Vault")
    label = "Seed Vault (LinkedIn PDF)" if not st.session_state['career_vault'] else "Update Vault (New PDF)"
    uploaded_file = st.file_uploader(label, type="pdf")
    
    if uploaded_file:
        with st.spinner("Processing professional DNA..."):
            try:
                reader = pypdf.PdfReader(uploaded_file)
                full_text = "".join([page.extract_text() for page in reader.pages])
                prompt = f"Parse this profile into a structured 'Problem-Solver' summary (Seniority, Skills, Wins, Achievements). TEXT: {full_text}"
                response = client.models.generate_content(model=selected_model, contents=prompt)
                st.session_state['career_vault'] = response.text
                st.success("Vault Synchronized.")
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state['career_vault']:
        st.divider()
        st.subheader("2. AI Interactive Interview")
        chat_input = st.chat_input("Tell the Advocate about a major win...")
        if chat_input:
            with st.chat_message("assistant"):
                interview_prompt = f"Context: {st.session_state['career_vault']}. Claim: '{chat_input}'. Ask a probing question for forensic metrics."
                res = client.models.generate_content(model=selected_model, contents=interview_prompt)
                st.write(res.text)

# --- Tab 2: Command Center ---
with tabs[1]:
    st.header("The Deception Decoder")
    jd_text = st.text_area("Paste Job Description (JD):", height=200, key="scout_jd")
    if st.button("Generate Trust Report"):
        if jd_text:
            st.session_state['last_jd_analyzed'] = jd_text
            with st.spinner("Analyzing intent..."):
                scout_prompt = f"Analyze this JD for Trust Score, Red Flags, Internal-Hire DNA, and Budget. Identify Company Name. JD: {jd_text}"
                res = client.models.generate_content(model=selected_model, contents=scout_prompt)
                st.markdown(res.text)
                if "**Company Name**:" in res.text:
                    st.session_state['detected_company'] = res.text.split("**Company Name**:")[1].strip().split("\n")[0]

# --- Tab 3: Strategic Intel ---
with tabs[2]:
    st.header("Strategic Intelligence")
    comp_name = st.text_input("Target Company:", value=st.session_state['detected_company'])
    if st.button("Generate Intelligence Map"):
        if comp_name:
            with st.spinner(f"Researching {comp_name}..."):
                intel_prompt = f"Research {comp_name}. Identify Stage, 'Bleeding Neck' Pain Points, and 5 Strategic Control Questions. Context: {st.session_state['career_vault']}"
                res = client.models.generate_content(model=selected_model, contents=intel_prompt)
                st.session_state['strategic_intel'] = res.text
                st.markdown(f"### 🧠 {comp_name} Intelligence Map")
                st.write(res.text)

# --- Tab 4: Outreach Architect ---
with tabs[3]:
    st.header("LinkedIn Outreach")
    outreach_comp = st.text_input("Target Company:", value=st.session_state['detected_company'], key="out_comp")
    if st.button("Identify Decision Makers"):
        if outreach_comp:
            res = client.models.generate_content(model=selected_model, contents=f"Identify 2 managers at {outreach_comp}. Format: Name | Title")
            st.session_state['potential_managers'] = [m.strip() for m in res.text.split('\n') if "|" in m]
    
    selected_target = st.selectbox("Select Target:", options=st.session_state['potential_managers'] if st.session_state['potential_managers'] else ["(Perform research)"])
    if st.button("Generate Note"):
        if selected_target and "|" in selected_target:
            name, title = selected_target.split("|")
            out_prompt = f"1st-person note to {name.strip()} ({title.strip()}) at {outreach_comp}. Grounded in Vault: {st.session_state['career_vault']}. Max 300 chars."
            res = client.models.generate_content(model=selected_model, contents=out_prompt)
            st.code(res.text, language="markdown")

# --- Tab 5: Application Builder (Integrated & Copy-Paste) ---
with tabs[4]:
    st.header("📝 Application Builder")
    if not st.session_state['career_vault'] or not st.session_state['last_jd_analyzed']:
        st.warning("⚠️ Complete 'Discovery Engine' and 'Command Center' first.")
    else:
        st.info(f"Target: **{st.session_state['detected_company']}**")
        if st.button("Generate Copy-Paste Application"):
            with st.spinner("Executing Strategic Overfitting..."):
                builder_prompt = f"""
                You are a Jobberly Application Architect. Generate a copy-paste resume and cover letter.
                
                ### DATA SOURCES:
                - CANDIDATE VAULT (Verified Wins): {st.session_state['career_vault']}
                - TARGET JD (Forensic DNA): {st.session_state['last_jd_analyzed']}
                - STRATEGIC INTEL (Pain Points): {st.session_state['strategic_intel']}
                
                ### INSTRUCTIONS:
                1. Use 'Strategic Overfitting'[cite: 52]: Mirror the JD's semantic and syntactic complexity to ensure alignment.
                2. Position as a 'Problem-Solver'[cite: 10]: Bridge vault achievements directly to the company's 'bleeding neck' pain points.
                3. First-Person POV: Use 'I' and 'my' to build human connection.
                4. Formatting: Use clear Markdown headers.
                
                ### OUTPUT:
                - **RESUME HIGHLIGHTS**: (Summary + 5 forensic bullet points)
                - **STRATEGIC COVER LETTER**: (Grounded in pain points and verified wins)
                """
                res = client.models.generate_content(model=selected_model, contents=builder_prompt)
                st.markdown("---")
                st.markdown(res.text)

# --- Tab 6: Market Tracking ---
with tabs[5]:
    st.header("Accountability Ledger")
    st.table(pd.DataFrame({"Company": ["GlobalCorp"], "Status": ["Interview"], "Escrow": ["Locked"]}))
