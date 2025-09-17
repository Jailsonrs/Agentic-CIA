
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain.docstore.document import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from agentic_cia.domain.prompts.prompt import template_sac_cea

loader = TextLoader("./data/dados-sac.md", encoding="utf8")
sac_doc = loader.load()

# ---------------------------
# 1. Load documents
# ---------------------------
# Split documents into chunks (bigger chunks = more GPU memory used)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,  # chunk size (characters)
    chunk_overlap=26,  # chunk overlap (characters)
    add_start_index=True,  # track index in original document
)

all_splits = text_splitter.split_documents(sac_doc)

# ---------------------------
# 2. Embeddings on GPU
# ---------------------------
# Make sure Ollama embeddings are GPU-enabled

embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Vector store
vector_store = Chroma(
    collection_name="SAC_DATA",
    embedding_function=embeddings,
)

vector_store.add_documents(documents = all_splits)

retriever = vector_store.as_retriever(
    search_type="similarity",   # ou "mmr" (diversidade)
    search_kwargs={"k": 15}      # retorna 5 documentos mais parecidos
)

# ---------------------------
# 3. Load LLM
# ---------------------------
llm = OllamaLLM(
    model="qwen3:14b",
    gpu=True,
    temperature=0.1,
    top_k = 5,
    reasoning= False
)
# ---------------------------
# 3. Pre built QA chain
# ---------------------------
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",  # 'stuff' keeps everything in memory, uses more VRAM
    chain_type_kwargs={"prompt": template_sac_cea}
)
