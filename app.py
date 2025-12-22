import streamlit as st
from google import genai
import pypdf
import pandas as pd
from fpdf import FPDF

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

# 4. Sidebar: Persistent Vault & Identity Settings
with st.sidebar:
    st.title("🛡️ Jobberly")
    st.markdown("**The Candidate-Centric Employment Protocol**")
    st.divider()
    
    st.subheader("⚙️ Vault Settings")
    uploaded_file = st.file_uploader("Seed/Update Vault (LinkedIn PDF)", type="pdf", key="vault_up")
    if uploaded_file:
        with st.spinner("Processing professional identity..."):
            try:
                reader = pypdf.PdfReader(uploaded_file)
                raw_text = "".join([p.extract_text() for p in reader.pages])
                prompt = f"Summarize this professional profile into a 'Problem-Solver' asset: {raw_text}"
                res = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
                st.session_state['career_vault'] = res.text
                st.success("Vault Synchronized.")
            except Exception as e:
                st.error(f"Seeding Error: {e}")
    
    if st.session_state['career_vault']:
        if st.button("🗑️ Wipe Career Vault"):
            st.session_state['career_vault'] = None
            st.rerun()
            
    st.divider()
    selected_model = st.selectbox("AI Model:", ["gemini-3-flash-preview", "gemini-3-pro-preview"], index=0)
    st.divider()
    st.metric("Hiring Reputation", "3.8/5", "-0.2")
    st.caption("Jobberly v3.6.0")

# --- PDF Generation Helper ---
def export_as_pdf(resume_text, cl_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, "--- TAILORED RESUME ---")
    pdf.multi_cell(0, 10, resume_text)
    pdf.add_page()
    pdf.multi_cell(0, 10, "--- STRATEGIC COVER LETTER ---")
    pdf.multi_cell(0, 10, cl_text)
    return pdf.output()

# 5. Main Application Tabs
tabs = st.tabs([
    "🚀 Discovery Engine", "🕵️ Command Center", "🧠 Strategic Intel", 
    "📧 Outreach Architect", "📝 Application Builder", "📊 Market Tracking"
])

# --- Tab 1: Discovery Engine ---
with tabs[0]:
    st.header("Achievement Refinement Agent")
    if not st.session_state['career_vault']:
        st.warning("Please seed your Vault in the sidebar to begin.")
    else:
        for msg in st.session_state['chat_history']:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
        
        if chat := st.chat_input("Explain a win..."):
            st.session_state['chat_history'].append({"role": "user", "content": chat})
            with st.chat_message("user"): st.markdown(chat)
            with st.chat_message("assistant"):
                prompt = f"Help user quantify this win for their vault: {chat}. Ask one metric-focused question."
                res = client.models.generate_content(model=selected_model, contents=prompt)
                st.markdown(res.text)
                st.session_state['chat_history'].append({"role": "assistant", "content": res.text})

# --- Tab 2: Command Center ---
with tabs[1]:
    st.header("Forensic JD Scout")
    jd = st.text_area("Paste JD:", height=200, key="jd_in")
    if st.button("Analyze Trust DNA"):
        if jd:
            st.session_state['last_jd_analyzed'] = jd
            res = client.models.generate_content(model=selected_model, contents=f"Analyze for Trust, Internal-Hire DNA, and Budget. CLEARLY IDENTIFY COMPANY NAME. JD: {jd}")
            st.markdown(res.text)
            comp_res = client.models.generate_content(model="gemini-3-flash-preview", contents=f"Extract only company name from: {res.text}")
            st.session_state['detected_company'] = comp_res.text.strip()

# --- Tab 3: Strategic Intel ---
with tabs[2]:
    st.header("Company Intelligence")
    target = st.text_input("Target Company:", value=st.session_state['detected_company'], key="intel_t")
    if st.button("Research Pain Points"):
        if target:
            prompt = f"Identify 3 'Bleeding Neck' pain points and 5 control questions for {target}. Vault: {st.session_state['career_vault']}"
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
    
    sel = st.selectbox("Target:", st.session_state['potential_managers'] if st.session_state['potential_managers'] else ["(Perform research)"])
    if st.button("Draft 1st-Person Note"):
        if "|" in sel:
            n, t = sel.split("|")
            prompt = f"Write 1st-person note to {n} ({t}) at {target_comp}. Grounded in Vault: {st.session_state['career_vault']}"
            res = client.models.generate_content(model=selected_model, contents=prompt)
            st.code(res.text)

# --- Tab 5: Application Builder ---
with tabs[4]:
    st.header("Application Builder")
    if st.session_state['career_vault'] and st.session_state['last_jd_analyzed']:
        region = st.radio("Resume Geography:", ["US Resume", "European CV"])
        if st.button("Generate Tailored Application"):
            with st.spinner("Bridging Vault to opportunity..."):
                prompt = f"""
                You are a Jobberly Architect. Generate a FULL Resume and Plain Text Cover Letter.
                GEOGRAPHY: {region}
                VAULT: {st.session_state['career_vault']}
                JD: {st.session_state['last_jd_analyzed']}
                INTEL: {st.session_state['strategic_intel']}
                
                ### ARCHITECTURE RULES:
                - US: Marketing brochure, reverse-chronological, NO personal data/photo, action-oriented.
                - EU: Historical record, formal, granular education, include placeholders for personal data (photo/DOB).
                - GENERAL: Use STAR/XYZ metrics. Use single-column layout. NO HALLUCINATIONS. 
                - If no metrics in vault, insert [METRIC] placeholder.
                - Cover Letter: STRICT PLAIN TEXT. NO bold, italics, or bullets.
                Split documents with '|||'.
                """
                res = client.models.generate_content(model=selected_model, contents=prompt)
                parts = res.text.split("|||")
                st.session_state['final_resume'] = parts[0].strip() if len(parts) > 0 else res.text
                st.session_state['final_cl'] = parts[1].strip() if len(parts) > 1 else ""

        if st.session_state['final_resume']:
            st.session_state['final_resume'] = st.text_area("Edit Resume", st.session_state['final_resume'], height=300)
            st.session_state['final_cl'] = st.text_area("Edit Cover Letter (Plain Text)", st.session_state['final_cl'], height=200)
            
            pdf_bytes = export_as_pdf(st.session_state['final_resume'], st.session_state['final_cl'])
            st.download_button("📥 Download PDF for Application", pdf_bytes, file_name="Jobberly_Application.pdf", mime="application/pdf")
    else:
        st.warning("Ensure Vault is seeded and JD is analyzed.")

# --- Tab 6: Tracking ---
with tabs[5]:
    st.header("Accountability Ledger")
    st.table(pd.DataFrame({"Company": [st.session_state['detected_company']], "Status": ["Drafting Ready"], "Escrow": ["Active"]}))
