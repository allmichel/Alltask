from flask import Flask, render_template, request, redirect, abort, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db' # usando SQLite como banco de dados
db = SQLAlchemy(app)


class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_tarefa = db.Column(db.String(100), nullable=False)
    prazo = db.Column(db.DateTime, nullable=True)
    concluida = db.Column(db.Boolean, default=False)

    def __init__(self, nome_tarefa, prazo, concluida):
        self.nome_tarefa = nome_tarefa
        self.prazo = prazo
        self.concluida = concluida


@app.route('/')
def index():
    tarefas = Tarefa.query.all()
    return render_template('index.html', tarefas=tarefas)

@app.route('/criar', methods=['GET','POST'])
def criar():
    if request.method == 'POST':
        nome_tarefa = request.form['nome_tarefa']
        prazo_str = request.form['prazo']
        prazo = datetime.strptime(prazo_str, '%Y-%m-%dT%H:%M') if prazo_str else None
        concluida = bool(int(request.form.get('concluida', 0)))
        tarefa = Tarefa(nome_tarefa=nome_tarefa, prazo=prazo, concluida=concluida)
        db.session.add(tarefa)
        db.session.commit()
        return redirect('/')
    return render_template('/')

@app.route('/editar/<int:tarefa_id>', methods=['GET', 'POST'])
def editar(tarefa_id):
    tarefa = Tarefa.query.get(tarefa_id)
    if request.method == 'POST':
        tarefa.nome_tarefa = request.form['nome_tarefa']
        tarefa.prazo = datetime.strptime(request.form['prazo'], '%Y-%m-%dT%H:%M')
        tarefa.concluida = bool(request.form.get('concluida'))
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('/editar.html', tarefa=tarefa)

@app.route('/remover/<int:tarefa_id>', methods=['GET', 'POST'])
def remover(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect('/')



if __name__ == '__main__':
    with app.app_context():
        db.create_all() # cria as tabelas do banco de dados
    app.run(debug=True)