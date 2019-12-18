from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
    # database is initialized with settings from our app

class Todo(db.Model): # why db.Model? Is is the argument we will later pass? This is our Todo model
    id = db.Column(db.Integer, primary_key=True) # first column
    content = db.Column(db.String(200), nullable =False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self): # what is this?
        return '<Task %r>' % self.id

 # tells the database where our app is located
@app.route('/', methods=['POST', 'GET'])
def index():
    # return "Hello world!"
    # if methods sent to this request is a POST request
    if request.method == 'POST':
        # pass
        task_content = request.form['content'] # setting up variable. request's form section, choose contents of tag with id="content", which is in the HTML
        new_task = Todo(content=task_content) # creating a todo object with its content equal to content to input

        try: # pushing to database
            db.session.add(new_task)
            db.session.commit()
            return redirect('/') # back to index page
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # query database, order by oldest and grab all
        # return render_template('index.html') will automatically look at templates folder.
        return render_template('index.html', tasks=tasks) # passing into template

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) # attempt to get task by id

    try: 
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content'] # look in HTML for id="content"
        # setting up objects's  key-value pairs

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    
    else:
        return render_template('update.html', task=task) # like passing down props


if __name__ == "__main__":
    app.run(debug = True) # error shows up

