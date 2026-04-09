from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama


def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Remove empty pages
    documents = [doc for doc in documents if doc.page_content.strip()]

    if not documents:
        raise ValueError("PDF has no readable text")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    docs = splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(model="llama3")
    db = FAISS.from_documents(docs, embeddings)

    return db


def ask_question(db, query):
    retriever = db.as_retriever(search_kwargs={"k": 3})

    # ✅ Use invoke (latest method)
    docs = retriever.invoke(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    llm = ChatOllama(model="llama3")

    prompt = f"""
You are an intelligent assistant.

Answer ONLY using the context below.
If the answer contains items (like cities, names), return them clearly as a list.
Explain in simple language.

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content, docs