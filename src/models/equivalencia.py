from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Equivalencia(db.Model):
    __tablename__ = 'equivalencias'
    
    id = db.Column(db.Integer, primary_key=True)
    disciplina_adm = db.Column(db.String(255), nullable=False)
    codigo_adm = db.Column(db.String(50), nullable=False)
    ch_adm = db.Column(db.String(10), nullable=False)
    disciplina_equiv = db.Column(db.String(255), nullable=False)
    codigo_equiv = db.Column(db.String(50), nullable=False)
    curso_equiv = db.Column(db.String(255), nullable=False)
    ch_equiv = db.Column(db.String(10), nullable=False)
    justificativa = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Equivalencia {self.disciplina_adm} -> {self.disciplina_equiv}>'

    def to_dict(self):
        return {
            'id': self.id,
            'disciplina_adm': self.disciplina_adm,
            'codigo_adm': self.codigo_adm,
            'ch_adm': self.ch_adm,
            'disciplina_equiv': self.disciplina_equiv,
            'codigo_equiv': self.codigo_equiv,
            'curso_equiv': self.curso_equiv,
            'ch_equiv': self.ch_equiv,
            'justificativa': self.justificativa,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Admin {self.username}>'

