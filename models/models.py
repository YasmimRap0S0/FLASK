from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo Pessoa 
class Pessoa(db.Model):
    __tablename__ = 'Pessoa'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    esta_empregado = db.Column(db.Boolean, default=False) 

    def dicionario(self):
        return {
            'id': str(self.id),
            'nome': self.nome,
            'esta_empregado': self.esta_empregado
        }

# Modelo Trabalho
class Trabalho(db.Model):
    __tablename__ = "Cargos"
    id = db.Column(db.Integer, primary_key=True)
    cargo = db.Column(db.String(100), nullable=False)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('Pessoa.id'), nullable=False)
    pessoa = db.relationship('Pessoa', backref=db.backref('trabalhos', lazy=True))

    def dicionario(self):
        return {
            'id': self.id,
            'cargo': self.cargo,
            'pessoa_id': str(self.pessoa_id),
            'pessoa': self.pessoa.dicionario()  # Inclui os detalhes da pessoa
        }
