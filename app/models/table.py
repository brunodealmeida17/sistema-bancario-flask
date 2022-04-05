from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def get_user(usuario_id):
    return User.query.filter_by(id=usuario_id).first()


class User(db.Model, UserMixin):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String())
    cpf = db.Column(db.String(11), unique=True)
    rg = db.Column(db.String(20), unique=True)
    conta = db.Column(db.String(20), unique=True)
    agencia = db.Column(db.String(20))
    saldo = db.Column(db.Float())
    email = db.Column(db.String(120), unique=True)
    senha = db.Column(db.String)

    def __init__(self, nome, cpf, rg, conta, agencia, saldo, email, senha):
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        self.conta = conta
        self.agencia = agencia
        self.saldo = saldo        
        self.email = email
        self.senha = generate_password_hash(senha)
        
    def verify_password(self, senha):
        return check_password_hash(self.senha, senha)
    
    def __repr__(self):
        return '<User %r>' % self.cpf           


class Transacao(db.Model):
    __tablename__ = 'transacao'
    id = db.Column(db.Integer, primary_key=True)
    tipo_transacao = db.Column(db.String(20))
    conta_origem = db.Column(db.String())
    cpf_origem = db.Column(db.String())
    valor = db.Column(db.Float())       
    conta_destino = db.Column(db.String())
    cpf_destino = db.Column(db.String())
    id_transacao = db.Column(db.String(), unique=True) 
    data_hora = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
      
    def get_id(self):
        return str(self.id)
    
    
    def __init__(self, tipo_transacao, valor, id_transacao, data_hora, conta_origem, cpf_origem, conta_destino = None, cpf_destino = None):
        self.tipo_transacao = tipo_transacao
        self.valor = valor
        self.id_transacao = id_transacao
        self.conta_origem = conta_origem
        self.cpf_origem = cpf_origem
        self.data_hora = data_hora
        self.conta_destino = conta_destino
        self.cpf_destino = cpf_destino

    
