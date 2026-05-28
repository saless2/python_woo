import requests

# 1. Preencha com os dados da sua aplicação Adobe Sign:
CLIENT_ID = "ats-70cd0459-b910-4793-be9c-c0e5d98561dd"  # O seu ID de Aplicação
CLIENT_SECRET = "K2U5kAmiGEMrgoW_BunfNBOHtIP1jEQI"  # O seu Client Secret
AUTHORIZATION_CODE = "CBNCKBAAHBCAABAA5xu6yW0ZeCLS-qDCizdiuT6DXkz8hLiC"


def obter_token():
    url = "https://api.echosign.com/oauth/v2/token"

    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "https://localhost",
        "code": AUTHORIZATION_CODE
    }

    print("A solicitar o Token de Acesso...")
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        dados = response.json()
        print("\nSUCESSO! Aqui estão as suas chaves:")
        print(f"Access Token: {dados.get('access_token')}\n")
        print(f"Refresh Token: {dados.get('refresh_token')}")
    else:
        print("Erro ao obter o token:")
        print(response.text)


if __name__ == "__main__":
    obter_token()