import streamlit as st
import openai
import PyPDF2
import os

openai.api_key = "API KEY"

def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def app():
    st.title("Help Me File a Claim")

    insurance_providers = ["UnitedHealthcare", "Anthem", "Aetna", "Cigna", "Kaiser Permanente", "Other"]
    selected_provider = st.selectbox("Select Your Insurance Provider", insurance_providers)

    claim_details = st.text_area(
        "Please provide as much information as possible about your insurance claim, any relevant documents (e.g., medical reports, bills, receipts). "
        "If you're asking about a specific issue, describe it clearly so I can guide you through the process effectively. "
        "For example, you can mention if you need help filing a claim, understanding coverage, or resolving a dispute.",
        height=200
    )

    policy_file = st.file_uploader("Upload your insurance policy (PDF)", type="pdf", key="policy_uploader")
    policy_text = None  

    if policy_file is not None:
        policy_text = extract_text_from_pdf(policy_file)
        if isinstance(policy_text, str) and "Error" not in policy_text:
            st.success("Insurance policy uploaded successfully.")
        else:
            st.error(f"Error processing policy: {policy_text}")
            policy_text = None 

    if st.button("Submit Claim Information"):
        if not claim_details:
            st.warning("Please provide details about your claim.")
            return

        try:
            with st.spinner("Processing your request..."):
                prompt = f"""
                    Insurance Provider: {selected_provider}
                    Claim Details: {claim_details}
                    """

                if policy_text:
                    prompt += f"""
                    Insurance Policy Text:
                    {policy_text}
                    """

                prompt += """
                    Analyze the provided information and determine:

                    1. Does the user's insurance policy likely cover this claim? (Yes/No/Maybe - with explanation)
                    2. If covered, what is the estimated coverage amount or percentage? (If not covered, explain why)

                    Provide a clear and concise response tailored for the user.  If possible, include specific policy details that support your answer. If the insurance provider is "Other", say that "I cannot determine coverage for other insurance providers."
                    """

                completion = openai.chat.completions.create(
                    model="gpt-3.5-turbo", 
                    messages=[
                        {"role": "system", "content": "You are an AI assistant helping users understand their insurance coverage."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.3,
                    max_tokens=700 
                )
                
                
                response = completion['choices'][0]['message']['content']
                st.write(response)

        except openai.OpenAIError as e:
            st.error(f"OpenAI API Error: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    app()
