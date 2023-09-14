from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://empadmin:Flask_App_23@postgres-app-db.postgres.database.azure.com:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
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
        todo = Todo(name=name, emp_id=emp_id)
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
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()

    db.engine.execute(text(f"SELECT setval('todo_sno_seq', (SELECT max(sno) FROM todo));"))
    return redirect("/")

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run()

