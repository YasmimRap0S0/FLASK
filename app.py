
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models.models import db, Pessoa, Trabalhp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

## @app.route('/')
## def index():
   ##  return render_template("index.html")

# Rotas CRUD para Pessoa
@app.route('/pessoas', methods=['POST'])
def create_pessoa():
    data = request.get_json()
    nova_pessoa = Pessoa(nome=data['nome'])
    db.session.add(nova_pessoa)
    db.session.commit()
    return jsonify({'message': 'Pessoa criada com sucesso!'}), 201

@app.route('/pessoas', methods=['GET'])
def get_pessoas():
    pessoas = Pessoa.query.all()
    result = [{'id': pessoa.id, 'nome': pessoa.nome} for pessoa in pessoas]
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
