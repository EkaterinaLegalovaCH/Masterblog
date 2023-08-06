from flask import Flask, render_template, request, redirect, url_for
import json


DATA_FILE = "data.json"
app = Flask(__name__)


def read_file(file_name):
    """
    take a file name as a parameter, open it, read
    and transfer info in a dictionary,
    return this dictionary.
    """
    with open(file_name, "r") as handle:
        posts_data = handle.read()
        posts_list = json.loads(posts_data)
        return posts_list

def write_file(file_name, new_data):
    """
    take a name of file for storaging info and new info,
    write this information in a file
    """
    with open(file_name, "w") as handle:
        handle.write(new_data)


def fetch_post_by_id(post_id):
    posts = read_file(DATA_FILE)
    for post in posts:
        if int(post["id"]) == int(post_id):
            print(post)
            return post



@app.route('/')
def index():
    blog_posts = read_file(DATA_FILE)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        global DATA_FILE
        blog_posts = read_file(DATA_FILE)
        new_id = len(blog_posts) + 1
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        new_post = {"id": new_id, "author": author, "title": title, "content": content}
        blog_posts.append(new_post)
        new_data = json.dumps(blog_posts)
        write_file(DATA_FILE, new_data)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<post_id>', methods=['POST'])
def delete(post_id):
    global DATA_FILE
    blog_posts = read_file(DATA_FILE)
    post_id = int(post_id)
    new_blog_posts = [item for item in blog_posts if item["id"] != post_id]
    new_data = json.dumps(new_blog_posts)
    write_file(DATA_FILE, new_data)
    return redirect(url_for('index'))


@app.route('/edit_post/<int:post_id>')
def edit_post(post_id):
    return render_template('update.html', post_id=post_id)


@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):
    global DATA_FILE
    posts = read_file(DATA_FILE)
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form.get('author', '')
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        for post in posts:
            if int(post["id"]) == int(post_id):
                post["author"] = author
                post["title"] = title
                post["content"] = content
            new_data = json.dumps(posts)
            write_file(DATA_FILE, new_data)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)



if __name__ == "__main__":
    app.run(debug=True)
