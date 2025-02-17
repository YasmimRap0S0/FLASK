# FLASK

O Flask é um microframework de desenvolvimento web criado com a linguagem de programação Python. Sua simplicidade e flexibilidade o tornam uma escolha ideal para desenvolvedores que buscam criar aplicações web, APIs e protótipos de forma ágil.

Características gerais:
- minimalista e modular 
- Configuração simples e intuitiva 
- Suporte a extensões para adicionar funcionalidades 

## SQLAchemy
biblioteca de mapeamento objeto-relacional (ORM) para Python, que facilita a interação com bancos de dados relacionais

## Pré-requisito
- Python 3.10 ou superior

### Iniciando Projeto
 

1. Crie uma pasta com um arquivo .py
2. Instalar as seguintes dependências em sua pasta de trabalho:

```python
pip install flask
pip install flask_sqlalchemy
pip install SQLAlchemy
pip install flasgger
pip install flask_cors
pip install flask-Migrate
pip install psycopg2

```

3. Realize os importes no seu arquivo .py

```txt

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger # type: ignore


```

- Flask: Utilizamos o Flask para criar a aplicação, request lida com as requisições HTTP, jsonify facilita a criação de respostas JSON, e render_template renderiza templates HTML.<br>
- SQLAlchemy: Importa o SQLAlchemy, que é um ORM (Object-Relational Mapping) que facilita a interação com o banco de dados.<br>
- Flasgger: Permite que você documente e explore APIs com uma interface baseada no Swagger UI.<br>

4. Crie uma instância para a aplicação o CORS na sua aplicação

```txt

app = Flask(__name__)
CORS(app)

```

5. Adicione a URI de conexão do seu banco de dados.
postgresql://<username>:<password>@<hostname>:<port>/<database_name>

6. 





