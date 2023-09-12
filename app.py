from sqlalchemy import create_engine, Column, Integer, String
from flask import Flask, render_template, request, redirect, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import psycopg2.extras


app = Flask(__name__)
# app.secret_key = 'my_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://empadmin:Flask_App3@postgres.database.azure.com/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
db_session = Session()
Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todo'
    sno = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    emp_id = Column(Integer)

Base.metadata.create_all(engine)
db_session.commit()

class Todo(db.Model):
    
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    emp_id = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"
        
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        name = request.form['name']
        emp_id = request.form['emp_id']
        
        if not name or not emp_id:
            flash('Both fields are required. Please fill them in.', 'error')
        else:
            todo = Todo(name=name, emp_id=emp_id)
            db.session.add(todo)
            db.session.commit()
            
    
    allTodo = Todo.query.all()
    error_messages = get_flashed_messages(category_filter=['error'])
    return render_template('index.html', allTodo=allTodo, error_messages=error_messages)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        name = request.form['name']
        emp_id = request.form['emp_id']
        if not name or not emp_id:
            flash('Both fields are required. Please fill them in.', 'error')
        else:
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
    return redirect("/")

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run()
