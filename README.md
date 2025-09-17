---
title: AgenteCiA -- Sistema de Chat RAG
---

# Descrição do Projeto

AgenteCiA é uma aplicação de **chat baseado em RAG (Retrieval-Augmented
Generation)** que integra múltiplos serviços de atendimento ao cliente
(SAC) e produtos, permitindo respostas automatizadas e contextualizadas
a perguntas dos usuários.

O projeto segue uma arquitetura modular, separando:

-   **API**: endpoints FastAPI

-   **Application**: lógica de negócio, serviços de chat, ingestão de
    documentos, avaliação e reset de memória

-   **Domain**: regras de negócio, prompts, utilitários e exceções

-   **Infrastructure**: comunicação com banco de dados, provedores de
    LLM, clientes externos e monitoramento

# Funcionalidades Principais

-   Endpoint `/chat` que recebe perguntas e retorna respostas via RAG

-   Suporte a múltiplos serviços de chat (`chat_sac`, `chat_prod`)

-   Histórico opcional de conversas

-   Impressão de respostas formatadas no terminal com **bullet points**

-   Extensível para novos serviços de chat via `ChatServiceFactory`

# Instalação e Setup Local

1.  Clonar o repositório:

    ``` {.bash language="bash"}
    git clone <URL_DO_REPO>
    cd agentic-cia
    ```

2.  Criar e ativar o ambiente virtual:

    ``` {.bash language="bash"}
    python -m venv .venv
    source .venv/bin/activate  # Linux / MacOS
    .venv\Scripts\activate     # Windows
    ```

3.  Instalar dependências:

    ``` {.bash language="bash"}
    pip install -r requirements.txt
    ```

4.  Instalar Ollama CLI e modelos:

    ``` {.bash language="bash"}
    # Linux / MacOS
    brew install ollama
    ollama pull nomic/embedding-text
    ollama pull qwen/qwen-3:14b

    # Windows
    winget install Ollama.Ollama
    ollama pull nomic/embedding-text
    ollama pull qwen/qwen-3:14b
    ```

5.  Rodar a API:

    ``` {.bash language="bash"}
    uvicorn application.api.main:app --reload --host 0.0.0.0 --port 8000
    ```

# Endpoints Disponíveis

## Listar serviços disponíveis

``` {.http language="http"}
GET /api/services
```

Exemplo de resposta:

``` {.json language="json"}
{
  "services": ["chat_sac", "chat_prod"]
}
```

## Enviar mensagem para o chat

``` {.http language="http"}
POST /api/chat
Content-Type: application/json
```

Exemplo de payload:

``` {.json language="json"}
{
  "service": "chat_sac",
  "message": "Como posso abrir uma conta?"
}
```

Exemplo de resposta:

``` {.json language="json"}
{
  "response": "Para abrir uma conta, você precisa apresentar documento de identidade, CPF e preencher o formulário online..."
}
```

# Fluxo da Aplicação

1.  O usuário envia uma mensagem via endpoint `/chat`.

2.  O endpoint seleciona o serviço de chat correto via
    `ChatServiceFactory`.

3.  O serviço chama o **RAG (qa_chain)** para buscar informações nos
    documentos do SAC.

4.  A resposta é retornada como string para o endpoint.

5.  Opcionalmente, a resposta é impressa no terminal com **bullet
    points**.

## Diagrama textual do fluxo

    Usuário
       │
       ▼
    POST /api/chat  ----> FastAPI Endpoint (chat)
                               │
                               ▼
                   ChatServiceFactory seleciona serviço
                               │
                               ▼
                ChatSacService / ChatProdService
                               │
                               ▼
                     RAG (qa_chain) → busca nos documentos
                               │
                               ▼
                       Resposta formatada
                               │
                               ▼
                      Retorno ao usuário

## Fluxo Interno do RAG com Ollama

O RAG utiliza:

-   **Ollama Embeddings**: `nomic-embed-text` para criar vetores a
    partir dos documentos

-   **Ollama LLM**: `qwen3:14b` para gerar respostas a partir do
    contexto recuperado

```{=html}
<!-- -->
```
    Documentos SAC (.md)
          │
          ▼
    TextSplitter → Divide em chunks
          │
          ▼
    OllamaEmbeddings (nomic-embed-text)
          │
          ▼
    Chroma Vector Store → Indexação dos chunks
          │
          ▼
    Retriever (busca por similaridade)
          │
          ▼
    Ollama LLM (qwen3:14b)
          │
          ▼
    Resposta gerada → Retorno ao usuário

# Perguntas Comuns para SAC

-   Qual o prazo de entrega do meu pedido?

-   Como faço para rastrear meu pedido?

-   Posso alterar o endereço de entrega depois de comprar?

-   Como solicitar reembolso?

-   Meu produto está com defeito, como proceder?

-   Quais são os horários de atendimento?

-   Como falar com um atendente humano?

-   Como criar ou recuperar minha conta?

# Observações

-   O RAG utiliza documentos do SAC (`data/dados-sac.md`) e embeddings
    via Ollama.

-   Serviços de chat podem ser adicionados criando uma classe que herde
    de `ChatService`.

-   O terminal imprime respostas formatadas com bullet points para
    facilitar depuração.

# Exemplo de Teste via `curl`

``` {.bash language="bash"}
curl -X POST http://127.0.0.1:8000/api/chat \
-H "Content-Type: application/json" \
-d '{"service":"chat_sac","message":"Como posso abrir uma conta?"}'
```

Saída esperada no terminal:

    Resposta do chat:

    • Para abrir uma conta, você precisa apresentar documento de identidade
    • CPF e preencher o formulário online
    • Confirme seus dados e aguarde a ativação da conta

# Como Adicionar Novos Serviços de Chat

1.  Criar uma nova classe que herde de `ChatService`:

    ``` {.python language="python"}
    from application.chat_service_base import ChatService

    class ChatNovoServico(ChatService):
        def generate_response(self, message, history=None):
            # Implementar lógica
            return "Resposta automática"
    ```

2.  Registrar no `chat_service_factory.py`:

    ``` {.python language="python"}
    _registry["chat_novo"] = ChatNovoServico
    ```

    Agora o endpoint `/chat` poderá utilizar o novo serviço:

    ``` {.json language="json"}
    {
      "service": "chat_novo",
      "message": "Olá!"
    }
    ```
