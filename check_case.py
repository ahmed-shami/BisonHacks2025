import streamlit as st
import PyPDF2
import openai
import os
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = "REMOVED FOR SAFETY CONCERNS"
if not OPENAI_API_KEY:
    st.error("Error: OpenAI API key not found. Please set OPENAI_API_KEY in environment variables.")
    st.stop()
openai.api_key = OPENAI_API_KEY

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text: {e}"

def analyze_denial_reason(denial_text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that analyzes insurance denial letters."},
        {"role": "user", "content": f"Analyze the following denial text and summarize the main reason for denial in a concise and user-friendly way:\n\n```\n{denial_text}\n```"}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error analyzing denial reason: {e}"

def generate_reclaim_report(denial_text, supporting_text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that generates reclaim appeal letters."},
        {"role": "user", "content": f"""Generate a reclaim appeal letter based on the following denial text and supporting information.  The letter should be persuasive, professional, and address the specific reasons for denial.  It should also clearly state the desired outcome (e.g., approval of the claim).

        Denial Text:
        ```
        {denial_text}
        ```

        Supporting Information:
        ```
        {supporting_text}
        ```
        """}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error generating reclaim report: {e}"

def analyze_legal_case(denial_text, supporting_text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that analyzes legal cases related to insurance denials."},
        {"role": "user", "content": f"""Analyze the following denial text and supporting information to determine if there is a potential legal case against the insurance company.  Consider factors like breach of contract, bad faith denial, and applicable laws. Provide a brief explanation of your reasoning.

        Denial Text:
        ```
        {denial_text}
        ```

        Supporting Information:
        ```
        {supporting_text}
        ```
        """}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error analyzing legal case: {e}"

def generate_lawsuit_draft(denial_text, supporting_text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that drafts legal documents (for educational purposes only)."},
        {"role": "user", "content": f"""Draft a basic outline or starting point for a lawsuit against the insurance company based on the following denial text and supporting information.  This is NOT a complete legal document, but rather a starting point for discussion with an attorney. Include potential causes of action and key arguments.

        Denial Text:
        ```
        {denial_text}
        ```

        Supporting Information:
        ```
        {supporting_text}
        ```
        """}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error generating lawsuit draft: {e}"

def app():
    st.title("Denial Case Assistant")
    st.markdown("---")

    denial_file = st.file_uploader("Upload Insurance Denial PDF", type=["pdf"], key="denial")
    supporting_docs = st.file_uploader("Upload Supporting Documents (Medical reports, receipts, images)", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True, key="supporting")

    denial_text = ""
    supporting_text = ""

    if denial_file:
        st.write("### Analyzing Denial Reason...")
        denial_text = extract_text_from_pdf(denial_file)
        if "Error" in denial_text or denial_text.startswith("Error"):
            st.error(denial_text)
        else:
            denial_reason = analyze_denial_reason(denial_text)
            st.write(denial_reason)

    if supporting_docs:
        st.write("### Processing Supporting Documents...")
        for doc in supporting_docs:
            if doc.type == "application/pdf":
                extracted_text = extract_text_from_pdf(doc)
                if "Error" in extracted_text or extracted_text.startswith("Error"):
                    st.error(extracted_text)
                else:
                    supporting_text += extracted_text + "\n"
            else:
                supporting_text += f"[Uploaded image: {doc.name}]\n"

        if denial_text:
            reclaim_report = generate_reclaim_report(denial_text, supporting_text)
            st.write("### Suggested Reclaim Appeal")
            st.text_area("Generated Appeal Letter", reclaim_report, height=300)
            st.download_button("Download Appeal Letter", data=reclaim_report.encode('utf-8'), file_name="appeal_letter.txt", mime="text/plain")

            st.markdown("---")

            st.write("### Potential Legal Case Analysis")
            legal_analysis = analyze_legal_case(denial_text, supporting_text)
            st.write(legal_analysis)

            if st.button("Generate Lawsuit Draft (Consult an Attorney!)"):
                lawsuit_draft = generate_lawsuit_draft(denial_text, supporting_text)
                st.text_area("Lawsuit Draft (Consult an Attorney!)", lawsuit_draft, height=300)
                st.warning("This is NOT a substitute for legal advice. You MUST consult with a qualified attorney before taking any legal action.")
        else:
            st.write("Please upload the denial letter first.")

if __name__ == "__main__":
    app()
