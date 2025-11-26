# Reserva Certa — Instruções de desenvolvimento

Resumo rápido
- Projeto Flask simples para gerenciar espaços e reservas.
- Para desenvolvimento use o servidor de desenvolvimento do Flask (já com live-reload ativado por `debug=True`).

Pré-requisitos
- Python 3.8+ instalado e disponível no PATH.
- (opcional) VS Code com extensão Python para debugging.

Instalar dependências
Abra PowerShell na raiz do projeto (onde está `app.py`) e rode:

```powershell
cd "c:\Users\iagof\OneDrive\Documentos\PUC\semestre_5\Engenharia2\reserva_certa_flask_app"
python -m pip install -r .\requirements.txt
```

Rodando a aplicação (dev + live-reload)
- Método simples (recomendado):

```powershell
python app.py
```

O `app.py` já chama `app.run(debug=True)`, então o Flask ativará o reloader e recarregará automaticamente quando você salvar alterações em arquivos Python ou templates.

- Alternativa (usar `flask run`):

```powershell
$env:FLASK_APP = 'app'
$env:FLASK_DEBUG = '1'
flask run --reload
```

Acessar no navegador
- Host local: http://127.0.0.1:5000/

Rotas úteis
- / — página inicial (lista espaços + minhas reservas)
- /reservar/<space_id> — página de reserva
- /spaces — consultar espaços
- /spaces/new — cadastrar novo espaço
- /users — listar usuários
- /admin/reservations — listar todas as reservas (admin)
- /agenda — agenda do dia
- /reports — relatórios simples
- /login — login por user_id (session)
- /logout — logout

Login (usuário)
- Para fins de desenvolvimento a autenticação é simples: vá em `/login` e informe um `user_id` existente (ex: `u1`). O `session['user_id']` será usado nas ações.

Live-reload e VS Code
- O servidor em `debug=True` já fornece reload automático. Basta salvar arquivos para ver as mudanças.
- Eu adicionei arquivos de configuração do VS Code em `.vscode/`:
  - `tasks.json` — tarefa "Run Flask (python app.py)" (Run Task / Ctrl+Shift+B)
  - `launch.json` — configuração de depuração (F5)

Observação sobre a extensão "Live Server"
- A extensão Live Server serve arquivos estáticos (HTML/CSS/JS) sem executar o backend. Como este projeto usa Flask + templates Jinja + DB, você deve rodar o servidor Flask (não use Live Server como substituto para o backend).

Protegendo rotas administrativas
- Há um helper `_require_admin()` e funções de sessão em `app.py`. No momento as rotas administrativas mostram flash mas não aplicam um decorator global. Se quiser, eu posso aplicar um decorator `@admin_required` e obrigar o login de administradores para acessar `/admin/*`.

Depuração e problemas comuns
- Se receber `ModuleNotFoundError: No module named 'flask'`, execute `python -m pip install -r requirements.txt`.
- Se alterações em templates não aparecem, limpe cache do navegador (Ctrl+F5) e verifique se o servidor está rodando em modo `debug` (procure `Debugger is active` no terminal onde iniciou a app).
- Se a porta 5000 estiver ocupada, rode `flask run --port 5001 --reload` ou ajuste `app.run(host='0.0.0.0', port=5001, debug=True)` temporariamente.

Parar o servidor
- No terminal onde o servidor rodou: Ctrl+C

Próximos passos recomendados
- Proteger rotas administrativas com autenticação/roles.
- Refatorar templates (já foi criado `base.html`) e melhorar validações (formularios).
- Implementar export de relatórios (CSV/PDF) e filtros por data.

Se quiser, eu posso:
- adicionar o decorator `@admin_required` e aplicá-lo nas rotas administrativas;
- atualizar `launch.json` para usar `debugpy` (nova recomendação do VS Code);
- gerar um README mais detalhado com exemplos de queries e testes automatizados.

---
Gerado automaticamente pelo assistente — se quiser que eu execute alguma das opções acima, diga qual.
Reserva Certa - Aplicação Flask (Protótipo)

Como executar:
1. Instale dependências:
   pip install -r requirements.txt
2. Na raiz do projeto, rode:
   python app.py
3. Abra no navegador: http://127.0.0.1:5000/

Estrutura principal:
- app.py -> aplicação Flask com rotas e integração com repositórios
- persistence/ -> connection factory e repositórios (SQLite)
- templates/ -> Jinja2 templates (index.html, reserve.html)
- sql/ -> scripts create_tables.sql e insert_data.sql (executados na primeira execução)
