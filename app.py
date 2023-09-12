from flask import Flask, render_template, request, redirect, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras
import webbrowser


app = Flask(__name__)
# app.secret_key = 'my_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Suyash12345@localhost/suyash"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


POSTGRES_HOST = 'localhost'
POSTGRES_DB = 'suyash'
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'Suyash12345'
port_id = 5432
conn = None
cur = None

try:
    conn = psycopg2.connect(
                host = POSTGRES_HOST,
                dbname = POSTGRES_DB,
                user = POSTGRES_USER,
                password = POSTGRES_PASSWORD,
                port = port_id)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    create_script = ''' CREATE TABLE IF NOT EXISTS todo(
                            sno     int PRIMARY KEY,
                            name   varchar(40) NOT NULL,
                            emp_id int) '''

    cur.execute(create_script)
    conn.commit()

except Exception as error:
    print(error)

finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()

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
