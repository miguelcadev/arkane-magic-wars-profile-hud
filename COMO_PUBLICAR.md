# Publicar o Grimório na Altare

CI/CD não é necessário. Ele automatiza verificações e publicações quando o código
muda. Para este projeto, você pode enviar os arquivos pelo painel.

## 1. Enviar os arquivos

Abra seu servidor Python na Altare e entre em Arquivos (Files).
Envie o ZIP e use a opção de extrair/descompactar, se disponível.
Se não houver essa opção, extraia no computador e envie os arquivos e as pastas.

Na pasta principal do servidor, a estrutura deve ficar assim:

```text
app.py
run.py
requirements.txt
templates/
    index.html
static/
    style.css
    ficha.png
```

O app.py deve ficar diretamente na pasta principal, sem uma pasta extra por fora.
Se já existirem arquivos com esses nomes, baixe uma cópia antes de substituí-los.

## 2. Configurar a inicialização

Em Inicialização (Startup), procure o campo do arquivo Python, que pode aparecer
como App py file ou PY_FILE, e informe `run.py`.
No campo do arquivo de dependências, mantenha `requirements.txt`.
O modelo Python instala as bibliotecas desse arquivo ao iniciar.

Abra Rede (Network) e anote o endereço e a porta atribuídos ao servidor.
O run.py tenta ler a porta das variáveis APP_PORT ou SERVER_PORT.
Se o console pedir para informar a porta, edite run.py pelo gerenciador de arquivos:
troque o número 0 em `PORTA_MANUAL = 0` pela porta de Rede e salve.

## 3. Iniciar e abrir

Clique em Iniciar (Start). Espere a instalação das bibliotecas terminar.
O console deve mostrar `Uvicorn running on http://0.0.0.0:...`.
No navegador, abra `http://ENDERECO:PORTA/`, substituindo pelos dados de Rede.
Compartilhe esse endereço com seus amigos. 0.0.0.0 não é o endereço para compartilhar.

Se houver erro, copie a mensagem do console para identificar o problema.

## Fichas e atualizações

O ZIP não inclui personagens.db: na primeira execução, o site cria um banco vazio
no servidor. Suas fichas locais continuam no computador.

Para transferir fichas locais, pare o site local antes de copiar personagens.db.
Pare também o servidor e baixe uma cópia do banco remoto, se já existir, antes de
enviar o banco local. Essa operação substitui as fichas remotas; não une os bancos.

Para atualizar o código: pare o servidor, faça uma cópia de personagens.db, envie
os arquivos de código alterados e inicie novamente. Preserve personagens.db.
Não envie .venv, __pycache__ ou versoes_anteriores.

Este site não tem login. Todos que acessarem podem ver, alterar e excluir as fichas.

Documentação: https://altare.gg/de/help/apps/deploy-fastapi-app
