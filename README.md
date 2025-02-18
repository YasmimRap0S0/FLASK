# FLASK

O Flask é um microframework de desenvolvimento web criado com a linguagem de programação Python. Sua simplicidade torna uma escolha interessante para criar aplicações web, APIs e protótipos de forma ágil.

## Características gerais:
- Minimalista e modular
- Configuração simples e intuitiva
- Suporte a extensões para adicionar funcionalidades

## SQLAlchemy

Biblioteca de mapeamento objeto-relacional (ORM) para Python, que facilita a interação com bancos de dados relacionais.

## Pré-requisito
- Python 3.10 ou superior

## Pré-requisito OPCIONAL
- pgAdmin4

### Iniciando Projeto

1. Crie uma pasta com um arquivo `.py`. Você pode dividir alguns trechos do código em pastas/arquivos ou colocá-los em um único arquivo

Exemplo da estrutura do nosso projeto:

├── FLASK/
│   ├── models/
│   │   └── models.py
├── app.py
├── config.py

2. Instale as seguintes dependências em sua pasta de trabalho:

```sh
pip install flask
pip install flask_sqlalchemy
pip install SQLAlchemy
pip install flasgger
pip install flask_cors
pip install flask-migrate
pip install psycopg2
```

3. Realize os imports no seu arquivo app.py

```python
from flask import Flask, request, jsonify
from models.models import db, Pessoa, Trabalho
from flasgger import Swagger  # type: ignore
from flask_migrate import Migrate
from flask_cors import CORS
```

Explicação dos imports:
- **Flask**: Utilizamos o Flask para criar a aplicação. O `request` lida com as requisições HTTP, `jsonify` facilita a criação de respostas JSON e `render_template` renderiza templates HTML.
- **SQLAlchemy**: ORM que facilita a interação com o banco de dados.
- **Flasgger**: Permite documentar e explorar APIs com uma interface baseada no Swagger UI.

4. Crie uma instância para a aplicação e habilite o CORS:

```python
app = Flask(__name__)
CORS(app)
```

> **Nota**: Substitua `usuario`, `senha`, `localhost`, `5433` e `nome_do_banco` pelos valores adequados do seu ambiente.

5. Adicione a URI de conexão do seu banco de dados.

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:senha@localhost:5433/nome_do_banco'
```

> **Nota**: Substitua `usuario`, `senha`, `localhost`, `5433` e `nome_do_banco` pelos valores adequados do seu ambiente.

---

Esse guia fornece as informações básicas para iniciar um projeto Flask utilizando SQLAlchemy. Para continuar, você pode configurar modelos, criar rotas e implementar migrações com `Flask-Migrate`.

