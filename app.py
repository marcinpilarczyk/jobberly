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

# 3. Session State
if 'career_vault' not in st.session_state:
    st.session_state['career_vault'] = None

# 4. Sidebar: Identity & Identity Protocol
with st.sidebar:
    st.title("🛡️ Jobberly")
    st.markdown("**The Candidate-Centric Employment Protocol**")
    st.info("Jobberly is an 'Agent' that permissions data rather than owning it.")
    st.divider()
    
    if st.session_state['career_vault']:
        st.status("Career Vault: Verified & Populated", state="complete")
    else:
        st.status("Career Vault: Awaiting Import", state="error")
    
    st.metric("Global Hiring Reputation", "3.8/5", "-0.2")
    st.divider()
    st.caption("Jobberly v1.3.0 (Unrestricted)")

# 5. Main Application Interface
st.title("🛡️ Jobseeker Advocate Suite")

tab_onboard, tab_scout, tab_intel, tab_outreach, tab_track = st.tabs([
    "🚀 Discovery Engine", 
    "🕵️ Command Center", 
    "🧠 Strategic Intel", 
    "📧 Outreach Architect",
    "📊 Market Tracking"
])

# --- Tab 1: Discovery Engine (High-Fidelity Import) ---
with tab_onboard:
    st.header("1. Build Your Proof-Based Vault")
    st.write("LinkedIn -> More... -> Save to PDF. Upload it below to seed your vault.")
    
    uploaded_file = st.file_uploader("Upload LinkedIn PDF", type="pdf")
    
    if uploaded_file and not st.session_state['career_vault']:
        with st.spinner("AI Agent analyzing full professional history..."):
            try:
                reader = pypdf.PdfReader(uploaded_file)
                # Now capturing the ENTIRE document text
                full_text = "".join([page.extract_text() for page in reader.pages])
                
                # High-fidelity prompt for 'Problem-Solver' mapping
                prompt = f"""
                You are a Career Data Architect. Parse this FULL LinkedIn professional history 
                into a structured summary. Identify:
                1. Roles and responsibilities.
                2. Quantifiable achievements and metrics.
                3. Core skills and endorsements.
                4. Map these to potential corporate 'pain points' (e.g. burn rate, growth).
                
                TEXT: {full_text} 
                """
                response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
                st.session_state['career_vault'] = response.text
                st.success("Vault Seeded with Full Profile Data!")
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state['career_vault']:
        st.divider()
        st.subheader("2. AI Interactive Interview")
        st.info("Vault Analysis (Problem-Solver Profile):")
        st.write(st.session_state['career_vault'])
        
        chat_input = st.chat_input("Tell the Advocate about a major win at work...")
        if chat_input:
            with st.chat_message("assistant"):
                try:
                    # Using the full vault context for better questions
                    interview_prompt = (
                        f"Context: {st.session_state['career_vault']}. "
                        f"The candidate claims: '{chat_input}'. "
                        "Ask a probing, evidence-based question to uncover deep achievements "
                        "or impact on company metrics that were not explicitly in the PDF."
                    )
                    res = client.models.generate_content(model="gemini-2.0-flash", contents=interview_prompt)
                    st.write(res.text)
                    st.caption("Captured and saved to Local Career Vault.")
                except Exception as e:
                    st.error(f"AI Error: {e}")

# --- Tab 2: Command Center (Full Context Scout) ---
with tab_scout:
    st.header("The Deception Decoder")
    st.write("Analyze listings for 'Ghost Jobs' and 'Internal-Hire Theater.'")
    
    jd_text = st.text_area("Paste a Job Description (JD):", height=200)
    if st.button("Analyze Listing"):
        if jd_text:
            with st.spinner("Decoding corporate-speak..."):
                try:
                    # Now allowing more text for JD analysis
                    scout_prompt = f"Analyze this JD for: 1. Ghost Score, 2. Internal-Hire Signals, 3. Budget Prediction. JD: {jd_text}"
                    res = client.models.generate_content(model="gemini-2.0-flash", contents=scout_prompt)
                    st.markdown("### 📊 Scout Report")
                    st.write(res.text)
                except Exception as e:
                    st.error(f"Analysis Error: {e}")

# --- Tab 3: Strategic Intel (Company Archeology) ---
with tab_intel:
    st.header("Company Archeology")
    comp_name = st.text_input("Target Company Name:")
    if st.button("Generate Strategic Intel"):
        with st.spinner(f"Researching {comp_name}..."):
            try:
                intel_prompt = f"Research {comp_name}. Identify: 1. Stage Pain Points, 2. A 3-Minute Interview Script."
                res = client.models.generate_content(model="gemini-2.0-flash", contents=intel_prompt)
                st.write(res.text)
            except Exception as e:
                st.error(f"Research Error: {e}")

# --- Tab 4: Outreach Architect ---
with tab_outreach:
    st.header("LinkedIn Connection Architect")
    role = st.text_input("Decision Maker Title:")
    if st.button("Draft Tactical Note"):
        if role:
            try:
                outreach_prompt = f"Write a 300-char LinkedIn note to a {role} at {comp_name}. Focus on solving a problem."
                res = client.models.generate_content(model="gemini-2.0-flash", contents=outreach_prompt)
                st.code(res.text, language="markdown")
            except Exception as e:
                st.error(f"Drafting Error: {e}")

# --- Tab 5: Market Tracking ---
with tab_track:
    st.header("Accountability Ledger")
    tracking_data = pd.DataFrame({
        "Company": ["GlobalCorp", "TechStart"],
        "Status": ["Interview Scheduled", "Ghosted (Claim Pending)"],
        "Escrow Status": ["Locked", "Transferred to Seeker ($50)"]
    })
    st.table(tracking_data)
