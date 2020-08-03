from ownblog import app ,bcrypt ,db
from flask import Flask ,render_template , redirect ,url_for,flash ,request
from ownblog.forms import LoginForm , RegistrationForm ,PostForm , CommentForm
from ownblog.models import User , Post ,Comment
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user ,current_user, logout_user ,login_required

@app.route("/home")
@app.route("/")
def home():
    page= request.args.get('page', 1, type=int)
    posts= Post.query.paginate(page=page, per_page=4)
    return render_template('home.html',title="Meow Blogs", posts=posts)

@app.route("/s")
def s():
    return render_template("container.html")

@app.route("/login" , methods=["post","get"])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html", form=form)

@app.route("/register", methods=["post","get"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data)
        user= User(username=form.username.data , password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("User created!!","info")
        return redirect(url_for('login'))
    return render_template("register.html", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_required
@app.route("/post",methods=["Post","GET"])
def post():
    form =PostForm()
    if form.validate_on_submit():
        flash("Post created", 'success')
        post= Post(title=form.title.data, content=form.post.data , author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('post.html',form=form)

@app.route("/upvote/<int:post_id>")
def upvote(post_id):
    post= Post.query.filter_by(id=post_id).first()
    post.upvotes= post.upvotes+1
    post.author.karma= post.author.karma+1
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/downvote/<int:post_id>")
def downvote(post_id):
    post= Post.query.filter_by(id=post_id).first()
    post.downvotes= post.downvotes+1
    post.author.karma= post.author.karma-0.5
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/post/<int:post_id>" , methods=["post","get"])
def see_post(post_id):
    post=Post.query.filter_by(id=post_id).first()
    comment_on_post = Comment.query.filter_by(post_id=post_id).all()
    form= CommentForm()
    if form.validate_on_submit():
        comment_add= Comment(content=form.post.data , author_id=current_user.id , post_id=post.id)
        db.session.add(comment_add)
        db.session.commit()
        return redirect(url_for('see_post',post_id=post.id))
    return render_template('see_post.html',post=post , comments=comment_on_post , form=form)

@app.route("/user/<int:user_id>")
def see_user(user_id):
    user= User.query.filter_by(id=user_id).first()
    return render_template('see_user.html' , user=user)

@app.route("/post/edit/<int:post_id>" , methods=["post","GET"])
def edit_post(post_id):
    post= Post.query.filter_by(id=post_id).first()
    if current_user!=post.author:
        return redirect(url_for('home'))
    form= PostForm()
    if form.validate_on_submit():
        post.title= form.title.data
        post.content = form.post.data
        db.session.commit()
        return redirect(url_for('home'))
    form.title.data= post.title
    form.post.data=post.content
    return render_template("edit.html", form=form)

@app.route("/post/delete/<int:post_id>" , methods=["POST"])
def delete_post(post_id):
    post= Post.query.filter_by(id=post_id).first()
    if current_user!=post.author:
        return redirect(url_for('home'))
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Your Post has been deleted' , 'success')
        return redirect (url_for('home'))
    


