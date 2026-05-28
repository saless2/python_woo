import os
import requests
import tkinter as tk
from tkinter import simpledialog

# ==============================================================================
# CONFIGURAÇÕES DO ADOBE SIGN E AMBIENTE
# ==============================================================================
# O Access Token deve ser mantido em segredo absoluto.
# Utilize o ficheiro .env (como explicado no script de autenticação) para guardar isto.
# Exemplo no .env: ADOBE_ACCESS_TOKEN=3AAABLblqZhCNtkPe4c...
ACCESS_TOKEN = os.environ.get("ADOBE_ACCESS_TOKEN", "COLOQUE_SEU_ACCESS_TOKEN_AQUI")

# O BASE_URL depende da região da sua conta (shard).
# Pode ser eu1, eu2, na1, na2, etc. Verifique na documentação ou no seu painel.
BASE_URL = os.environ.get("ADOBE_BASE_URL", "https://api.eu1.adobesign.com/api/rest/v6")

# Caminho do documento que será enviado.
# Dica: Em caminhos no Windows, use barras normais (/) ou adicione um 'r' antes da string: r"C:\Caminho\..."
CAMINHO_PDF = os.environ.get("ADOBE_PDF_PATH", "C:/Users/z0057mmt/Documents/docTesteAdobe.pdf")

# Nome que aparecerá no e-mail do cliente e no seu painel do Adobe Sign.
NOME_DO_ACORDO = "Contrato de Prestação de Serviços - Teste"


def enviar_para_assinatura(email_destino):
    """
    Faz o upload de um ficheiro local (Transient Document) e cria um Acordo (Agreement)
    para ser assinado pelo e-mail fornecido.
    """

    # ---------------------------------------------------------
    # PASSO 1: Fazer o Upload do Arquivo (Transient Document)
    # ---------------------------------------------------------
    url_transient = f"{BASE_URL}/transientDocuments"
    headers_upload = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    if not os.path.exists(CAMINHO_PDF):
        print(f"❌ Erro: O arquivo não foi encontrado no caminho especificado:\n{CAMINHO_PDF}")
        return

    print("A fazer o upload do ficheiro PDF para os servidores do Adobe Sign...")

    with open(CAMINHO_PDF, "rb") as arquivo:
        files = {
            # O Adobe precisa do nome do ficheiro, do conteúdo (stream) e do MimeType
            "File": (os.path.basename(CAMINHO_PDF), arquivo, "application/pdf")
        }
        response_transient = requests.post(url_transient, headers=headers_upload, files=files)

    if response_transient.status_code != 201:
        print(f"❌ Erro no upload (Código {response_transient.status_code}):")
        print(response_transient.text)  # Mostra o erro exato retornado pela API
        return

    transient_id = response_transient.json().get("transientDocumentId")
    print(f"✅ Upload concluído! ID Temporário: {transient_id[:15]}...\n")

    # ---------------------------------------------------------
    # PASSO 2: Criar o Acordo e Enviar para Assinatura
    # ---------------------------------------------------------
    url_agreements = f"{BASE_URL}/agreements"
    headers_json = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # Estrutura JSON exigida pela API v6 para criar um Acordo
    payload_agreement = {
        "fileInfos": [
            {"transientDocumentId": transient_id}  # Usa o ID gerado no Passo 1
        ],
        "name": NOME_DO_ACORDO,
        "participantSetsInfo": [
            {
                "memberInfos": [{"email": email_destino}],  # O e-mail capturado pela interface
                "order": 1,
                "role": "SIGNER"  # Papel: Assinante
            }
        ],
        "signatureType": "ESIGN",  # Assinatura Eletrónica
        "state": "IN_PROCESS"  # IN_PROCESS envia o e-mail imediatamente. DRAFT apenas guarda como rascunho.
    }

    print(f"A enviar solicitação de assinatura para: {email_destino} ...")
    response_agreement = requests.post(url_agreements, headers=headers_json, json=payload_agreement)

    if response_agreement.status_code == 201:
        id_acordo = response_agreement.json().get('id')
        print(f"🔥 Sucesso total! O documento foi enviado.")
        print(f"ID do Acordo: {id_acordo}")
    else:
        print(f"❌ Erro ao criar o acordo (Código {response_agreement.status_code}):")
        print(response_agreement.text)


# ==============================================================================
# INTERFACE GRÁFICA (Tkinter)
# ==============================================================================
def pedir_email_interface():
    """
    Abre uma pequena caixa de diálogo do Windows/Mac para pedir o e-mail do cliente,
    evitando que o utilizador precise de usar o terminal.
    """
    root = tk.Tk()
    root.withdraw()  # Esconde a janela base (fundo cinza) do Tkinter

    # Abre a caixa de diálogo de entrada de texto
    email_digitado = simpledialog.askstring(
        title="Novo Documento Adobe Sign",
        prompt="Digite o e-mail do cliente que vai assinar:"
    )
    return email_digitado


if __name__ == "__main__":
    # 1. Abre a interface a pedir o e-mail
    email_capturado = pedir_email_interface()

    # 2. Verifica se o utilizador digitou algo e clicou em 'OK' (se cancelar, retorna None)
    if email_capturado:
        # Remove espaços vazios acidentais antes e depois do e-mail
        email_limpo = email_capturado.strip()
        enviar_para_assinatura(email_limpo)
    else:
        print("Operação cancelada. Nenhum e-mail foi informado.")