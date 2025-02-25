from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo Trabalho
class Trabalho(db.Model):
    __tablename__ = "Trabalho"  
    id = db.Column(db.Integer, primary_key=True)
    cargo = db.Column(db.String(100), nullable=True)
    
# Modelo Pessoa 
class Pessoa(db.Model):
    __tablename__ = 'Pessoa'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    trabalho_id = db.Column(db.Integer, db.ForeignKey('Trabalho.id', ondelete='CASCADE'), nullable=True)
    trabalho = db.relationship('Trabalho', backref=db.backref('pessoas_cargos', lazy=True))  ##definir um relacionamento bidirecional entre duas tabelas
    

