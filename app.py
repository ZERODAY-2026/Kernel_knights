import streamlit as st
import fitz  # PyMuPDF

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from model_logic import analyze_legal_text

st.set_page_config(page_title="Legal Triage Agent", layout="wide")

st.title("⚖️ Private Legal Document Triage")
st.markdown("**100% On-Device Processing.** Your document never leaves this machine.")

# Step 1: Secure Local File Upload
uploaded_file = st.file_uploader("Upload a Legal Document (PDF)", type=["pdf"])

if uploaded_file is not None:
    # Step 2: On-Device Text Extraction
    with st.spinner("Extracting text locally..."):
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        document_text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            document_text += page.get_text("text") + "\n\n"

    st.success("Document parsed successfully!")

    # Step 3: UI Design for Trust (Rule L6)
    with st.expander("View Raw Extracted Text (Source)"):
        st.text_area("Extracted Text", document_text, height=300)

    st.divider()

    # Step 4: Model Integration with local Ollama
    st.subheader("Legal Triage Analysis")

    try:
        with st.spinner("Analyzing legal text locally with Ollama..."):
            analysis = analyze_legal_text(document_text)

        if analysis.get("requires_lawyer_escalation"):
            st.warning("This clause may require legal escalation due to complexity or risk.")
        if analysis.get("is_ambiguous"):
            st.warning("Some wording appears ambiguous and may need legal review.")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Plain-Language Summary")
            st.markdown(f"**Clause Topic:** {analysis.get('clause_topic', 'Not specified')}")
            st.write(analysis.get("plain_language_summary", "No summary generated."))
            st.markdown("**Obligations & Penalties:**")
            st.write(analysis.get("obligations_and_penalties", "No obligations extracted."))

            if analysis.get("warnings"):
                st.caption(f"Warnings: {analysis.get('warnings')}")

        with col2:
            st.subheader("Quoted Clauses")
            quotes = analysis.get("verifiable_quotes", [])
            if quotes:
                for quote in quotes:
                    st.markdown(f"- {quote}")
            else:
                st.write("No exact quotes were returned by the model.")
    except Exception as e:
        st.error("Could not connect to the local Ollama model.")
        st.info("Please ensure Ollama is installed and running, and that the model `gemma4:e4b` is available.")
        st.code(f"Error: {e}")

