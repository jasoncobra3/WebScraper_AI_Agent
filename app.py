import gradio as gr
import asyncio
from crawl4ai import AsyncWebCrawler
from urllib.parse import urlparse
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_groq import ChatGroq
import re
import os
from dotenv import load_dotenv
load_dotenv()


GROQ_API_KEY=os.getenv("GROQ_API_KEY")

qa_chain = None
scraped_file = None

# Clean LLM output
class StrictOutputParser(StrOutputParser):
    def parse(self, text: str) -> str:
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        text = re.sub(r'^(Reasoning|Thought|Analysis):.*?\n', '', text, flags=re.IGNORECASE)
        return text.strip()

# Async crawl function
async def crawl_site(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        return result.markdown

# UI-triggered scraper
def scrape_website(url):
    global scraped_file
    markdown = asyncio.run(crawl_site(url))
    domain = urlparse(url).netloc.replace("www.", "")
    filename = f"{domain}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown)
    scraped_file = filename
    return filename, markdown

# Query setup
def setup_qa():
    global qa_chain
    loader = TextLoader(scraped_file, encoding="utf-8")
    docs = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(loader.load())
    vectorstore = FAISS.from_documents(docs, HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))
    retriever = vectorstore.as_retriever()
    prompt = PromptTemplate.from_template("""
You are an AI assistant. Return ONLY the final answer.

**Rules (MUST follow):**
1. NO <think>, reasoning, or explanations.
2. NO markdown/formatting tags.
3. Answer in 3-4 concise sentences.

Context:
{context}

Question:
{question}

Answer (direct and short):""")

    llm = ChatGroq(
        api_key=GROQ_API_KEY,  # Use environment variable for security
        model="deepseek-r1-distill-llama-70b",
        temperature=0.0
    )

    qa_chain = (
        RunnableMap({
            "context": retriever,
            "question": RunnablePassthrough()
        }) | prompt | llm | StrictOutputParser()
    )
    return "✅ Query system ready!"

# Handle questions
def ask_question(query):
    if not qa_chain:
        return "❗ Please set up the QA system first."
    return qa_chain.invoke(query)

# Gradio interface
with gr.Blocks(title="Web Scraping AI Agent") as demo:
    gr.Markdown("## 🌐 Website Scraper AI Agent")

    url_input = gr.Textbox(label="Enter Website URL")
    scrape_btn = gr.Button("🔍 Scrape Website")
    download_output = gr.File(label="📄 Download Scraped File")
    markdown_box = gr.Textbox(label="Scraped Text", lines=10)
    
    setup_btn = gr.Button("💬 Query This Website")
    setup_status = gr.Textbox(label="Status")

    query_input = gr.Textbox(label="Ask a Question")
    query_btn = gr.Button("Ask")
    query_output = gr.Textbox(label="Answer")

    # Wire components
    scrape_btn.click(fn=scrape_website, inputs=[url_input], outputs=[download_output, markdown_box])
    setup_btn.click(fn=setup_qa, outputs=setup_status)
    query_btn.click(fn=ask_question, inputs=[query_input], outputs=[query_output])

# Run
demo.launch(share=True)
