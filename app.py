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

# --- CONSTANTS: Unified Report Protocol ---
REPORT_PROTOCOL_HINT = """
STRICT FORMATTING RULE: 
Return your response using this Markdown structure:
### 🛡️ [REPORT TITLE]
---
**SUMMARY:** (1-2 sentence overview)
**ANALYSIS:** (Key data points/findings)
**ACTIONABLE INTEL:** (Specific next steps or questions)
DO NOT include citations or markdown artifacts like.
"""

# --- HELPER: PDF Generation & Sanitization ---
def sanitize_for_pdf(text):
    """Replaces Unicode characters causing EncodingErrors in standard PDF fonts."""
    replacements = {
        '\u2013': '-', '\u2014': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2022': '*', '\u2026': '...'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'ignore').decode('latin-1')

def export_as_pdf(resume_text, cl_text):
    """Generates a binary PDF buffer for download."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    clean_resume = sanitize_for_pdf(resume_text)
    clean_cl = sanitize_for_pdf(cl_text)
    
    # Page 1: Resume
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "TAILORED RESUME", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, clean_resume)
    
    # Page 2: Cover Letter
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "STRATEGIC COVER LETTER", ln=True, align='C')
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, clean_cl)
    
    return bytes(pdf.output())

# 4. Sidebar
with st.sidebar:
    st.title("🛡️ Jobberly")
    st.markdown("**The Candidate-Centric Employment Protocol**")
    st.divider()
    
    st.subheader("⚙️ Vault Settings")
    uploaded_file = st.file_uploader("Seed/Update Career Vault (LinkedIn PDF)", type="pdf", key="vault_up")
    if uploaded_file:
        with st.spinner("Synchronizing professional identity..."):
            try:
                reader = pypdf.PdfReader(uploaded_file)
                raw_text = "".join([p.extract_text() for p in reader.pages])
                prompt = f"Parse this profile. Identify Seniority, specific Metric Wins, and Core Skills. {REPORT_PROTOCOL_HINT} TITLE: VAULT SYNCHRONIZATION. TEXT: {raw_text}"
                res = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
                st.session_state['career_vault'] = res.text
                st.success("Vault Synchronized.")
            except Exception as e:
                st.error(f"Seeding Error: {e}")
    
    if st.session_state['career_vault']:
        if st.button("🗑️ Delete Professional Identity"):
            st.session_state['career_vault'] = None
            st.rerun()
            
    st.divider()
    selected_model = st.selectbox("AI Model Tier:", ["gemini-3-flash-preview", "gemini-3-pro-preview"], index=0)
    st.divider()
    st.metric("Global Hiring Reputation", "3.8/5", "-0.2")
    st.caption("Jobberly v3.8.0")

# 5. Main Application Interface
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
        st.subheader("Current Vault Analysis")
        with st.expander("🔍 View Profile Wins & Skills", expanded=True):
            st.markdown(st.session_state['career_vault'])
            
        st.divider()
        st.subheader("Quantification Chat")
        
        for msg in st.session_state['chat_history']:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
        
        if chat := st.chat_input("Tell the Advocate about a project or win..."):
            st.session_state['chat_history'].append({"role": "user", "content": chat})
            with st.chat_message("user"): st.markdown(chat)
            with st.chat_message("assistant"):
                prompt = f"""
                Using this profile: {st.session_state['career_vault']}, help the user quantify this win: {chat}. 
                {REPORT_PROTOCOL_HINT} 
                TITLE: ACHIEVEMENT REFINEMENT
                IN ANALYSIS: Use the STAR method to break down the input.
                IN ACTIONABLE INTEL: Ask ONE metric-focused question.
                """
                res = client.models.generate_content(model=selected_model, contents=prompt)
                st.markdown(res.text)
                st.session_state['chat_history'].append({"role": "assistant", "content": res.text})

# --- Tab 2: Command Center ---
with tabs[1]:
    st.header("Forensic JD Scout")
    jd = st.text_area("Paste Job Description (JD):", height=200, key="jd_in")
    if st.button("Analyze Trust DNA"):
        if jd:
            st.session_state['last_jd_analyzed'] = jd
            with st.spinner("Decoding intent signals..."):
                try:
                    scout_prompt = f"""
                    Analyze this JD for Trust Score, Ghost Score, and Budget. Identify the Company Name.
                    {REPORT_PROTOCOL_HINT}
                    TITLE: JD FORENSIC SCOUT
                    JD: {jd}
                    """
                    res = client.models.generate_content(model=selected_model, contents=scout_prompt)
                    st.markdown("---")
                    st.markdown(res.text)
                    comp_res = client.models.generate_content(model="gemini-3-flash-preview", contents=f"Extract only the company name from: {res.text}. Return only the name.")
                    st.session_state['detected_company'] = comp_res.text.strip()
                except Exception as e:
                    st.error(f"Analysis Error: {e}")

# --- Tab 3: Strategic Intel ---
with tabs[2]:
    st.header("Strategic Intelligence")
    target = st.text_input("Target Company:", value=st.session_state['detected_company'], key="intel_t")
    if st.button("Research Pain Points"):
        if target:
            with st.spinner(f"Researching {target}..."):
                try:
                    prompt = f"""
                    Identify 3 'Bleeding Neck' pain points and 5 strategic control questions for {target}. 
                    Ground insights in this Vault: {st.session_state['career_vault']}.
                    {REPORT_PROTOCOL_HINT}
                    TITLE: STRATEGIC INTEL REPORT
                    """
                    res = client.models.generate_content(model=selected_model, contents=prompt)
                    st.session_state['strategic_intel'] = res.text
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"Intel Error: {e}")

# --- Tab 4: Outreach Architect ---
with tabs[3]:
    st.header("Outreach Architect")
    out_comp = st.text_input("Target Company:", value=st.session_state['detected_company'], key="outreach_comp")
    
    if st.button("Identify Potential Managers"):
        if out_comp:
            with st.spinner(f"Identifying decision makers at {out_comp}..."):
                res = client.models.generate_content(model=selected_model, contents=f"Identify 2 hiring managers at {out_comp} by NAME | TITLE. DO NOT include citations.")
                st.session_state['potential_managers'] = [m.strip() for m in res.text.split('\n') if "|" in m]
    
    sel = st.selectbox("Select Target Manager:", options=st.session_state['potential_managers'] if st.session_state['potential_managers'] else ["(Perform research first)"])
    
    if st.button("Draft 1st-Person Note"):
        if "|" in sel:
            n, t = sel.split("|")
            prompt = f"Write a 1st-person LinkedIn note (max 300 chars) to {n} ({t}) at {out_comp}. Grounded ONLY in Vault: {st.session_state['career_vault']}. DO NOT include citations."
            res = client.models.generate_content(model=selected_model, contents=prompt)
            st.code(res.text)

# --- Tab 5: Application Builder ---
with tabs[4]:
    st.header("📝 Application Builder")
    if st.session_state['career_vault'] and st.session_state['last_jd_analyzed']:
        st.info(f"Targeting role at: **{st.session_state['detected_company']}**")
        region = st.radio("Geopolitical Standard:", ["US Resume", "European CV"])
        
        if st.button("Generate Grounded Application"):
            with st.spinner("Synthesizing forensic documents..."):
                try:
                    builder_prompt = f"""
                    Generate a FULL Resume (Markdown) and a PLAIN TEXT Cover Letter.
                    GEOGRAPHY: {region}
                    VAULT: {st.session_state['career_vault']}
                    JD: {st.session_state['last_jd_analyzed']}
                    INTEL: {st.session_state['strategic_intel']}
                    RULES: 
                    1. US: Marketing brochure, reverse-chronological, no photo. 
                    2. EU: Comprehensive record, photo placeholders.
                    3. ANTI-HALLUCINATION: Use ONLY facts from Vault. Use [Placeholders] for missing data.
                    4. Cover Letter: PLAIN TEXT ONLY. NO CITATIONS.
                    Split documents with '|||'.
                    """
                    res = client.models.generate_content(model=selected_model, contents=builder_prompt)
                    parts = res.text.split("|||")
                    st.session_state['final_resume'] = parts[0].strip() if len(parts) > 0 else res.text
                    st.session_state['final_cl'] = parts[1].strip() if len(parts) > 1 else ""
                except Exception as e:
                    st.error(f"Builder Error: {e}")

        if st.session_state['final_resume']:
            st.session_state['final_resume'] = st.text_area("Edit Resume (Markdown)", st.session_state['final_resume'], height=300)
            st.session_state['final_cl'] = st.text_area("Edit Cover Letter (Plain Text)", st.session_state['final_cl'], height=200)
            
            if st.button("Prepare PDF for Download"):
                try:
                    pdf_bytes = export_as_pdf(st.session_state['final_resume'], st.session_state['final_cl'])
                    st.download_button("📥 Download PDF", pdf_bytes, file_name="Jobberly_Application.pdf", mime="application/pdf")
                except Exception as e:
                    st.error(f"PDF Prep Error: {e}")
    else:
        st.warning("⚠️ Seed Vault and analyze a JD first.")

# --- Tab 6: Tracking ---
with tabs[5]:
    st.header("📊 Market Ledger")
    st.table(pd.DataFrame({
        "Company": [st.session_state['detected_company'] if st.session_state['detected_company'] else "Pending"], 
        "Status": ["Ready" if st.session_state['final_resume'] else "Analyzing"], 
        "Escrow": ["Active"]
    }))
