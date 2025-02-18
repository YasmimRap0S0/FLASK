Desculpe pela confusão! Vou adicionar uma seção explicando sobre o `database.db` e como ele é utilizado no contexto do projeto. Vou incluir o conteúdo relacionado ao uso do **SQLite** para complementar o restante das informações sobre o banco de dados.

Aqui está a versão ajustada, com a explicação sobre o `database.db` incluída:

---

```markdown
# FLASK

O Flask é um microframework de desenvolvimento web criado com a linguagem de programação Python. Sua simplicidade torna uma escolha interessante para criar aplicações web, APIs e protótipos de forma ágil.

## Características gerais:
- Minimalista e modular
- Configuração simples e intuitiva
- Suporte a extensões para adicionar funcionalidades

## SQLAlchemy

Biblioteca de mapeamento objeto-relacional (ORM) para Python, que facilita a interação com bancos de dados relacionais.

## Pré-requisitos
- Python 3.10 ou superior
- PostgreSQL ou SQLite (se estiver usando pgAdmin4 ou para desenvolvimento com banco local)

## Estrutura do Projeto

Antes de começarmos, vamos entender a estrutura do projeto:

```plaintext
├── FLASK/
│   ├── models/
│   │   └── models.py
├── app.py
├── config.py
```

Aqui temos os seguintes arquivos:
- `app.py`: Arquivo principal, onde configuramos as rotas e a lógica do Flask.
- `models/models.py`: Onde ficam os modelos de dados (SQLAlchemy).
- `config.py`: Configurações adicionais, como as opções do Swagger.

---

## 1. Criando a Aplicação Web Básica

### 1.1 Instalando as Dependências

Para começar, instale as dependências básicas do projeto:

```sh
pip install flask
pip install flask_sqlalchemy
pip install SQLAlchemy
pip install flasgger
pip install flask_cors
pip install flask-migrate
pip install psycopg2
```

### 1.2 Arquivo `app.py`

Inicialmente, vamos criar um arquivo `app.py` simples para configurar o Flask e exibir uma mensagem básica:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>APLICAÇÃO WEB</h1>'

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0') ##rodar aplicação
```

### 1.3 Testando a Aplicação

Execute a aplicação com o comando:

```bash
python app.py
```

Acesse `http://localhost:8080/` no seu navegador e verifique se a mensagem "APLICAÇÃO WEB" aparece.

---

## 2. Integrando o Banco de Dados com SQLAlchemy

Agora vamos integrar o banco de dados à aplicação para armazenar as informações.

### 2.1 Instalando o SQLAlchemy

Caso não tenha feito, instale o SQLAlchemy, que é responsável pela integração com o banco de dados:

```bash
pip install flask_sqlalchemy
```

### 2.2 Criando os Modelos de Dados

Crie o arquivo `models/models.py` para definir os modelos do nosso exemplo: `Trabalho` e `Pessoa`.

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo Trabalho
class Trabalho(db.Model):
    __tablename__ = "Trabalho"
    id = db.Column(db.Integer, primary_key=True)
    cargo = db.Column(db.String(100), nullable=True)

    def dicionario(self):
        return {
            'id': self.id,
            'cargo': self.cargo,
        }

# Modelo Pessoa
class Pessoa(db.Model):
    __tablename__ = 'Pessoa'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    trabalho_id = db.Column(db.Integer, db.ForeignKey('Trabalho.id', ondelete='CASCADE'), nullable=True)
    trabalho = db.relationship('Trabalho', backref=db.backref('pessoas_cargos', lazy=True))

    def dicionario(self):
        return {
            'id': str(self.id),
            'nome': self.nome,
            'trabalho_id': str(self.trabalho_id) if self.trabalho_id else None,
            'trabalho': self.trabalho.dicionario() if self.trabalho else None
        }
```

### 2.3 Configuração do Banco de Dados

Adicione as configurações de conexão com o banco de dados no `app.py`:

#### Usando PostgreSQL

```python
from flask import Flask
from models.models import db, Pessoa, Trabalho
from flask_migrate import Migrate


app = Flask(__name__)

# Configuração do banco de dados (PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/flask'
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>APLICAÇÃO WEB COM BANCO DE DADOS</h1>'

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
```

> **Nota**: Substitua `postgres:postgres@localhost:5433/flask` com as configurações do seu ambiente de banco de dados PostgreSQL.

#### Usando SQLite (Arquivo `database.db`)

Se preferir usar **SQLite** para desenvolvimento ou testes, basta alterar a URI do banco de dados para um arquivo local. Com isso, será criado um banco de dados chamado `database.db` no mesmo diretório da aplicação. Veja como fazer:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Banco de dados SQLite
```

- A URI `sqlite:///database.db` indica que o banco de dados será armazenado no arquivo `database.db`.

> **Nota**: O arquivo `database.db` será gerado automaticamente assim que você criar as tabelas no banco de dados com o comando de migração.

### 2.4 Inicializando o Banco de Dados

Para criar as tabelas no banco de dados, execute os seguintes comandos no terminal:

```bash
flask db init
flask db migrate
flask db upgrade
```

- **`db init`**: Inicializa um diretório de migração do banco de dados.
- **`db migrate -m "Descrição das mudanças"`**: Cria uma migração quando você modifica os modelos.
- **`db upgrade`**: Aplica as mudanças no banco de dados, criando as tabelas.

Após esses passos, se estiver utilizando o SQLite, o arquivo `database.db` será gerado no diretório do projeto. Você pode verificar a presença desse arquivo, que conterá as tabelas definidas em seus modelos.

---

## 3. Configurando o Swagger para Documentação da API

Agora, vamos configurar o Swagger para gerar a documentação automática da nossa API.

### 3.1 Adicionando o Swagger ao `app.py`

No arquivo `app.py`, importe e configure o Swagger:

```python
from flask import Flask, request, jsonify
from models.models import db, Pessoa, Trabalho
from flasgger import Swagger  # type: ignore
from flask_migrate import Migrate
from config import swagger_config, swagger_template ## importações no arquivo config.py

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

swagger = Swagger(app, config=swagger_config, template=swagger_template) ## adicione esse trecho

@app.route('/')
def index():
    return '<h1>APLICAÇÃO WEB</h1>'

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')   
```

> **Nota**: O Swagger será configurado com as variáveis `swagger_config` e `swagger_template` definidas no arquivo `config.py` (explicado na próxima seção).

---

## 4. Definindo Configurações do Swagger

### 4.1 Criando o Arquivo `config.py`

O arquivo `config.py` contém configurações essenciais tanto para o funcionamento do Swagger quanto para a definição dos modelos e rotas da API. Ele ajuda a personalizar a documentação gerada automaticamente para a sua API.

```python
swagger_config = { ## O swagger_config é opcional, e pode ser retirado
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/teste/teste/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/test" ## rota para documentação do swagger
}

swagger_template = { ##necessário caso tenha mais de uma classe de modelo
    "swagger": "2.0",
    "info": {
        "title": "API de Pessoa e Trabalho",
        "description": "Documentação da API de exemplo",
        "version": "1.0"
    },
    "host": "localhost:8080",
    "basePath": "/",
    "schemes": [
        "http"
    ],
}
```

---
Pronto! O Swagger está configurado, mas ainda exibirá o erro "No operations defined in spec!" porque as rotas ainda não foram definidas. Antes de prosseguir com a definição das rotas, é necessário importar e configurar o CORS.

## 5. Requisitos para adicionar as Rotas da API

### 5.2 Instalando o CORS
Caso não tenha feito, instale o flask-CORS, o qual permitirá configurar e gerenciar o CORS no seu aplicativo Flask

```bash
pip install flask-cors
```

Não se esqueça de inserir no arquivo app.py. O inicio ficara assim:

```python
from flask import Flask, request, jsonify
from models.models import db, Pessoa, Trabalho
from flasgger import Swagger  # type: ignore
from flask_migrate import Migrate
from flask_cors import CORS

from config import swagger_config, swagger_template ## importações no arquivo config.py

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas
```

- A extensão `flask_cors` facilita a configuração do CORS no Flask, permitindo que você defina quais origens (domínios) podem fazer requisições à sua API. Isso é importante em APIs públicas ou quando o front-end e o back-end estão hospedados em domínios diferentes. Em outras palavras: permite ou restringe o acesso a recursos do servidor como APIs, fontes, imagens e outros dados.

### 5.2 Criando as Rotas para `Pessoa` e `Trabalho`

Agora, vamos adicionar as rotas CRUD para `Pessoa` e `Trabalho`, já com a documentação do Swagger. Adicione as rotas no seu `app.py`:

```python
# Rota para criar um trabalho
# Rotas CRUD para Pessoa

@app.route('/pessoas', methods=['POST'])
def create_pessoa():
    """
    Cria uma nova pessoa
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              description: Nome da pessoa
              example: Nome_Exemplo
            trabalho_id:
              type: integer
              description: ID do trabalho
              example: 1
    responses:
      201:
        description: Pessoa criada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Requisição inválida
    """
    data = request.get_json()
    if 'nome' not in data:
        return jsonify({'message': 'O campo "nome" é obrigatório.'}), 400

    nova_pessoa = Pessoa(
        nome=data['nome'],
        trabalho_id=data.get('trabalho_id')  # Usa get para permitir que trabalho_id seja opcional
    )
    db.session.add(nova_pessoa) 
    db.session.commit()
    return jsonify({'message': 'Pessoa criada com sucesso!'}), 201

@app.route('/pessoas', methods=['GET'])
def get_pessoas():
    """
    Retorna nossos amigos
    ---
    responses:
      200:
        description: Lista de pessoas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              nome:
                type: string
              trabalho:
                type: object
                properties:
                  cargo:
                    type: string
    definitions:
      Pessoa:
        type: object
        properties:
          id:
            type: string
          nome:
            type: string
          trabalho:
            type: object
            properties:
              cargo:
                type: string
    """
    pessoas = Pessoa.query.all()
    result = [{
        'id': str(pessoa.id),
        'nome': pessoa.nome,
        'trabalho': {
            'cargo': pessoa.trabalho.cargo
        } if pessoa.trabalho else None
    } for pessoa in pessoas]
    return jsonify(result), 200

@app.route('/pessoas/<int:id>', methods=['PUT'])
def update_pessoa(id):
    """
    Atualiza uma pessoa existente
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID da pessoa
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              description: Nome da pessoa
              example: nome_Atualizado
            trabalho_id:
              type: integer
              description: ID do trabalho
              example: 1
    responses:
      200:
        description: Pessoa atualizada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Pessoa não encontrada
    """
    data = request.get_json()
    pessoa = Pessoa.query.get(id)
    if not pessoa:
        return jsonify({'message': 'Pessoa não encontrada'}), 404

    pessoa.nome = data['nome']
    pessoa.trabalho_id = data.get('trabalho_id') 
    db.session.commit()
    return jsonify({'message': 'Pessoa atualizada com sucesso'}), 200

@app.route('/pessoas/<int:id>', methods=['DELETE'])
def delete_pessoa(id):
    """
    Deleta uma pessoa existente
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID da pessoa
    responses:
      200:
        description: Pessoa deletada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Pessoa não encontrada
    """
    pessoa = Pessoa.query.get(id)
    if not pessoa:
        return jsonify({'message': 'Pessoa não encontrada'}), 404

    db.session.delete(pessoa)
    db.session.commit()
    return jsonify({'message': 'Pessoa deletada com sucesso'}), 200

@app.route('/pessoas/<int:id>', methods=['GET'])
def get_pessoa(id):
    """
    Retorna uma pessoa específica
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID da pessoa
    responses:
      200:
        description: Pessoa encontrada
        schema:
          type: object
          properties:
            id:
              type: string
            nome:
              type: string
            trabalho:
              type: object
              properties:
                id:
                  type: string
                cargo:
                  type: string
      404:
        description: Pessoa não existe
    """
    pessoa = Pessoa.query.get(id)
    if not pessoa:
        return jsonify({'message': 'Pessoa não existe'}), 404

    return jsonify({
        'id': str(pessoa.id),
        'nome': pessoa.nome,
        'trabalho': {
            'id': str(pessoa.trabalho.id),
            'cargo': pessoa.trabalho.cargo
        } if pessoa.trabalho else None
    }), 200

# Rotas para Trabalho

@app.route('/trabalhos', methods=['POST'])
def create_trabalho():
    """
    Cria um novo trabalho
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - cargo
          properties:
            cargo:
              type: string
              description: Cargo da pessoa
              example: Engenheiro
    responses:
      201:
        description: Trabalho criado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Requisição inválida
    """
    data = request.get_json()
    if 'cargo' not in data:
        return jsonify({'message': 'O campo "cargo" é obrigatório.'}), 400

    novo_trabalho = Trabalho(cargo=data['cargo'])
    db.session.add(novo_trabalho)
    db.session.commit()
    return jsonify({'message': 'Trabalho criado com sucesso!'}), 201


    @app.route('/trabalhos', methods=['GET'])
def get_trabalhos():
    """
    Retorna todos os trabalhos
    ---
    responses:
      200:
        description: Lista de trabalhos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              cargo:
                type: string
    """
    trabalhos = Trabalho.query.all()
    result = [{
        'id': str(trabalho.id),
        'cargo': trabalho.cargo
    } for trabalho in trabalhos]
    return jsonify(result), 200

# Rotas CRUD para Pessoa
@app.route('/pessoas', methods=['POST'])
def create_pessoa():
    """
    Cria uma nova pessoa
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              description: Nome da pessoa
              example: Nome_Exemplo
            trabalho_id:
              type: integer
              description: ID do trabalho
              example: 1
    responses:
      201:
        description: Pessoa criada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Requisição inválida
    """
    data = request.get_json()
    if 'nome' not in data:
        return jsonify({'message': 'O campo "nome" é obrigatório.'}), 400

    nova_pessoa = Pessoa(
        nome=data['nome'],
        trabalho_id=data.get('trabalho_id')  # Usa get para permitir que trabalho_id seja opcional
    )
    db.session.add(nova_pessoa) 
    db.session.commit()
    return jsonify({'message': 'Pessoa criada com sucesso!'}), 201
```

---

## 6. Finalizando e Rodando a Aplicação

### 6.1 Executando a Aplicação

Para rodar a aplicação, execute o seguinte comando:

```bash
python app.py
```

Caso não tenha alterado a rota do swagger, verifique  a documentação do Swagger em `http://localhost:8080/apidocs/` para testar as rotas e ver a documentação gerada automaticamente.

---

