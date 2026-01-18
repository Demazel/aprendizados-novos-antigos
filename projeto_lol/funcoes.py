import requests
import os

def obter_puuid():
    # Carregar API Key do arquivo
    try:
        with open("apikey.txt", "r") as f:
            api_key = f.read().strip()
    except FileNotFoundError:
        print("Erro: Arquivo apikey.txt não encontrado.")
        return None

    region = input("Digite a região (escolha entre americas, europe, asia, sea): ")
    game_name = input("Digite o nome do jogador: ")
    tag_line = input("Digite a tag do jogador: ")
    
    endpoint = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    
    headers = {
        "X-Riot-Token": api_key
    }
    
    try:
        resposta = requests.get(endpoint, headers=headers)
        
        # Verificar se a requisição foi bem sucedida
        if resposta.status_code == 200:
            dados = resposta.json()
            return dados["puuid"]
        elif resposta.status_code == 401:
            print("Erro 401: Chave de API inválida ou expirada.")
        elif resposta.status_code == 404:
            print(f"Erro 404: Riot ID {game_name}#{tag_line} não encontrado.")
        else:
            print(f"Erro {resposta.status_code}: {resposta.text}")
            
    except Exception as e:
        print(f"Ocorreu um erro na requisição: {e}")
        
    return None

puuid = obter_puuid()  
if puuid:
    print(f"PUUID encontrado: {puuid}")
else:
    print("Não foi possível obter o PUUID.")

