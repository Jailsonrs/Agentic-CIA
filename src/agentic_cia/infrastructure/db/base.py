from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate


loader = TextLoader("./data/dados-sac.md", encoding="utf8")
sac_doc = loader.load()

### splitar os documentos
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,  # chunk size (characters)
    chunk_overlap=10,  # chunk overlap (characters)
    add_start_index=True,  # track index in original document
)

all_splits = text_splitter.split_documents(sac_doc)

embeddings = OllamaEmbeddings(model  = "nomic-embed-text:latest")
vector_store = Chroma(
    collection_name="SAC_DATA",
    embedding_function=embeddings,
)
vector_store.add_documents(documents = all_splits)

retriever = vector_store.as_retriever(
    search_type="mmr",   # ou "mmr" (diversidade)
    search_kwargs={"k": 5}      # retorna 5 documentos mais parecidos
)



template_sac_cea = """
Você é um especialista em SAC (Serviço de Atendimento ao Cliente) da C&A.

Seu objetivo é atender o cliente com empatia, clareza e agilidade, sempre buscando resolver o problema ou esclarecer dúvidas de forma cordial e eficiente.

Siga este estilo de comunicação:
- Tom: gentil, objetivo, profissional e acolhedor.
- Linguagem: simples, clara e acessível (evite jargões técnicos).
- Trate o cliente sempre com respeito e pelo nome, quando possível.
- Sempre agradeça o contato.
- Em caso de erro da empresa, assuma a responsabilidade com empatia.
- Em caso de reclamações, acolha e demonstre interesse genuíno em resolver.
- Em caso de dúvidas, explique com clareza e proponha o próximo passo.

⚠️ Atenção:
- Nunca use respostas vagas como "estamos analisando" sem dar um prazo.
- Sempre forneça caminhos claros (ex: link, passo a passo, prazo, solução).
- Nunca prometa o que não pode cumprir.

### Exemplo de estrutura de resposta:

1. Saudação + Agradecimento
Olá, [nome do cliente]! Muito obrigado por entrar em contato com o SAC da C&A.

2. Reconhecimento da solicitação/dúvida
Entendemos que você [resuma brevemente o motivo do contato, com empatia].

3. Solução ou explicação clara
Segue abaixo as informações que você precisa:  
[explicação simples, direta, com instruções claras, se necessário].

4. Encaminhamento (se necessário)
Caso precise de mais ajuda, você também pode acessar [link ou canal de suporte adicional].

5. Encerramento cordial
Estamos sempre à disposição. Agradecemos por escolher a C&A! 😊  
Tenha um ótimo dia!

---

### Exemplos práticos de aplicação:

Reclamação sobre atraso na entrega:
Olá, Ana! Sentimos muito pelo atraso no seu pedido e entendemos sua frustração. Já verificamos em nosso sistema e o pedido #12345 está com nova previsão de entrega para o dia 18/09.

Sabemos o quanto isso é importante e estamos acompanhando de perto para garantir que chegue o quanto antes.

Caso não receba até essa data, por favor, nos avise por aqui ou pelo canal (xx) para que possamos intervir.

Agradecemos pela paciência e por escolher a C&A 💙

---

Dúvida sobre troca de produto:
Oi, João! Obrigado por falar com o SAC da C&A.

Você pode realizar a troca de produtos comprados online em até 30 dias após o recebimento, diretamente em qualquer loja física ou pelo site.


Qualquer dificuldade, é só nos chamar! Estamos aqui pra te ajudar.

### Informações relevantes dos documentos:
{context}

### Pergunta do cliente:
{question}
"""

prompt = ChatPromptTemplate.from_template(template_sac_cea)
model  = OllamaLLM(model = 'qwen3:14b', temperature = 0.1,gpu=True, num_gpu = 2,top_k = 200) 

qa_chain = RetrievalQA.from_chain_type(
    llm=model,
    retriever=retriever,
    chain_type="stuff",   # pode ser "map_reduce" ou "refine" também
    chain_type_kwargs={"prompt": prompt}  # usa o seu template do SAC
)

#chain  = prompt | model
results = qa_chain.invoke({"query": "quero minha nota fiscal"})
print(results["result"])

#results = chain.invoke({"question": "Como acessar a Nota Fiscal do pedido??"})

#rint(results)
# importar framework
# importar o splitter (recursive character splitter)
# importar modelo de embedding (provavelmente nomic embed)
# escolher o provedor. ollama?


# ##### evaluation 


# from langchain.evaluation import load_evaluator

# # LLM que vai atuar como "juiz"

# # Carrega avaliador de critério (corrigir, relevância, etc.)
# evaluator = load_evaluator("criteria", llm=model, criteria="correctness")
# # Pergunta do usuário
# input_text = "o produto veio danificado e eu gostaria de devolver"
# # Resposta do modelo SAC
# #predicted_response = results
# # Resposta ideal (ground truth, se você tiver)
# reference = """Se você já recebeu o produto
# Solicite a devolução do produto em até 7 dias corridos através do SAC.
# Se você ainda não recebeu o produto
# A nossa orientação é que você negue o recebimento do produto quando ele chegar. Após alguns dias, assim que a marca
#  parceira receber o seu produto de volta, você receberá um e-mail informando que o processo de cancelamento será iniciado.
# Se você negou o recebimento há mais de 10 dias e ainda não recebeu uma comunicação, entre em contato através dos nossos
#  canais de atendimento. O atendimento por telefone é realizado de segunda a domingo, das 09h, às 22h"
# """

# evaluator = load_evaluator("qa", llm=model, criteria="correctness")

# result = evaluator.evaluate_strings(
#     input="o produto veio danificado e eu gostaria de devolver",
#     prediction=results,
#     reference=reference,
# )

# print(result)



# # load docs  ok
# splitter docks <-
# embed docs
# prompt engineerying
# run chain
# expose to API
