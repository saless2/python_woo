# ✍️ Automação Adobe Sign API (Python + Tkinter)

Este projeto é uma ferramenta em Python que automatiza o envio de documentos PDF para assinatura eletrónica através da API v6 do Adobe Sign (Acrobat Sign). Inclui uma interface gráfica simples (GUI) para facilitar a introdução do e-mail do cliente, ocultando a necessidade de usar a linha de comandos.

## ✨ Funcionalidades

* **Upload de Documentos (Transient Documents):** Envia ficheiros PDF locais para os servidores do Adobe de forma segura.
* **Criação de Acordos (Agreements):** Gera pedidos de assinatura eletrónica de forma automatizada.
* **Interface Simples:** Utiliza `Tkinter` para apresentar uma janela pop-up que pede o e-mail do destinatário.
* **Segurança Reforçada:** Utiliza variáveis de ambiente (`.env`) para garantir que tokens e credenciais não ficam expostos no código-fonte.

## 🛠️ Pré-requisitos

Certifique-se de que tem o seguinte instalado no seu computador:
* [Python 3.8+](https://www.python.org/downloads/)
* Uma conta de programador/API no [Adobe Acrobat Sign](https://acrobat.adobe.com/pt/pt/sign.html).

# 🚀 Como Utilizar
Passo 1: Obter o Token de Acesso (Apenas na 1ª vez ou quando expirar)
Se ainda não tem um Access Token, ou se o seu token expirou, execute o script de autenticação para o gerar a partir do seu código de autorização:
```bash
python obter_token.py
```
* Copie o Access Token gerado no terminal e cole-o no seu ficheiro .env na variável ADOBE_ACCESS_TOKEN.

Passo 2: Enviar um Documento para Assinatura
Certifique-se de que o caminho para o seu ficheiro PDF está correto na variável ADOBE_PDF_PATH do seu .env. Depois, basta executar o script principal:

```bash
python enviar_documento.py
```
* Irá abrir uma pequena janela no seu ecrã.

* Digite o e-mail da pessoa que deve assinar o documento.

* Clique em OK.

* Acompanhe o progresso do upload e envio através do terminal. Se for bem-sucedido, receberá a mensagem "🔥 Sucesso total!".

# 📂 Estrutura do Projeto
* obter_token.py - Script responsável por trocar o Authorization Code pelos Tokens de Acesso e Refresh da API do Adobe.

* enviar_documento.py - Script principal que faz o upload do PDF e gera o pedido de assinatura com interface gráfica.

* .env.example - Ficheiro de exemplo com a estrutura das variáveis de ambiente (sem valores reais) para orientar novos utilizadores.

### Bibliotecas Python Necessárias
Abra o terminal e instale as dependências executando:

```bash
pip install requests python-dotenv
