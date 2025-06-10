import streamlit as st
from fpdf import FPDF
import google.generativeai as genai

# ======== CONFIGURATION ========
# Set your Gemini API key directly in code (INBUILT)
genai.configure(api_key="AIzaSyAgEitj_uAy5UpNmxNl5RX8Sdh6BAQw0C4 ")

model = genai.GenerativeModel("gemini-2.0-flash")

# ======== STREAMLIT UI ========
st.set_page_config(page_title="AI Email Generator", layout="centered")

st.title("📧 AI Email Generator")
st.write("Generate professional emails in your desired **tone** and **format** using AI.")

# Initialize session state
if "generated_email" not in st.session_state:
    st.session_state.generated_email = ""

# Sidebar Controls
st.sidebar.header("Email Preferences")

tone = st.sidebar.radio("Select Tone", ["Formal", "Friendly", "Persuasive", "Apologetic"])
format_type = st.sidebar.selectbox("Select Format", ["Business", "Personal", "Follow-Up", "Thank You", "Complaint"])

# Main Input
user_input = st.text_area("✍️ Enter your message or prompt", height=200)

# ======== Email Generation Function ========
def generate_email(text, tone, format_type):
    prompt = f"""Generate an email in a {tone} tone and {format_type} format using the following prompt:

{text}

Make sure the email has a subject, greeting, body, and closing."""
    response = model.generate_content(prompt)
    return response.text

# ======== Buttons ========
col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Email"):
        if user_input.strip() == "":
            st.warning("Please enter some text before generating.")
        else:
            email = generate_email(user_input, tone, format_type)
            st.session_state.generated_email = email

with col2:
    if st.button("Regenerate with New Style"):
        if user_input.strip() == "":
            st.warning("Please enter some text to regenerate.")
        else:
            email = generate_email(user_input, tone, format_type)
            st.session_state.generated_email = email

# ======== Display Generated Email ========
if st.session_state.generated_email:
    st.subheader("📩 Generated Email")
    st.markdown(st.session_state.generated_email)

    # ======== Download PDF ========
    def save_as_pdf(text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in text.split('\n'):
            pdf.multi_cell(0, 10, line)
        pdf_path = "/tmp/generated_email.pdf"
        pdf.output(pdf_path)
        return pdf_path

    pdf_file = save_as_pdf(st.session_state.generated_email)

    with open(pdf_file, "rb") as f:
        st.download_button("📥 Download as PDF", f, file_name="generated_email.pdf")

# ======== Footer ========
st.markdown("---")
st.caption("Built with ❤️ using Streamlit and Gemini Pro API.")
