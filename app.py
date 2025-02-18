from flask import Flask, request, jsonify
from models.models import db, Pessoa, Trabalho
from flask_migrate import Migrate
from flasgger import Swagger  # type: ignore
from config import swagger_config, swagger_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

swagger = Swagger(app, config=swagger_config, template=swagger_template)

@app.route('/')
def index():
    return ('<h1>APLICAÇÃO WEB</h1>')

# Rota para criar um trabalho
@app.route('/api/trabalhos', methods=['POST'])
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

# Rota para obter todos os trabalhos
@app.route('/api/trabalhos', methods=['GET'])
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

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')