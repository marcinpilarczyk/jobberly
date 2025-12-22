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
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'detected_company' not in st.session_state:
    st.session_state['detected_company'] = ""
if 'last_jd_analyzed' not in st.session_state:
    st.session_state['last_jd_analyzed'] = ""
if 'strategic_intel' not in st.session_state:
    st.session_state['strategic_intel'] = ""
if 'potential_managers' not in st.session_state:
    st.session_state['potential_managers'] = []
if 'final_resume' not in st.session_state:
    st.session_state['final_resume'] = ""
if 'final_cl' not in st.session_state:
    st.session_state['final_cl'] = ""

# 4. Sidebar: Identity, Metrics, and Persistent Vault Settings
with st.sidebar:
    st.title("🛡️ Jobberly")
    st.markdown("**The Candidate-Centric Employment Protocol**")
    st.divider()
    
    st.subheader("⚙️ Vault Settings")
    uploaded_file = st.file_uploader("Upload LinkedIn PDF to Seed Vault", type="pdf", key="vault_up")
    if uploaded_file:
        with st.spinner("Synchronizing professional identity..."):
            try:
                reader = pypdf.PdfReader(uploaded_file)
                raw_text = "".join([p.extract_text() for p in reader.pages])
                prompt = f"Parse this profile into a structured summary for a 'Problem-Solver' profile. Identify Seniority, Wins, and Skills. TEXT: {raw_text}"
                res = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
                st.session_state['career_vault'] = res.text
                st.success("Vault Active & Persistent.")
            except Exception as e:
                st.error(f"Seeding Error: {e}")
    
    if st.session_state['career_vault']:
        if st.button("🗑️ Delete Local Professional Identity"):
            st.session_state['career_vault'] = None
            st.rerun()
            
    st.divider()
    selected_model = st.selectbox("AI Model:", ["gemini-3-flash-preview", "gemini-3-pro-preview"], index=0)
    st.divider()
    st.metric("Hiring Reputation", "3.8/5", "-0.2")
    st.caption("Jobberly v3.7.4")

# 5. Main Application Tabs
tabs = st.tabs([
    "🚀 Discovery Engine", "🕵️ Command Center", "🧠 Strategic Intel", 
    "📧 Outreach Architect", "📝 Application Builder", "📊 Market Tracking"
])

# --- Tab 1: Discovery Engine ---
with tabs[0]:
    st.header("Achievement Refinement Agent")
    if not st.session_state['career_vault']:
        st.warning("⚠️ Access Denied: Seed your Career Vault in the sidebar to begin.")
    else:
        st.subheader("Current Profile Content")
        with st.expander("🔍 View Your Profile Wins & Skills", expanded=True):
            st.markdown(st.session_state['career_vault'])
            
        st.divider()
        st.subheader("Interactive Quantification Chat")
        st.write("Resumes often lack 'Problem-Solver' metrics. Let's quantify your vague claims.")

        for msg in st.session_state['chat_history']:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
        
        if chat := st.chat_input("Tell me about a project or win..."):
            st.session_state['chat_history'].append({"role": "user", "content": chat})
            with st.chat_message("user"): st.markdown(chat)
            with st.chat_message("assistant"):
                prompt = f"Using this profile: {st.session_state['career_vault']}, help the user quantify this claim: {chat}. Use the STAR method to ask one metric-focused question."
                res = client.models.generate_content(model=selected_model, contents=prompt)
                st.markdown(res.text)
                st.session_state['chat_history'].append({"role": "assistant", "content": res.text})

# --- Tab 2: Command Center ---
with tabs[1]:
    st.header("Forensic JD Scout")
    jd = st.text_area("Paste Job Description:", height=200, key="jd_in")
    if st.button("Analyze Trust DNA"):
        if jd:
            st.session_state['last_jd_analyzed'] = jd
            with st.spinner("Decoding intent signals..."):
                scout_prompt = f"Analyze for Trust, Internal-Hire DNA, and Budget. Identify the Company Name. JD: {jd}"
                res = client.models.generate_content(model=selected_model, contents=scout_prompt)
                st.markdown(res.text)
                comp_res = client.models.generate_content(model="gemini-3-flash-preview", contents=f"Extract only company name from: {res.text}")
                st.session_state['detected_company'] = comp_res.text.strip()

# --- Tab 3: Strategic Intel ---
with tabs[2]:
    st.header("Company Intelligence")
    target = st.text_input("Target Company:", value=st.session_state['detected_company'], key="intel_t")
    if st.button("Research Pain Points"):
        if target:
            prompt = f"Identify 3 'Bleeding Neck' pain points and 5 strategic control questions for {target}. Context: {st.session_state['career_vault']}"
            res = client.models.generate_content(model=selected_model, contents=prompt)
            st.session_state['strategic_intel'] = res.text
            st.write(res.text)

# --- Tab 4: Outreach Architect ---
with tabs[3]:
    st.header("Outreach Architect")
    target_comp = st.text_input("Company:", value=st.session_state['detected_company'], key="out_comp")
    if st.button("Identify Decision Makers"):
        if target_comp:
            res = client.models.generate_content(model=selected_model, contents=f"Identify 2 managers at {target_comp} by NAME | TITLE.")
            st.session_state['potential_managers'] = [m.strip() for m in res.text.split('\n') if "|" in m]
    
    sel = st.selectbox("Target Manager:", st.session_state['potential_managers'] if st.session_state['potential_managers'] else ["(Perform research)"])
    if st.button("Draft 1st-Person Note"):
        if "|" in sel:
            n, t = sel.split("|")
            prompt = f"Write 1st-person LinkedIn note (max 300 chars) to {n} ({t}) at {target_comp}. Grounded ONLY in Vault: {st.session_state['career_vault']}"
            res = client.models.generate_content(model=selected_model, contents=prompt)
            st.code(res.text)

# --- Tab 5: Application Builder ---
with tabs[4]:
    st.header("📝 Application Builder")
    if st.session_state['career_vault'] and st.session_state['last_jd_analyzed']:
        region = st.radio("Geopolitical Standard:", ["US Resume", "European CV"])
            
        if st.button("Generate Grounded Application"):
            with st.spinner("Bridging Vault to opportunity..."):
                builder_prompt = f"""
                Generate a FULL Resume (Markdown) and a PLAIN TEXT Cover Letter.
                GEOGRAPHY: {region}
                VAULT: {st.session_state['career_vault']}
                JD: {st.session_state['last_jd_analyzed']}
                INTEL: {st.session_state['strategic_intel']}
                RULES: 
                1. US: Marketing brochure model, no photo, action-oriented. 
                2. EU: Comprehensive record, 2 pages, photo placeholders.
                3. NO HALLUCINATIONS: Grounded strictly in vault.
                4. Cover Letter: PLAIN TEXT ONLY. No formatting.
                Split docs with '|||'.
                """
                res = client.models.generate_content(model=selected_model, contents=builder_prompt)
                parts = res.text.split("|||")
                st.session_state['final_resume'] = parts[0].strip() if len(parts) > 0 else res.text
                st.session_state['final_cl'] = parts[1].strip() if len(parts) > 1 else ""

        if st.session_state['final_resume']:
            st.subheader("Tailored Resume (Markdown)")
            st.info("💡 Copy the code block below directly into Google Docs or Word. (Google Docs: Tools > Preferences > Enable Markdown)")
            st.code(st.session_state['final_resume'], language="markdown")
            
            st.divider()
            
            st.subheader("Strategic Cover Letter (Plain Text)")
            st.text_area("Final Cover Letter", st.session_state['final_cl'], height=250)
            
            st.success("Application generated. Content is now ready for copy-pasting.")
    else:
        st.warning("⚠️ Seed Vault and analyze a JD first.")

# --- Tab 6: Tracking ---
with tabs[5]:
    st.header("📊 Market Ledger")
    st.table(pd.DataFrame({"Company": [st.session_state['detected_company'] if st.session_state['detected_company'] else "Pending"], "Status": ["Documents Ready" if st.session_state['final_resume'] else "Analyzing"], "Escrow": ["Active"]}))
