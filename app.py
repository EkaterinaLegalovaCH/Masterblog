from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)
users = {
    'Alice': {'age': 25, 'country': 'USA'},
    'Bob': {'age': 30, 'country': 'UK'},
    'Charlie': {'age': 35, 'country': 'Australia'}
}


@app.route('/')
def index():
    user = request.args.get('name')
    if not user:
        user = "Anonymous"
    return render_template('index.html', title='Home', name=user, users=users, time=datetime.now())


@app.route('/greet/<name>')
def greet(name):
    return render_template('index.html', title='Home', name=name)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f"post id is {post_id}."


@app.route('/all-users')
def all_users():
    return render_template('all-users.html', users=users)


@app.route('/form')
def form():
    return render_template('form.html', title='Form')


if __name__ == "__main__":
    # Launch the Flask dev server
    app.run(host="0.0.0.0", port=5000)
