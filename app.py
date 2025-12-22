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
if 'potential_managers' not in st.session_state:
    st.session_state['potential_managers'] = []
if 'generated_resume' not in st.session_state:
    st.session_state['generated_resume'] = ""
if 'generated_cover_letter' not in st.session_state:
    st.session_state['generated_cover_letter'] = ""

# 4. Sidebar: Identity, Metrics, and Persistent Settings
with st.sidebar:
    st.title("🛡️ Jobberly")
    st.markdown("**The Candidate-Centric Employment Protocol**")
    st.divider()
    
    st.subheader("⚙️ Vault Settings")
    if not st.session_state['career_vault']:
        st.info("Your Career Vault is empty. Seed it with your LinkedIn PDF to begin.")
    
    uploaded_file = st.file_uploader("Upload LinkedIn PDF", type="pdf", key="vault_uploader")
    
    if uploaded_file:
        with st.spinner("Forensically seeding your Career Vault..."):
            try:
                reader = pypdf.PdfReader(uploaded_file)
                full_text = "".join([page.extract_text() for page in reader.pages])
                prompt = f"Parse this profile into a structured summary focusing on Seniority, Skills, and specific Wins. TEXT: {full_text}"
                response = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
                st.session_state['career_vault'] = response.text
                st.success("Vault Synchronized.")
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
    st.caption("Jobberly v3.5.0")

# 5. Main Application Interface
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
    st.header("🚀 The Discovery Engine")
    
    if not st.session_state['career_vault']:
        st.warning("⚠️ Access Denied: Please seed your Career Vault in the Sidebar Settings.")
    else:
        st.subheader("Interactive Achievement Refinement")
        st.write("Let's identify vague claims in your profile and turn them into quantifiable wins.")
        
        with st.expander("🔍 View Profile Analysis"):
            st.write(st.session_state['career_vault'])

        st.divider()
        
        for message in st.session_state['chat_history']:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if chat_prompt := st.chat_input("Explain a project or a major win..."):
            st.session_state['chat_history'].append({"role": "user", "content": chat_prompt})
            with st.chat_message("user"):
                st.markdown(chat_prompt)

            with st.chat_message("assistant"):
                refinement_prompt = f"""
                You are the Jobberly Achievement Architect. 
                VAULT CONTEXT: {st.session_state['career_vault']}
                USER INPUT: {chat_prompt}
                
                Ask one specific, conversational question to find the metric (e.g., revenue impact, time saved, or burn rate reduction). 
                Focus on making the achievement forensic and clear.
                """
                response = client.models.generate_content(model=selected_model, contents=refinement_prompt)
                st.markdown(response.text)
                st.session_state['chat_history'].append({"role": "assistant", "content": response.text})

# --- Tab 2: Command Center ---
with tabs[1]:
    st.header("🕵️ Command Center")
    st.write("Analyze listings for 'Ghost Jobs' and 'Compliance Theater'.")
    
    jd_text = st.text_area("Paste Job Description (JD):", height=200, key="scout_jd")
    if st.button("Generate Trust Report"):
        if jd_text:
            st.session_state['last_jd_analyzed'] = jd_text
            with st.spinner("Decoding intent signals..."):
                try:
                    scout_prompt = f"""
                    Analyze this JD for Trust Score, Red Flags, Internal-Hire DNA, and Budget. 
                    IDENTIFY THE COMPANY NAME CLEARLY.
                    JD: {jd_text}
                    """
                    res = client.models.generate_content(model=selected_model, contents=scout_prompt)
                    st.markdown("---")
                    st.markdown(res.text)
                    
                    # Forensic extraction of company name
                    extract_prompt = f"Extract only the company name from this report: {res.text}. Return only the name."
                    name_res = client.models.generate_content(model="gemini-3-flash-preview", contents=extract_prompt)
                    st.session_state['detected_company'] = name_res.text.strip()
                except Exception as e:
                    st.error(f"Analysis Error: {e}")
        else:
            st.warning("Please paste a job description.")

# --- Tab 3: Strategic Intel ---
with tabs[2]:
    st.header("🧠 Strategic Intel")
    st.write("Research 'bleeding neck' pain points and prepare strategic control questions.")
    
    # Auto-populated from Command Center
    comp_name = st.text_input("Target Company:", value=st.session_state['detected_company'], key="intel_comp")
    
    if st.button("Generate Intelligence Map"):
        if comp_name:
            with st.spinner(f"Researching {comp_name}..."):
                try:
                    intel_prompt = f"""
                    Research {comp_name}. 
                    Identify: 
                    1. Company Stage & Market Position.
                    2. 'Bleeding Neck' Pain Points (Top 3 friction areas).
                    3. Strategic Control Questions: 5 deep-dive questions the candidate can ask to demonstrate understanding and control the interview.
                    
                    Context from Vault: {st.session_state['career_vault']}
                    """
                    res = client.models.generate_content(model=selected_model, contents=intel_prompt)
                    st.session_state['strategic_intel'] = res.text
                    st.markdown(f"### 🧬 {comp_name} Strategy Map")
                    st.write(res.text)
                except Exception as e:
                    st.error(f"Intel Error: {e}")

# --- Tab 4: Outreach Architect ---
with tabs[3]:
    st.header("📧 Outreach Architect")
    st.write("Identify decision-makers and craft grounded personal notes.")
    
    # Auto-populated from previous tabs
    outreach_comp = st.text_input("Target Company:", value=st.session_state['detected_company'], key="outreach_comp")
    
    if st.button("Identify Potential Hiring Managers"):
        if outreach_comp:
            with st.spinner(f"Identifying managers at {outreach_comp}..."):
                res = client.models.generate_content(model=selected_model, contents=f"Identify 2 likely managers at {outreach_comp} by NAME | TITLE.")
                st.session_state['potential_managers'] = [m.strip() for m in res.text.split('\n') if "|" in m]
    
    selected_target = st.selectbox("Select Target:", options=st.session_state['potential_managers'] if st.session_state['potential_managers'] else ["(Perform research)"])
    
    if st.button("Generate Grounded Note"):
        if selected_target and "|" in selected_target:
            name, title = selected_target.split("|")
            out_prompt = f"""
            Write a 1st-person note (max 300 chars) to {name.strip()} ({title.strip()}) at {outreach_comp}.
            STRICT GROUNDING: Use ONLY wins/skills from this vault: {st.session_state['career_vault']}.
            DO NOT HALLUCINATE.
            """
            res = client.models.generate_content(model=selected_model, contents=out_prompt)
            st.markdown(f"### 📧 Personal Note for {name.strip()}")
            st.code(res.text, language="markdown")

# --- Tab 5: Application Builder ---
with tabs[4]:
    st.header("📝 Application Builder")
    if not st.session_state['career_vault'] or not st.session_state['last_jd_analyzed']:
        st.warning("⚠️ Complete Vault seeding and JD analysis first.")
    else:
        st.info(f"Generating documents for: **{st.session_state['detected_company']}**")
        
        if st.button("Generate Full Application Docs"):
            with st.spinner("Synthesizing tailored documents..."):
                builder_prompt = f"""
                Generate a FULL Resume (Markdown) and a PLAIN TEXT Cover Letter (No formatting, no bold, no bullets).
                
                ### DATA:
                VAULT: {st.session_state['career_vault']}
                JD: {st.session_state['last_jd_analyzed']}
                INTEL: {st.session_state['strategic_intel']}
                
                ### RULES:
                1. STRICT GROUNDING: Use ONLY existing vault experience.
                2. Use placeholders like [PHONE] for missing contact info.
                3. First-person POV.
                4. Split docs with '|||'.
                """
                res = client.models.generate_content(model=selected_model, contents=builder_prompt)
                parts = res.text.split('|||')
                st.session_state['generated_resume'] = parts[0].strip() if len(parts) > 0 else res.text
                st.session_state['generated_cover_letter'] = parts[1].strip() if len(parts) > 1 else ""

        if st.session_state['generated_resume']:
            st.subheader("📄 Tailored Resume")
            st.text_area("Edit & Copy", value=st.session_state['generated_resume'], height=400)
            
            st.subheader("📧 Strategic Cover Letter (Plain Text)")
            st.text_area("Copy Text", value=st.session_state['generated_cover_letter'], height=300)

# --- Tab 6: Market Tracking ---
with tabs[5]:
    st.header("📊 Market Tracking")
    st.table(pd.DataFrame({"Company": [st.session_state['detected_company']], "Status": ["Drafts Ready"], "Escrow": ["Active"]}))
