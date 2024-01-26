from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# We set a config variable (with the path below) to the database. And, the three '///' means this is a relative path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# now we create database
db = SQLAlchemy(app)

# Had to find this on stackoverflow after trying a few different failed solutions. Error message "working out of context"
app.app_context().push()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


# the default (or home) route
@app.route('/')
def index():
    # show all todos
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)


@app.route("/add", methods=["POST"]) # an example of a concept -- decorating, he said
def add():
    # add new item
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/update/<int:todo_id>") 
def update(todo_id):
    # query database for id and modify complete variable
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # delete an item for database
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


# # the about route
# @app.route('/about')
# def about():
#     return "About"

if __name__ == '__main__':
    # we create database before we run app
    db.create_all()
    app.run(debug=True)