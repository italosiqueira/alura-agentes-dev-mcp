import os
# Gerenciamento local de chaves de API
import dotenv
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain.agents import create_agent

dotenv.load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

# Pasta do projeto
projeto_dir = os.path.dirname(__file__)

async def main():
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

    tools = await client.get_tools()
    agent = create_agent(
        "gpt-4o-mini",
        tools  
    )

    paciente_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Busque o paciente com CPF 11111111111"}]}
    )

    print(f"Resposta do agente: {paciente_response.get('messages')[3].content}")

if __name__ == "__main__":
    asyncio.run(main())