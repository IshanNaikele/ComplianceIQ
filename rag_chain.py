import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

FAISS_PATH = "faiss_index"

PROMPT_TEMPLATE = """Use the context below to answer the question clearly and concisely.
If the answer is not in the context, say "I don't have enough information to answer this."

Context:
{context}

Question: {question}
Answer:"""

def load_chain():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="openai/gpt-oss-120b")
    retriever = db.as_retriever(search_kwargs={"k": 4})
    prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])
    return llm, retriever, prompt

def ask(chain, question):
    llm, retriever, prompt = chain
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    final_prompt = prompt.format(context=context, question=question)
    response = llm.invoke(final_prompt)
    answer = response.content

    citations = []
    seen = set()
    for doc in docs:
        page = doc.metadata.get("page", "?")
        source = doc.metadata.get("source", "document")
        key = (source, page)
        if key not in seen:
            seen.add(key)
            citations.append(f"📄 {source} — Page {int(page) + 1}")

    return answer, citations