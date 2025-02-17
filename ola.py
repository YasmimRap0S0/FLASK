from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger # type: ignore

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
swagger = Swagger(app)
db = SQLAlchemy(app)

# Modelo Pessoa 
class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class Trabalho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cargo = db.Column(db.String(100), nullable = False)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)
    pessoa = db.relationship('Pessoa', backref=db.backref('trabalhos', lazy=True))


with app.app_context():
   ##  db.drop_all()  para excluir tabelas
    db.create_all()  

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
          id: Pessoa
          required:
            - nome
          properties:
            nome:
              type: string
              description: Nome da pessoa
              example: João
    responses:
      201:
        description: Pessoa criada com sucesso
        schema:
          id: Pessoa
          properties:
            message:
              type: string
    """
    data = request.get_json()
    nova_pessoa = Pessoa(nome=data['nome'])
    db.session.add(nova_pessoa)
    db.session.commit()
    return jsonify({'message': 'Pessoa criada com sucesso!'}), 201

@app.route('/pessoas', methods=['GET'])
def get_pessoas():
    """
    Retorna todas as pessoas
    ---
    responses:
      200:
        description: Lista de pessoas
        schema:
          type: array
          items:
            $ref: '#/definitions/Pessoa'
    definitions:
      Pessoa:
        type: object
        properties:
          id:
            type: integer
          nome:
            type: string
    """
    pessoas = Pessoa.query.all()
    result = [{'id': pessoa.id, 'nome': pessoa.nome} for pessoa in pessoas]
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)
