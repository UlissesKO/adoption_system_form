# Projeto Formulario de Adoção 

## Descrição
Site/API para cadastro de adotantes em feiras de adoção, reunindo informações pessoais e dados sobre o ambiente do animal.  
Objetivo: melhorar o tempo de atendimento e a gestão dos dados para a ONG.

## Tecnologias
- Python (Flask)
- SQLite (SQL)
- HTML, CSS, JavaScript

## Estrutura
- `src_py/app.py` → back-end Flask
- `database/schema.sql` → modelo do banco
- `templates/` → páginas HTML
- `static/` → CSS, JS, imagens

## Funcionalidades
- CRUD de adotantes
- Cadastro de ambiente
- Listagem e gerenciamento de dados

## Como rodar
```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar servidor
flask run
