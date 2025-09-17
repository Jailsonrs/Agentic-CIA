from langchain.evaluation import load_evaluator
from langchain_openai import ChatOpenAI
import prompt

# LLM que vai atuar como "juiz"
llm = ChatOpenAI(model="gpt-4o-mini")

# Carrega avaliador de critério (corrigir, relevância, etc.)
evaluator = load_evaluator("criteria", llm=llm, criteria="correctness")

# Pergunta do usuário
input_text = "o produto veio danificado e eu gostaria de devolver"

# Resposta do modelo SAC
predicted_response = "Nosso SAC funciona de segunda a sexta, das 8h às 18h."

# Resposta ideal (ground truth, se você tiver)
reference = """Se você já recebeu o produto
Solicite a devolução do produto em até 7 dias corridos através do SAC.
Se você ainda não recebeu o produto
A nossa orientação é que você negue o recebimento do produto quando ele chegar. Após alguns dias, assim que a marca parceira receber o seu produto de volta, você receberá um e-mail informando que o processo de cancelamento será iniciado.
Se você negou o recebimento há mais de 10 dias e ainda não recebeu uma comunicação, entre em contato através dos nossos canais de atendimento. O atendimento por telefone é realizado de segunda a domingo, das 09h, às 22h"
"""
# Avaliação
result = evaluator.evaluate_strings(
    input=input_text,
    prediction=predicted_response,
    reference=reference,
)

print(result)
