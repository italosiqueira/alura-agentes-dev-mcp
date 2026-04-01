import os
# Gerenciamento local de chaves de API
import dotenv
import asyncio
from types import SimpleNamespace
from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain.agents import create_agent

dotenv.load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

# Pasta do projeto
projeto_dir = os.path.dirname(__file__)

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

async def load_agent():
    tools = await client.get_tools()
    return create_agent(
        "gpt-4o-mini",
        tools  
    )

async def responder_pergunta(pergunta: str):

    agent = await load_agent()

    paciente_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": pergunta}]}
    )

    output = paciente_response.get('messages')[3].content
    output_structured = paciente_response.get('messages')[2].artifact['structured_content']

    return output, output_structured

if __name__ == "__main__":
    print(asyncio.run(responder_pergunta("Busque o paciente com CPF 11111111111")))