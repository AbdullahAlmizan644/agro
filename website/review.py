from flask import Blueprint, redirect,render_template,request, session,flash
from .__init__ import db,create_app
from datetime import datetime
import os
from werkzeug.utils import secure_filename



review=Blueprint("review", __name__)
app=create_app()

@review.route("/review")
def blog():
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM posts")
    posts=cur.fetchall()
    return render_template("view/blog.html",posts=posts)



@review.route("/review_details/<int:id>")
def blog_details(id):
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM posts where post_id=%s",(id,))
    post=cur.fetchone()

    cur=db.connection.cursor()
    cur.execute("SELECT * FROM posts")
    posts=cur.fetchall()
    return render_template("view/blog-single.html",post=post,posts=posts)


@review.route("/user_review",methods=["GET","POST"])
def user_review():
    if "user" in session:
        if request.method=="POST":
            title=request.form.get('title')
            content=request.form.get('ckeditor')
            image = request.files['image']
            if image.filename == '':
                flash('No selected file', category="error")
                return redirect(request.url)
            else:
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))

            cur=db.connection.cursor()
            cur.execute("INSERT INTO posts(title,content,writer,date,image) values(%s,%s,%s,%s,%s)",(title,content,session["user"],datetime.now(),image.filename))
            db.connection.commit()
            return redirect("/review")
        return render_template("view/user_review.html")

    else:
        return redirect("/login")


@review.route("/all_review",methods=["GET","POST"])
def all_review():
    if "user" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM posts where writer=%s",(session["user"],))
        posts=cur.fetchall()
        return render_template("view/all_review.html",posts=posts)

    else:
        return redirect("/login")






@review.route("/edit_review/<int:sno>",methods=["GET","POST"])
def edit_review(sno):
    if "user" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM posts WHERE post_id=%s",(sno,))
        post=cur.fetchone()
        if request.method=="POST":
            title=request.form.get('title')
            content=request.form.get('ckeditor')
            image = request.files['image']
            if image.filename == '':
                flash('No selected file', category="error")
                return redirect(request.url)
            else:
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))

            cur=db.connection.cursor()
            cur.execute("UPDATE posts set title=%s,content=%s,image=%s, WHERE post_id=%s",(title,content,image.filename,sno,))
            db.connection.commit()
            return redirect("/all_review")
        return render_template("view/edit_user_review.html",post=post)

    else:
        return redirect("/login")

