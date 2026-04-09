import streamlit as st
from rag import process_pdf, ask_question

st.set_page_config(page_title="Fine Print Decoder")

st.title("📄 Fine Print Decoder")
st.write("Upload a policy PDF and ask questions in simple language!")

# Session state setup
if "db" not in st.session_state:
    st.session_state.db = None
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "docs" not in st.session_state:
    st.session_state.docs = []

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("PDF uploaded successfully!")

    if st.session_state.db is None:
        with st.spinner("Processing PDF..."):
            st.session_state.db = process_pdf("temp.pdf")

# Ask question
if st.session_state.db is not None:
    query = st.text_input("💬 Ask your question:")

    if st.button("Ask"):
        if query.strip() == "":
            st.warning("Please enter a question")
        else:
            with st.spinner("Thinking..."):
                answer, docs = ask_question(st.session_state.db, query)

                # Save results
                st.session_state.answer = answer
                st.session_state.docs = docs

# Show answer (IMPORTANT: outside button)
if st.session_state.answer:
    st.write("### ✅ Answer:")
    st.write(st.session_state.answer)

    st.write("### 📍 Sources:")
    for doc in st.session_state.docs:
        st.write(f"Page: {doc.metadata.get('page', 'N/A')}")
        st.write(doc.page_content[:200])
        st.write("---")