from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__,)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'
db=SQLAlchemy(app)

class Blogpost(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100),nullable=False,default='Title')
    content=db.Column(db.Text,nullable=False,default='content')
    author=db.Column(db.String(30),nullable=False,default='Authorwa')
    date_post=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return 'blog post   '+ str(self.id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts',methods=['GET','POST'])     
def posts():

    if request.method=='POST':
        post_title=request.form['title']
        post_content=request.form['content']
        post_author=request.form['author']
        newblog=Blogpost(title=post_title,content=post_content,author=post_author)
        db.session.add(newblog)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts= Blogpost.query.order_by(Blogpost.date_post).all()
        return render_template('posts.html',crib=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post=Blogpost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    post=Blogpost.query.get_or_404(id)
    if request.method=='POST':
        post.title=request.form['title']
        post.author=request.form['author']
        post.content=request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html',editor=post)



@app.route('/<string:name>/posts/<int:id>')
def hello(name,id):

    return "heelo bhai,"+ name+"your id is "+str(id)

if __name__=="__main__":
    app.run(debug=True)