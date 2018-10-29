
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz_password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'ie92jI93hus83hu9s'

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, title, body, owner):
        self.title = title 
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/blog/newpost')
        else:
            # TODO - explain login fail
            return '<h1>Error!</h1>'
            

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup(): 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO validate user data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect ('/blog/newpost')
        else:
            # TODO better response
            return '<h1>Duplicate user</h1>'



    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/')
def index():
    users = User.query.all()
    return render_template('user_list.html', page_title='Blogz', users=users)


@app.route('/blog', methods=['POST', 'GET'])
def view_post():

    blog_id = request.args.get('Blog.id')
    owner_id = request.args.get('User.id')
    title = request.args.get('title')
    username = request.args.get('username')
    users = User.query.filter_by(username=username).first()
    blogs = Blog.query.all()

    if owner_id is not None:
        blogs = Blog.query.filter_by(owner_id=owner_id).all()
        return render_template('singleUser.html', page_title='Blog Posts', blogs=blogs)
    
    if blog_id is not None:
        blogs = Blog.query.filter_by(id=blog_id)
        return render_template('single_post.html', page_title='Blog Post', blogs=blogs)
    
            
    return render_template('blog.html', page_title ='Blogz!', blogs=blogs)

@app.route('/blog/newpost', methods=['POST', 'GET'])
def add_post():
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        owner = User.query.filter_by(username=session['username']).first()
        title_error = ''
        content_error = ''

        if not title:
            title_error = "Please enter a blog title"
            
        if not content:
            content_error = "Please enter a blog post"
            
        if title_error or content_error:
            return render_template('newpost.html', title_error=title_error, content_error=content_error, page_title="New Entry")

        else:
            blog_post = Blog(title, content, owner)
            blog_id = request.args.get(Blog.id)
            db.session.add(blog_post)
            db.session.commit()
            return redirect('/blog?id='+str(blog_post.id))

    
    return render_template('newpost.html', page_title="New Entry")

if __name__ == '__main__':
    app.run()