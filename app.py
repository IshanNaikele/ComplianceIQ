import streamlit as st
from rag_chain import load_chain, ask

st.set_page_config(page_title="ComplianceIQ", page_icon="🔍")
st.title("🔍 ComplianceIQ")
st.caption("RAG-Powered Compliance Document Assistant — SOC 2 Trust Services Criteria")

@st.cache_resource
def get_chain():
    return load_chain()

chain = get_chain()

question = st.text_input("Ask a question about SOC 2 compliance:")

if question:
    with st.spinner("Thinking..."):
        answer, citations = ask(chain, question)

    st.markdown("### Answer")
    st.write(answer)

    st.markdown("### Sources")
    for c in citations:
        st.write(c)