
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:MyNewPass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    
    def __init__(self, title, body):
        self.title = title 
        self.body = body

#@app.route('/blog')
#def view_blog():
    #blog_post = (Blog.title, Blog.body)
    #blog_title = request.args.get(Blog.title)
    #blog_content = request.args.get(Blog.body)
    #blog_id = request.args.get(Blog.id)
    #all_blogs = Blog.query.all()
    #return render_template('blog.html', page_title = "Build a Blog!", all_blogs=all_blogs, blog_title=blog_title, blog_content=blog_content)

@app.route('/blog', methods=['POST', 'GET'])
def view_post():

    # blog_title = request.args.get(Blog.title)
    # blog_content = request.args.get(Blog.body)
    blog_id = request.args.get('id')
    print('##############')
    print(blog_id)

    if blog_id is not None:
        blogs = Blog.query.filter_by(id=blog_id)
        print("test")
        return render_template('single_post.html', page_title='Blog Post', blogs=blogs)
        
    else:
        blogs = Blog.query.all()
        print("test2")
        return render_template('blog.html', page_title ='Build a Blog!', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def add_post():
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        title_error = ''
        content_error = ''

        if not title:
            title_error = "Please enter a blog title"
            
        if not content:
            content_error = "Please enter a blog post"
            
        if title_error or content_error:
            return render_template('newpost.html', title_error=title_error, content_error=content_error, page_title="New Entry")

        else:
            blog_post = Blog(title, content)
            blog_id = request.args.get(Blog.id)
            db.session.add(blog_post)
            db.session.commit()
            return redirect('/blog?id='+str(blog_post.id))

    
    return render_template('newpost.html', page_title="New Entry")



if __name__ == '__main__':
    app.run()