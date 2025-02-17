from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate
from models.models import db, Pessoa, Trabalho
from flasgger import Swagger  # type: ignore
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/flask'

db.init_app(app)
migrate = Migrate(app, db)

swagger_config = { ##item não obrigatorio
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
    "specs_route": "/test" ## minha rota pro swagger
}

swagger = Swagger(app, config=swagger_config)

@app.route('/')
def index():
    return render_template("index.html")

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
            - esta_empregado
          properties:
            nome:
              type: string
              description: Nome da pessoa
              example: Nome_Exemplo
            esta_empregado:
              type: boolean
              description: Indica se a pessoa está empregada
              example: true
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
    if 'nome' not in data or 'esta_empregado' not in data:
        return jsonify({'message': 'Os campos "nome" e "esta_empregado" são obrigatórios.'}), 400

    nova_pessoa = Pessoa(nome=data['nome'], esta_empregado=data['esta_empregado'])
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
              esta_empregado:
                type: boolean
    definitions:
      Pessoa:
        type: object
        properties:
          id:
            type: string
          nome:
            type: string
          esta_empregado:
            type: boolean
    """
    pessoas = Pessoa.query.all()
    result = [{'id': str(pessoa.id), 'nome': pessoa.nome, 'esta_empregado': pessoa.esta_empregado} for pessoa in pessoas]
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
            - esta_empregado
          properties:
            nome:
              type: string
              description: Nome da pessoa
              example: Nome_Atualizado
            esta_empregado:
              type: boolean
              description: Indica se a pessoa está empregada
              example: false
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
    pessoa.esta_empregado = data['esta_empregado']
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
            esta_empregado:
              type: boolean
      404:
        description: Pessoa não existe
    """
    pessoa = Pessoa.query.get(id)
    if not pessoa:
        return jsonify({'message': 'Pessoa não existe'}), 404

    return jsonify({
        'id': str(pessoa.id),
        'nome': pessoa.nome,
        'esta_empregado': pessoa.esta_empregado
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
