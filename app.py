import streamlit as st
import openai
import PyPDF2
import io


openai.api_key = "API KEY"  

def summarize_text(text, model="gpt-4o-mini"):
    try:
        completion = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text, especially legal and technical documents, into clear and concise bullet points."},
                {"role": "user", "content": f"Please summarize the following text into bullet points, focusing on key information and making it easy to understand, especially for insurance policy terms and conditions:\n\n{text}"},
            ],
            temperature=0.3, 
            max_tokens=800,
        )
        summary = completion.choices[0].message.content
        return summary
    except Exception as e:
        return f"Error during summarization: {e}"


def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"


st.title("Insurance Policy Summarizer")

uploaded_file = st.file_uploader("Upload an insurance policy PDF", type="pdf")

if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)

    if isinstance(text, str) and "Error" not in text:
        if len(text) > 5000: 
            st.warning("The document is quite large.  Summarization might take a while, or be truncated. Consider breaking it down into smaller sections if necessary.")
            

        with st.spinner("Summarizing..."):
            summary = summarize_text(text)
            if isinstance(summary, str) and "Error" not in summary:
                st.subheader("Summary:")
                st.write(summary)
            else:
                st.error(summary) 
    else:
        st.error(text) 
