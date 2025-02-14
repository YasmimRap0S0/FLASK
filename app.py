from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo Pessoa
class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)

# Modelo Endereco
class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(150), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)
    
    pessoa = db.relationship('Pessoa', backref=db.backref('enderecos', lazy=True))

# Modelo Trabalho
class Trabalho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cargo = db.Column(db.String(100), nullable=False)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/index')
def index():
    return render_template("index.html")




if __name__ == "__main__":
    app.run(debug=True)
