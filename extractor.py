import streamlit as st
import asyncio
from crawl4ai import AsyncWebCrawler
from extractor import infer_modules  # Your existing LLM-based extractor
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Pulse-AI Module Extractor", layout="wide")
st.title("🧠 Pulse-AI Help Documentation Module Extractor")

st.markdown("""
This tool extracts **modules**, **submodules**, and their **descriptions** from product help/documentation URLs.
""")

urls = st.text_area("Enter one or more documentation URLs (one per line):", height=150)
submit = st.button("🔍 Extract Modules")

if submit and urls:
    url_list = [url.strip() for url in urls.splitlines() if url.strip()]

    async def process_urls(urls):
        async with AsyncWebCrawler() as crawler:
            for url in urls:
                st.markdown(f"---\n### 🔗 Processing: {url}")
                with st.spinner("Crawling pages..."):
                    try:
                        result = await crawler.arun(url=url)
                        page_text = result.markdown
                        st.success("✅ Content fetched successfully.")

                        if not page_text:
                            st.warning("No content extracted from the page.")
                            continue

                        st.markdown("#### 📝 Sample Extracted Content")
                        st.text(page_text[:1000] + "...")  # Show preview

                        with st.spinner("Extracting modules using LLM..."):
                            results = infer_modules([page_text])

                        for idx, res in enumerate(results):
                            st.markdown(f"##### ✅ Output from Chunk {idx+1}")
                            st.json(res)
                    except Exception as e:
                        st.error(f"Error processing {url}: {e}")

    asyncio.run(process_urls(url_list))
