from fastmcp import FastMCP
import requests
import json

# Define o endpoint da API
url = "http://127.0.0.1:8000"

# Define um Servidor MCP com a biblioteca FastMCP 
mcp = FastMCP("Clinica MCP")

@mcp.tool(name="buscar_paciente_por_cpf")
async def buscar_paciente_por_cpf(cpf: str):
    """
    Busca um paciente pelo CPF.

    Args:
        cpf (str): O CPF do paciente a ser buscado.

    Returns:
        dict: Um dicionário contendo:
            - Se paciente encontrado:
                - "sucesso" (bool): True
                - "paciente" (dict): Dados do paciente com os campos:
                    - "id" (int):  ID do paciente
                    - "nome" (str): Nome do paciente
                    - "cpf" (str): CPF do paciente
                    - "telefone" (str): Telefone do paciente
                    - "convenio" (str): Convênio do paciente
                    - "criado_em" (str): Data e hora de criação do registro
            - Se paciente não encontrado:
                - "sucesso" (bool): False
                - "mensagem" (str): Mensagem de erro
    """
    response = requests.get(f"{url}/pacientes/{cpf}")
    if (response.status_code == 200):
        paciente = response.json()
        if paciente:
            return { "sucesso": True, "paciente": paciente }
        else:
            return { "sucesso": False, "mensagem": "Paciente não encontrado." }
    else:
        return { "sucesso": False, "mensagem": "Erro ao buscar paciente." }

@mcp.tool(name="cadastrar_paciente")
async def cadastrar_paciente(nome: str, cpf: str, telefone: str, convenio: str):
    """
    Cadastra um novo paciente.

    Args:
        nome (str): Nome do paciente
        cpf (str): CPF do paciente
        telefone (str): Telefone do paciente
        convenio (str): Convênio do paciente

    Returns:
        dict: Um dicionário contendo:
            - Se paciente encontrado:
                - "sucesso" (bool): True
                - "mensagem" (str): Mensagem do servidor
                - "paciente" (dict): Dados do paciente com os campos:
                    - "id" (int):  ID do paciente
                    - "nome" (str): Nome do paciente
                    - "cpf" (str): CPF do paciente
                    - "telefone" (str): Telefone do paciente
                    - "convenio" (str): Convênio do paciente
                    - "criado_em" (str): Data e hora de criação do registro
            - Se paciente já existe:
                - "sucesso" (bool): False
                - "mensagem" (str): Mensagem de aviso
            - Se paciente não encontrado:
                - "sucesso" (bool): False
                - "mensagem" (str): Mensagem de erro
    """
    payload = {
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "convenio": convenio
    }
    response = requests.post(f"{url}/pacientes", json=payload)
    
    if (response.status_code == 200):
        output = response.json()
        if output["sucesso"]:
            return { "sucesso": True, "mensagem": output["mensagem"], "paciente": output["paciente"] }
        else:
            return { "sucesso": False, "mensagem": "Paciente já cadastrado." }
    else:
        return { "sucesso": False, "mensagem": "Erro ao cadastrar paciente." }

@mcp.tool(name="consultar_horario")
async def consultar_horario(especialidade: str, data: str = ""):
    """
    Consulta os horários disponíveis para atendimento da especialidade desejada. Caso uma data seja informada, retorna os horários disponíveis para aquela data.
    Caso contrário, retorna todos os horários disponíveis para a especialidade.

    Args:
        especialidade (str): Especialidade médica a ser consultada
        data (str): Data para consulta no formato "YYYY-MM-DD"

    Returns:
        dict: Um dicionário contendo:
            - Se houver horários disponíveis:
                - "sucesso" (bool): True
                - "horarios" (list): Lista de horários disponíveis para a especialidade e data informados, onde cada item é um dicionário com os campos:
                    - "horario_id" (int): ID do horário,
                    - "data" (str): data do horário no formato YYYY-MM-DD
                    - "hora" (str): hora disponível, no formato HH:MM
                    - "medico_id" (int): ID do Médico
                    - "medico_nome" (str): Nome do Médico
                    - "especialidade" (str): Especialidade do Médico
            - Se não houver horários disponíveis:
                - "sucesso" (bool): False
                - "mensagem" (str): Mensagem indicando que não há horários disponíveis
            - Se ocorrer um erro durante a consulta:
                - "sucesso" (bool): False
                - "mensagem" (str): Mensagem informando que ocorreu um erro ao consultar os horários
    """
    payload = {
        "especialidade": especialidade
    }
    if data:
        payload["data"] = data

    response = requests.get(f"{url}/horarios", params=payload)
    if (response.status_code == 200):
        body = response.json()
        if body["quantidade"] > 0:
            return { "sucesso": True, "horarios": body["horarios"] }
        else:
            return { "sucesso": False, "mensagem": "Não há horário disponível." }
    else:
        return { "sucesso": False, "mensagem": "Erro ao buscar horários." }

@mcp.tool(name="agendar_consulta")
async def agendar_consulta(cpf: str, horario_id: int, observacoes: str = ""):
    """
    Agenda uma consulta para um paciente.

    Args:
        cpf (str): CPF do paciente
        horario_id (int): ID do horário a ser agendado
        observacoes (str): Observações adicionais para o agendamento (opcional)

    Returns:
        dict: Um dicionário contendo:
            - Se agendamento realizado com sucesso:
                - "sucesso" (bool): True
                - "mensagem" (str): Mensagem de sucesso
                - "agendamento" (dict): Dados do agendamento com os campos:
                    - "agendamento_id" (int): ID do agendamento
                    - "status" (str): Status do agendamento (ex: "agendado")
                    - "observacoes" (str): Observações do agendamento
                    - "paciente_nome" (str): Nome do paciente
                    - "cpf" (str): CPF do paciente
                    - "medico_nome" (str): Nome do médico
                    - "especialidade" (str): Especialidade médica
                    - "data" (str): Data da consulta no formato YYYY-MM-DD
                    - "hora" (str): Hora da consulta no formato HH:MM
            - Se não foi possível registrar o agendamento:
                - "sucesso" (bool): False
                - "mensagem" (str): Mensagem de erro indicando o provável motivo pelo qual o agendamento não pôde ser registrado (ex: paciente não encontrado, horário não encontrado, horário não disponível)
            - Se ocorrer um erro durante o processo:
                - "sucesso" (bool): False
                - "mensagem" (str): Mensagem de erro indicando que ocorreu um erro ao tentar agendar a consulta
    """
    pass

if __name__ == "__main__":
    mcp.run(transport="stdio")