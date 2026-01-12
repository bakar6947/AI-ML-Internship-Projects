from google import genai
import streamlit as st



# Setup API Key

API_KEY = st.secrets["GEMINI_API"]
client = genai.Client(api_key=API_KEY)



# Setup Page
st.set_page_config(page_title="HealthAssist AI", page_icon="💊", layout="centered")



# Style Main Page (Hero Section)
st.title("🩺 HealthAssist AI")
st.markdown("##### *Quick Symptom Checker & Wellness Guide*")
st.write("Please describe your symptoms in the box below.")



# Style Input Box and Button
with st.container():
    user_input = st.text_input("", placeholder="e.g., I have a persistent headache and blurry vision...")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        submit_button = st.button("Search")



# Logic and Response
if submit_button:
    if user_input:
        
        # Setup Promt
        prompt = f"""
        ROLE: You are a professional Health Assistant.
    
        TOPIC GUARDRAIL: 
            - If the user's question is NOT about health, medicine, or symptoms, you must ONLY say: 
              "I'm just a HealthAssist and I only answer questions related to health and medical symptoms." \n Your Question: {user_input}
            - Do not explain why, do not apologize, and do not provide the answer to the off-topic question.

        MEDICAL GUIDELINES (Only if the topic is health):
            1. GUESS: Provide a simple, non-technical guess of the possible condition.
            2. LIFESTYLE: Suggest one basic wellness tip (e.g., hydration, rest, or warm compresses).
            3. NO MEDICINE: Never name specific medications, drugs, or dosages.
            4. MANDATORY CONCLUSION: ALWAYS conclude by telling the user to consult a doctor for a professional diagnosis.

        USER QUESTION: {user_input}
        """


        with st.spinner("🔄 Consultating medical database..."):
            try:
                st.markdown("---")
                st.subheader("📋 Assessment Summary")

                # Model
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=prompt
                )

                # Model Response
                st.success(response.text)
                st.caption("⚠️ Note: This is an automated guess. Do not self-medicate.")

            except Exception as e:
                st.error(f"Error connecting to AI service: {e}")
    else:
        st.toast("Please type your symptoms first!", icon="⚠️")



# Style Footer
col_a, col_b = st.columns(2)
with col_a:
    st.markdown("**Common Queries:**")
    st.caption("- Flu-like symptoms\n- Muscle Strains\n- Skin Rashes")
with col_b:
    st.markdown("**Emergency?**")
    st.markdown("Call **1122** or your local emergency number immediately.")

# Style Footer Label
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0E1117; /* Matches Streamlit dark theme */
        color: #FAFAFA;
        text-align: center;
        padding: 4px 4px 0px;
        font-size: 14px;
        letter-spacing: 1px;
    }
    </style>
    <div class="footer">
        <p>Developed by <span style='color: #fb923c; font-weight: bold;'>Abu Bakar</span> | © 2026 HealthAssist AI<br>v1.0.0 | Powered by Gemini 2.5</p>
    </div>
    """, unsafe_allow_html=True)