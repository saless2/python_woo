from dotenv import load_dotenv
load_dotenv() # Isto carrega automaticamente as variáveis do ficheiro .env

import os
import requests


# ==============================================================================
# CONFIGURAÇÕES DE AUTENTICAÇÃO E OAUTH
# ==============================================================================
# As credenciais estão a ser chamadas via variáveis de ambiente para segurança.
# Caso as variáveis não existam, o segundo parâmetro (ex: "COLOQUE_SEU...")
# serve como um fallback temporário ou aviso.

# 1. CLIENT_ID (ID de Aplicação)
# COMO OBTER:
#   1. Faça login na sua conta do Adobe (Acrobat Sign).
#   2. Vá para o separador "Conta" (Account) > "API do Acrobat Sign" > "Aplicações de API".
#   3. Crie uma nova aplicação ou clique para ver uma existente.
#   4. O "ID da Aplicação" (Application ID) apresentado é o seu CLIENT_ID.
CLIENT_ID = os.environ.get("ADOBE_CLIENT_ID", "COLOQUE_SEU_CLIENT_ID_AQUI")

# 2. CLIENT_SECRET (Segredo do Cliente)
# COMO OBTER:
#   1. Na mesma página da sua Aplicação de API no painel do Adobe Sign.
#   2. Clique em "Configurar OAuth para Aplicação" (Configure OAuth for Application).
#   3. O "Client Secret" estará visível nesta página. Copie-o.
CLIENT_SECRET = os.environ.get("ADOBE_CLIENT_SECRET", "COLOQUE_SEU_CLIENT_SECRET_AQUI")

# 3. AUTHORIZATION_CODE (Código de Autorização)
# COMO OBTER:
#   ATENÇÃO: Este código tem um tempo de vida muito curto (minutos) e é de uso ÚNICO.
#   1. Tem de construir uma URL de autorização contendo o seu client_id, redirect_uri e scopes (permissões).
#   2. Cole essa URL no seu browser e autorize a aplicação.
#   3. O Adobe irá redirecioná-lo para a sua redirect_uri (ex: https://localhost) com um parâmetro na URL:
#      Exemplo: https://localhost/?code=CBNCKBAAHBCAABAA...
#   4. Copie o valor que está depois de "?code=" e use-o aqui.
AUTHORIZATION_CODE = os.environ.get("ADOBE_AUTH_CODE", "COLOQUE_SEU_AUTH_CODE_AQUI")


def obter_token():
    url = "https://api.echosign.com/oauth/v2/token"

    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        # O redirect_uri DEVE ser exatamente o mesmo configurado no painel da Aplicação do Adobe Sign
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

        # Dica: Guarde o 'refresh_token' de forma segura.
        # Ele serve para gerar novos 'access_tokens' sem precisar de fazer login novamente.
    else:
        print("Erro ao obter o token. Detalhes:")
        print(response.text)


if __name__ == "__main__":
    obter_token()