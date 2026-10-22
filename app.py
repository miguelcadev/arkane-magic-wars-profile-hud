from pathlib import Path
import sqlite3

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Estes caminhos funcionam mesmo se o terminal estiver em outra pasta.
PASTA = Path(__file__).resolve().parent
BANCO = PASTA / "personagens.db"
app = FastAPI()
app.mount("/static", StaticFiles(directory=PASTA / "static"), name="static")
templates = Jinja2Templates(directory=PASTA / "templates")


# Abre o banco, executa um comando SQL e fecha a conexão.
def executar_sql(comando, valores=()):
    banco = sqlite3.connect(BANCO)
    banco.row_factory = sqlite3.Row
    try:
        resultado = banco.execute(comando, valores).fetchall()
        banco.commit()
        return resultado
    finally:
        banco.close()


# IF NOT EXISTS mantém as fichas que já estão salvas.
executar_sql("""
    CREATE TABLE IF NOT EXISTS personagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        vida_atual INTEGER NOT NULL DEFAULT 0,
        vida_maxima INTEGER NOT NULL DEFAULT 0,
        recurso_atual INTEGER NOT NULL DEFAULT 0,
        recurso_maximo INTEGER NOT NULL DEFAULT 0,
        movimento INTEGER NOT NULL DEFAULT 0,
        regeneracao INTEGER NOT NULL DEFAULT 0,
        resistencia INTEGER NOT NULL DEFAULT 0
    )
""")


# GET mostra a única página. Exemplo: /?editar=1 abre a ficha 1 no formulário.
@app.get("/")
def inicio(request: Request, editar: int = 0, aviso: str = ""):
    personagens = executar_sql("SELECT * FROM personagens ORDER BY id DESC")
    ficha = {}
    for personagem in personagens:
        if personagem["id"] == editar:
            ficha = dict(personagem)

    mensagens = {"salvo": "Ficha salva!", "excluido": "Ficha excluída."}
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"personagens": personagens, "ficha": ficha,
                 "mensagem": mensagens.get(aviso, "")},
    )


# Form recebe os inputs do HTML. ge=0 impede números negativos.
@app.post("/salvar")
def salvar(
    nome: str = Form(min_length=1, max_length=100, pattern=r".*\S.*"),
    vida_atual: int = Form(ge=0, le=999999),
    vida_maxima: int = Form(ge=0, le=999999),
    recurso_atual: int = Form(ge=0, le=999999),
    recurso_maximo: int = Form(ge=0, le=999999),
    movimento: int = Form(ge=0, le=999999),
    regeneracao: int = Form(ge=0, le=999999),
    resistencia: int = Form(ge=0, le=999999),
    id: int = Form(0, ge=0),
):
    valores = (nome.strip(), vida_atual, vida_maxima, recurso_atual,
               recurso_maximo, movimento, regeneracao, resistencia)

    # Os ? recebem os valores separados do comando SQL.
    if id == 0:
        executar_sql("""
            INSERT INTO personagens (nome, vida_atual, vida_maxima, recurso_atual,
                recurso_maximo, movimento, regeneracao, resistencia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, valores)
    else:
        executar_sql("""
            UPDATE personagens SET nome=?, vida_atual=?, vida_maxima=?,
                recurso_atual=?, recurso_maximo=?, movimento=?, regeneracao=?,
                resistencia=? WHERE id=?
        """, valores + (id,))

    # Volta à página depois de salvar, evitando repetir o POST ao atualizar.
    return RedirectResponse("/?aviso=salvo", status_code=303)


@app.post("/excluir/{id}")
def excluir(id: int):
    executar_sql("DELETE FROM personagens WHERE id=?", (id,))
    return RedirectResponse("/?aviso=excluido", status_code=303)
