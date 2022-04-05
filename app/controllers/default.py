from app import app, db
from flask import render_template, flash, redirect, url_for, request
from hashlib import md5
import random
from datetime import datetime
from flask_login import login_user, logout_user, current_user



from app.models.table import User
from app.models.table import Transacao


date = datetime.now()
date_f = date.strftime('%d-%m-%Y %H:%M:%S')
inicio = 'baaTzas'
meio = 'Tba'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.verify_password(senha):
            return render_template('index.html')
        
        
          
        login_user(user)
        return render_template('home.html')       
        
    
    return render_template('index.html')
    
    
@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return render_template('index.html')

@app.route("/home")
def home():
    
    nome = User.query.filter_by(cpf='11111111121').first()    
        
    return render_template('home.html', nome=nome)




@app.route("/extrato")
def extrato():    
    return render_template('extrato.html')


@app.route("/transferencia", methods=["GET", "POST"])
def transferir():
    final = random.randint(10000, 99999)
    numeros = random.randint(100000000000, 999999999999)
    id_trans = inicio + str(numeros) + meio + str(final)   
   
    
    conta = current_user.conta
    cpf = current_user.cpf
    
    if request.method == "POST":
        conta_destino = request.form['conta_destino']
        cpf_destino = request.form['cpf_destino']
        valor_dep = request.form['valor_dep']
        valor = float(valor_dep)        
        saldo = current_user.saldo
        
        if (saldo - valor) < 0:
            print('saldo insuficiente!')
            return render_template('sacar.html')
        else:
            saldo_ret = (saldo - valor)
                        
            r = User.query.filter_by(cpf=cpf).first()
            
            r.saldo = saldo_ret
            db.session.add(r)
            
            s = User.query.filter_by(conta=conta_destino).first()
            saldo_atualizar = s.saldo
            
            saldo_novo = saldo_atualizar + valor
            
            s.saldo = saldo_novo
            
            db.session.add(s)
            
            t = Transacao("Transferencia", valor, id_trans, date_f, conta, cpf, conta_destino, cpf_destino)
            db.session.add(t)
            db.session.commit()     
         
    return render_template('transferir.html')

@app.route("/saque", methods=["GET", "POST"])
def saque():    
    
    final = random.randint(10000, 99999)
    numeros = random.randint(100000000000, 999999999999)
    id_trans = inicio + str(numeros) + meio + str(final)
    
   
        
    conta = current_user.conta
    cpf = current_user.cpf
        
    if request.method == "POST":
        valor_form = request.form['valor_saque']
        valor = float(valor_form)        
        saldo = current_user.saldo
        
        if (saldo - valor) < 0:
            print('saldo insuficiente!')
            return render_template('sacar.html')
        else:
            saldo_atual = (saldo - valor)
            
            r = User.query.filter_by(cpf=cpf).first()
            
            r.saldo = saldo_atual
            db.session.add(r)
            t = Transacao("saque", valor, id_trans, date_f, conta, cpf)
            db.session.add(t)
            db.session.commit()         
        
    return render_template('sacar.html')


@app.route("/deposito", methods=["GET", "POST"])
def deposito():      
    final = random.randint(10000, 99999)
    numeros = random.randint(100000000000, 999999999999)
    id_trans = inicio + str(numeros) + meio + str(final)   
    
    
    cpf = current_user.cpf
    conta = current_user.conta    
    
    if request.method == "POST":
        valor_form = request.form['valor_deposito']
        valor = float(valor_form)
        saldo = current_user.saldo
        
        saldo_atual = (saldo + valor)
        r = User.query.filter_by(conta=conta).first()
        r.saldo = saldo_atual
        
        db.session.add(r)
        t = Transacao("deposito", valor, id_trans, date_f, conta, cpf)
        db.session.add(t)
        db.session.commit()    
          
    return render_template('depositar.html')


@app.route("/menu")
def menu():    
    return render_template('menu.html')


@app.route("/test/<info>")
@app.route("/teste", defaults={"info": None})
def teste(info):
    
    nome = "teste de aplicação"
    cpf = "20252525233"
    rg = "222231"
    saldo = 10000
    email = "teste@teste.com"
    senha = "teste@123"
    conta = random.randint(100000, 999999)
    agencia = "0001"

    i = User(nome, cpf, rg, conta, agencia, saldo, email, senha )
    db.session.add(i)
    db.session.commit() 
    
    return "ok"
    
    
    

    
    
    
    
    
    
       