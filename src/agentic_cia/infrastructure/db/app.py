# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
import logging

# ---------------------------
# Configuração de logging
# ---------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------
# Configuração FastAPI
# ---------------------------
app = FastAPI(title="SAC C&A API", version="1.0")

# ---------------------------
# Modelos de request/response
# ---------------------------
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

# ---------------------------
# Inicialização do agente (executa 1x no startup)
# ---------------------------
logger.info("Carregando documentos...")
loader = TextLoader("./data/dados-sac.md", encoding="utf8")
sac_doc = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=10,
    add_start_index=True,
)
all_splits = text_splitter.split_documents(sac_doc)

# Persistência do Chroma
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = Chroma(
    collection_name="SAC_DATA",
    embedding_function=embeddings,
    persist_directory="./chroma_sac"
)

if not vector_store._collection.count():
    logger.info("Criando embeddings e persistindo no Chroma...")
    vector_store.add_documents(all_splits)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# LLM
llm = OllamaLLM(
    model="qwen3:14b",
    gpu=True,
    temperature=0.1,
    top_k=10
)

# Prompt
template_sac_cea = PromptTemplate(
    input_variables=["context", "question"],
    template="""Você é um especialista em SAC da C&A... 
{context}
Pergunta: {question}"""
)

# RetrievalQA
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": template_sac_cea}
)

# ---------------------------
# Rota principal
# ---------------------------
@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    logger.info(f"Pergunta recebida: {request.question}")
    result = qa_chain.invoke(request.question)
    return QueryResponse(answer=result["result"])
