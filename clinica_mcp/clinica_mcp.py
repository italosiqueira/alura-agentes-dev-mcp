from fastmcp import FastMCP
import requests
import json

# Define o endpoint da API
url = "http://127.0.0.1:8000"

# Define um Servidor MCP com a biblioteca FastMCP 
mcp = FastMCP("Clinica MCP")

@mcp.tool
async def buscar_paciente_por_cpf(cpf: str):
    """Busca um paciente pelo CPF."""
    response = requests.get(f"{url}/pacientes/{cpf}")
    return response.json()

@mcp.tool
async def cadastrar_paciente(nome: str, cpf: str, telefone: str, convenio: str):
    """Cadastra um novo paciente."""
    payload = {
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "convenio": convenio
    }
    response = requests.post(f"{url}/pacientes", json=payload)
    if response.status_code == 200:
        return response.json()["mensagem"]
    else:
        return response.json().detail[0]

if __name__ == "__main__":
    mcp.run(transport="stdio")