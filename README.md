# Grimório de personagens

Uma página roxa e vermelha para criar, editar e excluir fichas.

## Como abrir

No terminal do VS Code, dentro desta pasta:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app:app --reload --port 8765
```

Abra http://127.0.0.1:8765 no navegador. Para parar, pressione Ctrl+C.
O HTML precisa ser aberto por esse endereço para receber os dados do Python.

Se estiver preparando o projeto em outro computador, execute antes:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Os três arquivos para estudar

- `app.py`: recebe pedidos do navegador e consulta o SQLite.
- `templates/index.html`: a única página, com o formulário e as fichas salvas.
- `static/style.css`: cores, tamanhos e organização visual.

`personagens.db` guarda as fichas mesmo depois que o servidor é fechado.
`requirements.txt` lista as bibliotecas. `.venv` contém essas bibliotecas.
`versoes_anteriores` guarda uma cópia dos arquivos antigos e não participa do site.

## O caminho de uma ficha

1. Ao abrir `/`, o Python lê o banco e preenche o HTML.
2. Ao clicar em Salvar, o formulário envia seus campos para `/salvar`.
3. O Python recebe cada campo com `Form`. `int` indica número inteiro; `ge=0` impede negativos.
4. Se o `id` for zero, `INSERT` cria uma ficha. Se já existir um `id`, `UPDATE` altera a ficha.
5. O navegador volta para a mesma página e mostra a lista atualizada.
6. Editar abre `/?editar=ID` e preenche o mesmo formulário. Excluir usa `DELETE`.

No HTML, `{{ ... }}` mostra um valor vindo do Python e `{% for ... %}` repete um bloco.
No SQL, os `?` recebem os valores do formulário separados do comando.

O nome é o nome do personagem; este projeto não possui contas ou login.
Os números vão de 0 a 999999. Para mudar esse limite, altere `le` no Python e `max` no HTML.

Referências: [formulários no FastAPI](https://fastapi.tiangolo.com/tutorial/request-forms/)
e [templates no FastAPI](https://fastapi.tiangolo.com/advanced/templates/).

