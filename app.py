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

# 4. Sidebar: Identity, Metrics, and Model Selection
with st.sidebar:
    st.title("🛡️ Jobberly")
    st.markdown("**The Candidate-Centric Employment Protocol**")
    
    st.divider()
    
    st.subheader("🤖 AI Settings")
    selected_model = st.selectbox(
        "Select Model Tier:",
        ["gemini-2.0-flash", "gemini-2.0-pro-exp-02-05"], # Updated to current 2025 naming
        index=0,
        help="Choose the model used for discovery, analysis, and outreach."
    )
    
    st.divider()
    
    if st.session_state['career_vault']:
        st.status("Career Vault: Verified & Populated", state="complete")
    else:
        st.status("Career Vault: Awaiting Import", state="error")
    
    st.metric("Global Hiring Reputation", "3.8/5", "-0.2")
    st.info("Jobberly is an 'Agent' that permissions data rather than owning it.")
    st.caption("Jobberly v1.5.0 (Standardized Scout)")

# 5. Main Application Interface
st.title("🛡️ Jobseeker Advocate Suite")

tab_onboard, tab_scout, tab_intel, tab_outreach, tab_track = st.tabs([
    "🚀 Discovery Engine", 
    "🕵️ Command Center", 
    "🧠 Strategic Intel", 
    "📧 Outreach Architect",
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
                You are a Career Data Architect. Parse this FULL LinkedIn history 
                into a structured summary. Identify:
                1. Roles and responsibilities.
                2. Quantifiable achievements and metrics.
                3. Core skills and endorsements.
                4. Map these to potential corporate 'pain points' (e.g. burn rate, growth).
                
                TEXT: {full_text} 
                """
                response = client.models.generate_content(model=selected_model, contents=prompt)
                st.session_state['career_vault'] = response.text
                st.success("Vault Seeded with Full Profile Data!")
            except Exception as e:
                st.error(f"Error seeding vault: {e}")

    if st.session_state['career_vault']:
        st.divider()
        st.subheader("2. AI Interactive Interview")
        st.info("Vault Analysis (Problem-Solver Profile):")
        st.write(st.session_state['career_vault'])
        
        chat_input = st.chat_input("Tell the Advocate about a major win at work...")
        if chat_input:
            with st.chat_message("assistant"):
                try:
                    interview_prompt = (
                        f"Context: {st.session_state['career_vault']}. "
                        f"The candidate claims: '{chat_input}'. "
                        "Ask a probing, evidence-based question to uncover deep achievements "
                        "or impact on metrics (burn rate, revenue) not explicitly in the PDF."
                    )
                    res = client.models.generate_content(model=selected_model, contents=interview_prompt)
                    st.write(res.text)
                    st.caption(f"Interviewing with {selected_model}")
                except Exception as e:
                    st.error(f"AI Error: {e}")

# --- Tab 2: Command Center (Standardized Scout) ---
with tab_scout:
    st.header("The Deception Decoder")
    st.write("Analyze listings for 'Ghost Jobs' and 'Internal-Hire Theater.'")
    
    jd_text = st.text_area("Paste a Job Description (JD):", height=200)
    if st.button("Analyze Listing"):
        if jd_text:
            with st.spinner(f"Generating High-Fidelity Scout Report with {selected_model}..."):
                try:
                    # PRESCRIPTIVE PROMPT for consistent formatting
                    scout_prompt = f"""
                    Analyze this Job Description (JD) using the Jobberly Protocol. 
                    Your output MUST follow this exact structure:

                    ### 1. Ghost Score: [X]/100 ([Interpretation: e.g., Highly Likely to be Real])
                    A "Ghost Job" is a posting with no intent to hire. Provide:
                    * Bullet points explaining the score (e.g., specific language, company momentum, posting age).

                    ### 2. Internal-Hire Signals: [X]/100 ([Risk Level])
                    Identify if this is "Compliance Theater" for a pre-selected internal candidate. Provide:
                    * Bullet points identifying "hand-crafted" requirements or "bridge role" characteristics.

                    ### 3. Budget Prediction
                    Predict the hiring budget based on company stage, funding, and title deflation patterns. Provide:
                    * **Estimated Base Salary**: [Range]
                    * **Total Compensation Insights**: [Equity, perks, or comparison to market].

                    ### Strategic "Cheat Sheet" for Applying:
                    1. **The Core Bridge**: How to frame your experience for this specific role.
                    2. **Highlight the Friction**: Specific phrase or achievement to include.
                    3. **The X-Factor**: What will make you stand out from the "Purple Squirrel" hunt.

                    JD TEXT: {jd_text}
                    """
                    res = client.models.generate_content(model=selected_model, contents=scout_prompt)
                    st.markdown("---")
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"Analysis Error: {e}")
        else:
            st.warning("Please paste a job description first.")

# --- Tab 3: Strategic Intel ---
with tab_intel:
    st.header("Company Archeology")
    st.write("Research 'bleeding neck' pain points before you apply.")
    comp_name = st.text_input("Target Company Name:")
    if st.button("Generate Strategic Intel"):
        with st.spinner(f"Researching with {selected_model}..."):
            try:
                intel_prompt = f"Research {comp_name}. Identify: 1. Stage Pain Points, 2. A 3-Minute Interview Script."
                res = client.models.generate_content(model=selected_model, contents=intel_prompt)
                st.write(res.text)
            except Exception as e:
                st.error(f"Research Error: {e}")

# --- Tab 4: Outreach Architect ---
with tab_outreach:
    st.header("LinkedIn Connection Architect")
    st.write("Bypass the ATS with direct, tactical connection sequences.")
    role = st.text_input("Decision Maker Title:")
    if st.button("Draft Tactical Note"):
        if role:
            try:
                outreach_prompt = f"Write a 300-char LinkedIn note to a {role} at {comp_name}. Focus on solving a problem."
                res = client.models.generate_content(model=selected_model, contents=outreach_prompt)
                st.code(res.text, language="markdown")
            except Exception as e:
                st.error(f"Drafting Error: {e}")

# --- Tab 5: Market Tracking ---
with tab_track:
    st.header("Accountability Ledger")
    st.write("Track status and enforce the 'Feedback Escrow'.")
    tracking_data = pd.DataFrame({
        "Company": ["GlobalCorp", "TechStart"],
        "Status": ["Interview Scheduled", "Ghosted (Claim Pending)"],
        "Escrow Status": ["Locked", "Transferred to Seeker ($50)"]
    })
    st.table(tracking_data)
    
    st.divider()
    st.button("Activate 'Be Discovered' Mode (Reverse Auction)")
    st.caption("Verified anonymous profiles visible to employers for bidding.")
