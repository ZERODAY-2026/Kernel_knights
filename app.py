import streamlit as st
import fitz  # PyMuPDF

st.set_page_config(page_title="Legal Triage Agent", layout="wide")

st.title("⚖️ Private Legal Document Triage")
st.markdown("**100% On-Device Processing.** Your document never leaves this machine.")

# Step 1: Secure Local File Upload
uploaded_file = st.file_uploader("Upload a Legal Document (PDF)", type=["pdf"])

if uploaded_file is not None:
    # Step 2: On-Device Text Extraction
    with st.spinner("Extracting text locally..."):
        # Read the file from memory, no saving to disk
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
    
    # Step 4: Placeholder for Model Integration
    st.subheader("Legal Triage Analysis")
    st.info("The Gemma 4 model integration will go here.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Plain-Language Summary")
        st.write("Model output will appear here.")
    with col2:
        st.subheader("Quoted Clauses")
        st.write("Exact text snippets from the source.")
