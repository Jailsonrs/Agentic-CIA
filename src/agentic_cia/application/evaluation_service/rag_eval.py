from langsmith import client
from langsmith import traceable
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate



loader = TextLoader("./data/dados-sac.md", encoding="utf8")
sac_doc = loader.load()

### splitar os documentos
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=250,  # chunk size (characters)
    chunk_overlap=100,  # chunk overlap (characters)
    add_start_index=True,  # track index in original document
)

all_splits = text_splitter.split_documents(sac_doc)

embeddings = OllamaEmbeddings(model  = "nomic-embed-text:latest")
vector_store = Chroma(
    collection_name="SAC_DATA",
    embedding_function=embeddings,
)
vector_store.add_documents(documents = all_splits)

retriever  = vector_store.as_retriever(k=8)

@traceable()
def rag_bot(question: str) -> dict:
    # LangChain retriever will be automatically traced
    docs = retriever.invoke(question)
    docs_string = "".join(doc.page_content for doc in docs)
    instructions = f"""You are a helpful assistant who is good at analyzing source information and answering questions.
       Use the following source documents to answer the user's questions.
       If you don't know the answer, just say that you don't know.
       Use three sentences maximum and keep the answer concise.

Documents:
{docs_string}"""
    # langchain ChatModel will be automatically traced
    ai_msg = llm.invoke([
            {"role": "system", "content": instructions},
            {"role": "user", "content": question},
        ],
    )
    return {"answer": ai_msg.content, "documents": docs}



client = Client()

# Define the examples for the dataset
examples = [
    {
        "inputs": {"question": "How does the ReAct agent use self-reflection? "},
        "outputs": {"answer": "ReAct integrates reasoning and acting, performing actions - such tools like Wikipedia search API - and then observing / reasoning about the tool outputs."},
    },
    {
        "inputs": {"question": "What are the types of biases that can arise with few-shot prompting?"},
        "outputs": {"answer": "The biases that can arise with few-shot prompting include (1) Majority label bias, (2) Recency bias, and (3) Common token bias."},
    },
    {
        "inputs": {"question": "What are five types of adversarial attacks?"},
        "outputs": {"answer": "Five types of adversarial attacks are (1) Token manipulation, (2) Gradient based attack, (3) Jailbreak prompting, (4) Human red-teaming, (5) Model red-teaming."},
    },
]

# Create the dataset and examples in LangSmith
dataset_name = "Lilian Weng Blogs Q&A"
dataset = client.create_dataset(dataset_name=dataset_name)
client.create_examples(
    dataset_id=dataset.id,
    examples=examples
)