import streamlit as st
import os
from LLM import MistralLLM, query_document


mistral_llm = MistralLLM()


st.set_page_config(page_title="Audit Findings Chat", page_icon="💬", layout="wide")

st.title("💬 ARES RAG AGENT")
st.markdown(
    """
    Welcome to the **ARES RAG AGENT**! This application allows users to detect vulnerabilities in smart contracts.

### Features:
- **Smart Retrieval**: Finds relevant excerpts and vulnerabilities.
- **Custom Checklists**: Choose a checklist file to guide the analysis.

🚀 **Follow us on Twitter [@aresAI_agent](https://x.com/ARES_Sec) for bigger updates coming your way!**
    """
)



checklist_dir = "./checklists"
if not os.path.exists(checklist_dir):
    os.makedirs(checklist_dir)


checklist_files = [f for f in os.listdir(checklist_dir) if f.endswith(".md")]


selected_checklist = st.selectbox("Select a checklist file:", ["None"] + checklist_files)


query = st.text_area("Enter your question or audit request:")


checklist_content = ""
if selected_checklist != "None":
    with open(os.path.join(checklist_dir, selected_checklist), "r", encoding="utf-8") as file:
        checklist_content = file.read()

# Submit button
if st.button("Send to AI"):
    if not query:
        st.warning("Please enter a question or audit request.")
    else:
        
        query_with_checklist = query
        if checklist_content:
            query_with_checklist += f"\n\n---\n\n### 🔍 Checklist:\n{checklist_content}"


        with st.spinner("Processing..."):
            try:
                response, total_tokens = query_document(query_with_checklist, mistral_llm)
                st.markdown("### AI Response:")
                st.markdown(response)
                st.markdown(f"_Total Tokens Used: {total_tokens}_")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}") # added emojis soo it looks cooler hahahah
