import os
# Gerenciamento local de chaves de API
import dotenv
import asyncio
from types import SimpleNamespace
from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain.agents import create_agent
from langchain.messages import ToolMessage, AIMessage

dotenv.load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

# Pasta do projeto
projeto_dir = os.path.dirname(__file__)

# Prompt de sistema
system_prompt = """
Você é um agente clínico especializado em gerenciar informações de pacientes. Sua função é consultar os dados dos pacientes e cadastrar novos pacientes quando solicitado. Utilize as ferramentas do MCP para executar as tarefas.

 Os usuários podem realizar as seguintes ações:
 - solicitar informações sobre os pacientes a partir de seu CPF;
 - solicitar o cadastra de novos pacientes fornecendo obrigatoriamente seu nome, CPF, telefone e convênio;
 - consultar horários disponíveis para atendimento de uma especialidade, com a possibilidade de indicar uma data específica (opcional);
 - agendar uma consulta para um paciente, indicando o CPF do paciente, o identificador do horário desejado e uma observação (opcional).

 Antes de agendar uma consulta considere as seguintes orientações:
 - não é necessário verificar se o CPF do paciente é válido;
 - caso além da data do atendimento o usuário informe uma hora, compare esta hora com a hora dos horários disponíveis no dia e especialidade desejados. Caso o horário não esteja disponível avise ao usuário com a seguinte mensagem: "O horário informado não está disponível. Por favor, escolha outro horário ou data".
"""

client = MultiServerMCPClient(
    {
        "clinic": {
            "transport": "stdio",  # Local subprocess communication
            "command": "python",
            # Absolute path to your math_server.py file
            "args": [os.path.join(projeto_dir, "clinica_mcp", "clinica_mcp.py")],
        }
    }
)

tools = asyncio.run(client.get_tools())

agent = create_agent(
    "gpt-4o-mini",
    tools  
)

def extrair_resposta(response: dict):
    output = {}
    for message in response["messages"]:
        if isinstance(message, ToolMessage) and message.artifact:
            output["objeto"] = message.artifact["structured_content"]
            continue
        if isinstance(message, AIMessage):
            output["conteudo"] = message.content
            continue
    return output

async def responder_pergunta(pergunta: str):
    paciente_response = await agent.ainvoke(
        {"messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pergunta}

        ]}
    )
    return extrair_resposta(paciente_response)

if __name__ == "__main__":
    print(asyncio.run(responder_pergunta("Busque o paciente com CPF 11111111111")))