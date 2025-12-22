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
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'detected_company' not in st.session_state:
    st.session_state['detected_company'] = ""
if 'last_jd_analyzed' not in st.session_state:
    st.session_state['last_jd_analyzed'] = ""
if 'strategic_intel' not in st.session_state:
    st.session_state['strategic_intel'] = ""
if 'generated_resume' not in st.session_state:
    st.session_state['generated_resume'] = ""
if 'generated_cover_letter' not in st.session_state:
    st.session_state['generated_cover_letter'] = ""

# 4. Sidebar: Identity, Metrics, and NEW Persistent Settings
with st.sidebar:
    st.title("🛡️ Jobberly")
    st.markdown("**The Candidate-Centric Employment Protocol**")
    st.divider()
    
    # --- VAULT SETTINGS (Persistent Upload) ---
    st.subheader("⚙️ Vault Settings")
    if not st.session_state['career_vault']:
        st.info("Your Career Vault is empty. Seed it with your LinkedIn PDF to begin.")
    
    uploaded_file = st.file_uploader("Upload LinkedIn PDF", type="pdf", key="vault_uploader")
    
    if uploaded_file:
        with st.spinner("Forensically seeding your Career Vault..."):
            try:
                reader = pypdf.PdfReader(uploaded_file)
                full_text = "".join([page.extract_text() for page in reader.pages])
                # Protocol: Identify seniority and key metrics initially 
                prompt = f"Parse this profile into a structured summary focusing on Seniority, Skills, and specific Wins. TEXT: {full_text}"
                response = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
                st.session_state['career_vault'] = response.text
                st.success("Vault Synchronized and Persistent.")
            except Exception as e:
                st.error(f"Seeding failed: {e}")
    
    if st.session_state['career_vault']:
        if st.button("🗑️ Delete Professional Identity"):
            st.session_state['career_vault'] = None
            st.rerun()
            
    st.divider()
    st.subheader("🤖 AI Model")
    selected_model = st.selectbox("Tier:", ["gemini-3-flash-preview", "gemini-3-pro-preview"], index=0)
    
    st.divider()
    st.metric("Global Hiring Reputation", "3.8/5", "-0.2")
    st.caption("Jobberly v3.4.0 (Conversational Refinement)")

# 5. Main Application Interface
tabs = st.tabs([
    "🚀 Discovery Engine", 
    "🕵️ Command Center", 
    "🧠 Strategic Intel", 
    "📧 Outreach Architect",
    "📝 Application Builder",
    "📊 Market Tracking"
])

# --- Tab 1: Discovery Engine (Conversational Refinement) ---
with tabs[0]:
    st.header("🚀 The Discovery Engine")
    
    if not st.session_state['career_vault']:
        st.warning("⚠️ Access Denied: Please seed your Career Vault in the Sidebar Settings to proceed.")
    else:
        st.subheader("Interactive Achievement Refinement")
        st.write("Resumes often fail because they lack 'Problem-Solver' metrics. Let's quantify your wins.")
        
        # Display Current Vault Analysis
        with st.expander("🔍 View Profile Analysis"):
            st.write(st.session_state['career_vault'])

        st.divider()
        
        # Chat Interface for Quantification
        for message in st.session_state['chat_history']:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Explain a recent project or win..."):
            st.session_state['chat_history'].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # Protocol: Ask probing questions to uncover impact on burn rate/revenue [cite: 1, 190]
                refinement_prompt = f"""
                You are the Jobberly Achievement Architect. 
                VAULT CONTEXT: {st.session_state['career_vault']}
                USER INPUT: {prompt}
                
                Your goal is to help the user quantify this achievement. 
                1. Identify what is vague (e.g., 'improved efficiency').
                2. Ask one specific, conversational question to find the metric (e.g., 'By what % did efficiency increase?' or 'How many hours did the team save per week?').
                3. Focus on corporate pain points: Burn rate, revenue impact, or operational speed.
                """
                response = client.models.generate_content(model=selected_model, contents=refinement_prompt)
                st.markdown(response.text)
                st.session_state['chat_history'].append({"role": "assistant", "content": response.text})

# --- Tab 2: Command Center (Forensic Trust Report) ---
with tabs[1]:
    st.header("🕵️ Command Center")
    st.write("Analyze listings for 'Ghost Jobs' and 'Compliance Theater'[cite: 5, 66].")
    
    jd_text = st.text_area("Paste Job Description (JD):", height=200, key="scout_jd")
    if st.button("Generate Trust Report"):
        if jd_text:
            st.session_state['last_jd_analyzed'] = jd_text
            with st.spinner("Decoding intent signals..."):
                try:
                    scout_prompt = f"Analyze this JD using the Jobberly Protocol for Trust Score, Red Flags, Internal-Hire DNA, and Budget. JD: {jd_text}"
                    res = client.models.generate_content(model=selected_model, contents=scout_prompt)
                    st.markdown("---")
                    st.markdown(res.text)
                    if "**Company Name**:" in res.text:
                        st.session_state['detected_company'] = res.text.split("**Company Name**:")[1].strip().split("\n")[0]
                except Exception as e:
                    st.error(f"Analysis Error: {e}")

# --- Tab 3: Strategic Intel ---
with tabs[2]:
    st.header("🧠 Strategic Intel")
    comp_name = st.text_input("Target Company:", value=st.session_state['detected_company'])
    if st.button("Generate Intelligence Map"):
        if comp_name:
            with st.spinner(f"Researching {comp_name}..."):
                intel_prompt = f"Research {comp_name}. Identify Stage, 'Bleeding Neck' Pain Points, and 5 Strategic Control Questions. Context: {st.session_state['career_vault']}"
                res = client.models.generate_content(model=selected_model, contents=intel_prompt)
                st.session_state['strategic_intel'] = res.text
                st.write(res.text)

# --- Tab 4: Outreach Architect ---
with tabs[3]:
    st.header("📧 Outreach Architect")
    if st.button("Identify Decision Makers"):
        if st.session_state['detected_company']:
            res = client.models.generate_content(model=selected_model, contents=f"Identify 2 likely managers at {st.session_state['detected_company']} by NAME | TITLE.")
            st.session_state['potential_managers'] = [m.strip() for m in res.text.split('\n') if "|" in m]
    
    selected_target = st.selectbox("Select Target:", options=st.session_state['potential_managers'] if st.session_state['potential_managers'] else ["(Perform research)"])
    if st.button("Generate Note"):
        if selected_target and "|" in selected_target:
            name, title = selected_target.split("|")
            out_prompt = f"1st-person note to {name.strip()} ({title.strip()}) at {st.session_state['detected_company']}. Grounded in Vault: {st.session_state['career_vault']}. Max 300 chars."
            res = client.models.generate_content(model=selected_model, contents=out_prompt)
            st.code(res.text, language="markdown")

# --- Tab 5: Application Builder (Interactive & Grounded) ---
with tabs[4]:
    st.header("📝 Application Builder")
    if not st.session_state['career_vault'] or not st.session_state['last_jd_analyzed']:
        st.warning("⚠️ Complete Vault seeding and JD analysis first.")
    else:
        if st.button("Generate Draft Application"):
            with st.spinner("Bridging Vault wins to JD pain points..."):
                builder_prompt = f"""
                Generate a full Resume and a Plain-Text Cover Letter. 
                Grounded in Vault: {st.session_state['career_vault']}
                Target JD: {st.session_state['last_jd_analyzed']}
                Strategy: {st.session_state['strategic_intel']}
                Use 'Strategic Overfitting' [cite: 52-53]. Cover letter must be PLAIN TEXT ONLY.
                """
                res = client.models.generate_content(model=selected_model, contents=builder_prompt)
                st.markdown(res.text)

# --- Tab 6: Market Tracking ---
with tabs[5]:
    st.header("📊 Market Tracking")
    st.table(pd.DataFrame({"Company": [st.session_state['detected_company']], "Status": ["Grounded Draft Ready"], "Escrow": ["Active"]}))
