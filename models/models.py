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
    trabalho = db.relationship('Trabalho', backref=db.backref('pessoas_cargos', lazy=True))  ##definir um relacionamento bidirecional entre duas tabelas
    
    def dicionario(self):
        return {
            'id': str(self.id),
            'nome': self.nome,
            'trabalho_id': str(self.trabalho_id) if self.trabalho_id else None,
            'trabalho': self.trabalho.dicionario() if self.trabalho else None
        }
