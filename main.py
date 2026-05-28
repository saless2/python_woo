import os
import requests
import tkinter as tk
from tkinter import simpledialog

# --- CONFIGURAÇÕES DO ADOBE SIGN ---
ACCESS_TOKEN = "3AAABLblqZhCNtkPe4c3Qq-ESBPQJeX0oNVoewLNUHuOLH7aAcFJSumk6N6Zd6deEs2HKhE9__20A0XgdSgsFEl4lk7NTGc0a"
BASE_URL = "https://api.eu1.adobesign.com/api/rest/v6"

CAMINHO_PDF = "C:/Users/z0057mmt/Documents/docTesteAdobe.pdf"
NOME_DO_ACORDO = "Contrato de Prestação de Serviços - Teste"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}


# Transformamos a função para receber o e-mail como parâmetro
def enviar_para_assinatura(email_destino):
    url_transient = f"{BASE_URL}/transientDocuments"

    if not os.path.exists(CAMINHO_PDF):
        print(f"Erro: O arquivo {CAMINHO_PDF} não foi encontrado.")
        return

    print(f"Subindo o arquivo PDF para o Adobe Sign...")
    with open(CAMINHO_PDF, "rb") as arquivo:
        files = {
            "File": (os.path.basename(CAMINHO_PDF), arquivo, "application/pdf")
        }
        response_transient = requests.post(url_transient, headers=headers, files=files)

    if response_transient.status_code != 201:
        print(f"Erro no upload: {response_transient.status_code}")
        return

    transient_id = response_transient.json().get("transientDocumentId")
    print(f"Upload concluído! ID: {transient_id}\n")

    url_agreements = f"{BASE_URL}/agreements"
    headers_json = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload_agreement = {
        "fileInfos": [{"transientDocumentId": transient_id}],
        "name": NOME_DO_ACORDO,
        "participantSetsInfo": [
            {
                "memberInfos": [{"email": email_destino}],  # <-- Usa o e-mail digitado aqui
                "order": 1,
                "role": "SIGNER"
            }
        ],
        "signatureType": "ESIGN",
        "state": "IN_PROCESS"
    }

    print(f"Enviando solicitação de assinatura para {email_destino}...")
    response_agreement = requests.post(url_agreements, headers=headers_json, json=payload_agreement)

    if response_agreement.status_code == 201:
        print(f"🔥 Sucesso total! O documento foi enviado.")
    else:
        print(f"Erro ao criar o acordo: {response_agreement.status_code}")


# --- FUNÇÃO DA INTERFACE GRÁFICA ---
def pedir_email_interface():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela base do sistema

    # Abre a caixa de diálogo
    email_digitado = simpledialog.askstring(
        "Novo Documento",
        "Digite o e-mail de quem vai assinar:"
    )
    return email_digitado


if __name__ == "__main__":
    # 1. Abre a interface pedindo o e-mail
    email_capturado = pedir_email_interface()

    # 2. Se o usuário digitou algo e não cancelou, roda o envio
    if email_capturado:
        enviar_para_assinatura(email_capturado)
    else:
        print("Envio cancelado. Nenhum e-mail foi informado.")