from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# создаём базу данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()


@app.route('/', methods=["GET", "POST"])
def homepage():
    tasks = Todo.query.all()
    if request.method == "POST":
        text = request.form['text']
        task = Todo(text=text)
        db.session.add(task)
        db.session.commit()
        return redirect('/')

    return render_template('homepage.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get(id)
    return render_template('update.html', task=task)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
