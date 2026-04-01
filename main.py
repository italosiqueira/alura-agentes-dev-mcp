import asyncio
import client

def efetua_pergunta():
    print('---\n')
    return input('# PERGUNTA (digite "sair" para encerrar) \n')

async def inicia_chat():
    print('### BEM-VINDO AO AGENTE CLÍNICO. ###')

    prompt = efetua_pergunta()

    while prompt.strip().lower() != 'sair':
        resposta = await client.responder_pergunta(prompt)
        print(f"\n# Resposta:\n {resposta['conteudo']}\n")
        prompt = efetua_pergunta()
    
    print('### OBRIGADO POR USAR O AGENTE CLÍNICO! ATÉ LOGO! ###')

if __name__ == "__main__":
    asyncio.run(inicia_chat())