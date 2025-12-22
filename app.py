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

# --- HELPER: PDF Generation & Sanitization ---
def sanitize_for_pdf(text):
    """Removes or replaces characters that cause FPDF UnicodeEncodingErrors."""
    # Standard FPDF fonts only support latin-1. We replace common problematic chars.
    replacements = {
        '\u2013': '-', '\u2014': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2022': '*', '\u2026': '...'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Encode to latin-1 and back to ignore other complex symbols/emojis
    return text.encode('latin-1', 'ignore').decode('latin-1')

def export_as_pdf(resume_text, cl_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Sanitization to fix FPDFUnicodeEncodingException
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
    
    return pdf.output()

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
                # Protocol: Extract seniority, wins, and skills
                prompt = f"Parse this profile into a structured summary for a 'Problem-Solver' profile. TEXT: {raw_text}"
                res = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
                st.session_state['career_vault'] = res.text
                st.success("Vault Synchronized.")
            except Exception as e:
                st.error(f"Seeding Error: {e}")
    
    if st.session_state['career_vault']:
        if st.button("🗑️ Wipe Career Vault"):
            st.session_state['career_vault'] = None
            st.session_state['chat_history'] = []
            st.rerun()
            
    st.divider()
    selected_model = st.selectbox("AI Model:", ["gemini-3-flash-preview", "gemini-3-pro-preview"], index=0)
    st.divider()
    st.metric("Hiring Reputation", "3.8/5", "-0.2")
    st.caption("Jobberly v3.6.1")

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
        # RESTORED: Show current profile and wins
        st.subheader("Current Profile Content")
        with st.expander("🔍 View Your Problem-Solver Profile", expanded=True):
            st.markdown(st.session_state['career_vault'])
            
        st.divider()
        st.subheader("Refine and Quantify Your Wins")
        st.write("Let's make your achievements forensic. Tell me about a win you'd like to improve.")

        for msg in st.session_state['chat_history']:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
        
        if chat := st.chat_input("Tell the Advocate about a project..."):
            st.session_state['chat_history'].append({"role": "user", "content": chat})
            with st.chat_message("user"): st.markdown(chat)
            with st.chat_message("assistant"):
                prompt = f"Using the context of this profile: {st.session_state['career_vault']}, help the user quantify this new win: {chat}. Ask one metric-focused question."
                res = client.models.generate_content(model=selected_model, contents=prompt)
                st.markdown(res.text)
                st.session_state['chat_history'].append({"role": "assistant", "content": res.text})

# --- Tab 2: Command Center ---
with tabs[1]:
    st.header("Forensic JD Scout")
    st.write("Analyze listings for Ghost Scores and Internal-Hire DNA.")
    jd = st.text_area("Paste JD:", height=200, key="jd_in")
    if st.button("Generate Trust Report"):
        if jd:
            st.session_state['last_jd_analyzed'] = jd
            with st.spinner("Decoding Forensic DNA..."):
                try:
                    scout_prompt = f"Analyze for Trust, Internal-Hire DNA, and Budget. CLEARLY IDENTIFY COMPANY NAME. JD: {jd}"
                    res = client.models.generate_content(model=selected_model, contents=scout_prompt)
                    st.markdown(res.text)
                    # Extract company name for other tabs
                    extract_prompt = f"Extract only the company name from this report: {res.text}"
                    comp_res = client.models.generate_content(model="gemini-3-flash-preview", contents=extract_prompt)
                    st.session_state['detected_company'] = comp_res.text.strip()
                except Exception as e:
                    st.error(f"Analysis Error: {e}")

# --- Tab 3: Strategic Intel ---
with tabs[2]:
    st.header("Strategic Intelligence")
    target = st.text_input("Target Company:", value=st.session_state['detected_company'], key="intel_t")
    if st.button("Research Company Pain Points"):
        if target:
            with st.spinner(f"Researching {target}..."):
                try:
                    prompt = f"Identify 3 'Bleeding Neck' pain points and 5 strategic control questions for {target}. Vault: {st.session_state['career_vault']}"
                    res = client.models.generate_content(model=selected_model, contents=prompt)
                    st.session_state['strategic_intel'] = res.text
                    st.write(res.text)
                except Exception as e:
                    st.error(f"Intel Error: {e}")

# --- Tab 4: Outreach Architect ---
with tabs[3]:
    st.header("Outreach Architect")
    target_comp = st.text_input("Target Company:", value=st.session_state['detected_company'], key="out_comp")
    if st.button("Identify Potential Managers"):
        if target_comp:
            with st.spinner("Identifying decision makers..."):
                res = client.models.generate_content(model=selected_model, contents=f"Identify 2 likely managers at {target_comp} by NAME | TITLE.")
                st.session_state['potential_managers'] = [m.strip() for m in res.text.split('\n') if "|" in m]
    
    sel = st.selectbox("Target Manager:", st.session_state['potential_managers'] if st.session_state['potential_managers'] else ["(Perform research)"])
    if st.button("Draft Tactical Note"):
        if "|" in sel:
            n, t = sel.split("|")
            prompt = f"Write 1st-person LinkedIn note (max 300 chars) to {n} ({t}) at {target_comp}. Grounded in Vault: {st.session_state['career_vault']}"
            res = client.models.generate_content(model=selected_model, contents=prompt)
            st.code(res.text)

# --- Tab 5: Application Builder ---
with tabs[4]:
    st.header("📝 Application Builder")
    if st.session_state['career_vault'] and st.session_state['last_jd_analyzed']:
        st.info(f"Targeting role at: **{st.session_state['detected_company']}**")
        region = st.radio("Resume Geography Standards:", ["US Resume", "European CV"])
        
        if st.button("Generate Tailored Application"):
            with st.spinner("Bridging Vault to opportunity..."):
                try:
                    builder_prompt = f"""
                    Generate a FULL Resume and a PLAIN TEXT Cover Letter.
                    
                    GEOGRAPHY: {region}
                    VAULT: {st.session_state['career_vault']}
                    JD: {st.session_state['last_jd_analyzed']}
                    INTEL: {st.session_state['strategic_intel']}
                    
                    ### CORE RULES:
                    1. US: Marketing brochure model. 1-2 pages. NO photo/DOB. Action-oriented.
                    2. EU: Comprehensive record. 2 pages. Include placeholders for photo and personal data.
                    3. BOTH: Use Single-Column layout. NO tables or graphics. 
                    4. Use STAR/XYZ method for bullets. If metrics are missing, use [METRIC].
                    5. COVER LETTER: STRICT PLAIN TEXT. NO bold, italics, or bullets.
                    6. AVOID AI BUZZWORDS: Spearheaded, Leverage, Tapestry, Delve. Use punchy, varied sentence lengths.
                    
                    Split documents with '|||'.
                    """
                    res = client.models.generate_content(model=selected_model, contents=builder_prompt)
                    parts = res.text.split("|||")
                    st.session_state['final_resume'] = parts[0].strip() if len(parts) > 0 else res.text
                    st.session_state['final_cl'] = parts[1].strip() if len(parts) > 1 else ""
                except Exception as e:
                    st.error(f"Generation Error: {e}")

        if st.session_state['final_resume']:
            st.session_state['final_resume'] = st.text_area("Edit Resume (Markdown format)", st.session_state['final_resume'], height=300)
            st.session_state['final_cl'] = st.text_area("Edit Cover Letter (Plain Text)", st.session_state['final_cl'], height=200)
            
            if st.button("Prepare PDF for Download"):
                try:
                    pdf_bytes = export_as_pdf(st.session_state['final_resume'], st.session_state['final_cl'])
                    st.download_button("📥 Download PDF", pdf_bytes, file_name="Jobberly_Application.pdf", mime="application/pdf")
                except Exception as e:
                    st.error(f"PDF Prep Error: {e}")
    else:
        st.warning("⚠️ Access Denied: Please seed your Career Vault and analyze a JD first.")

# --- Tab 6: Tracking ---
with tabs[5]:
    st.header("📊 Market Accountability Ledger")
    tracking_data = pd.DataFrame({
        "Company": [st.session_state['detected_company'] if st.session_state['detected_company'] else "Pending"],
        "Status": ["Documents Generated" if st.session_state['final_resume'] else "Awaiting Analysis"],
        "Feedback Escrow": ["Active"]
    })
    st.table(tracking_data)
