import streamlit as st
from utils.firecrawl_scraper import firecrawl_scrape
from utils.llm_extractor import query_openrouter

st.set_page_config(page_title="Pulse-AI Doc Extractor", layout="wide")
st.title("📘 Pulse-AI Help Documentation Module Extractor")

url = st.text_input("🔗 Enter the documentation website URL:", "")
depth = st.slider("📚 How deeply should we crawl?", 1, 5, 3)

if st.button("🚀 Extract Documentation Modules") and url:
    with st.spinner("🔥 Crawling documentation site with Firecrawl..."):
        full_context = firecrawl_scrape(url, depth)

    with st.expander("📄 Raw Extracted Content (from all crawled pages)", expanded=False):
        st.text_area("Website Text", value=full_context[:15000], height=300)

    with st.spinner("🤖 Structuring modules using OpenRouter LLM..."):
        structured_output = query_openrouter(full_context)

    st.subheader("📂 Structured Documentation Modules")
    st.markdown(structured_output)
