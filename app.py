from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)

app = Flask(__name__)

environment = os.environ.get('FLASK_ENV', default='development')

if environment == 'development':
    POSTGRES_HOST = 'localhost'
    POSTGRES_DB = 'suyash'
    POSTGRES_USER = 'postgres'
    POSTGRES_PASSWORD = 'Suyash12345'
    POSTGRES_PORT = 5432
    DEBUG = True

else:
    POSTGRES_HOST = os.environ['POSTGRES_HOST_PROD']
    POSTGRES_DB = os.environ['POSTGRES_DB_PROD']
    POSTGRES_USER = os.environ['POSTGRES_USER_PROD']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD_PROD']
    POSTGRES_PORT = int(os.environ.get('POSTGRES_PORT_PROD'))
    DEBUG = False
    
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(200), nullable=False)
    emp_id = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"
    
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        name = request.form['name']
        emp_id = request.form['emp_id']
        
        max_sno = db.session.query(db.func.max(Todo.sno)).scalar()
        next_sno = (max_sno or 0) + 1

        todo = Todo(sno=next_sno, name=name, emp_id=emp_id)
        db.session.add(todo)
        db.session.commit()
            
    
    allTodo = Todo.query.order_by(Todo.sno).all()
    return render_template('index.html', allTodo=allTodo)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        name = request.form['name']
        emp_id = request.form['emp_id']

        todo = Todo.query.filter_by(sno=sno).first()
        todo.name = name
        todo.emp_id = emp_id
        
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    try:
        todo_to_delete = Todo.query.filter_by(sno=sno).first()

        if todo_to_delete:
            db.session.delete(todo_to_delete)
            todos_to_update = Todo.query.filter(Todo.sno > sno).all()

            for todo in todos_to_update:
                todo.sno -= 1
                db.session.add(todo)

            db.session.commit()
        
        return redirect("/")
    except Exception as e:
        # Log the exception for debugging purposes
        logging.error(str(e))
        return "An error occurred while processing your request.", 500

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run()

