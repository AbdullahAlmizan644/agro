from crypt import methods
from flask import Blueprint, redirect, render_template,request,session,flash,redirect
from website.__init__ import db,create_app

admin=Blueprint('admin',__name__)



@admin.route("/dashboard")
def dashboard():
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users")
        users=cur.fetchall()

        cur=db.connection.cursor()
        cur.execute("SELECT count(sno) from users ")
        total_user=cur.fetchone()

        cur=db.connection.cursor()
        cur.execute("SELECT count(post_id) from posts ")
        total_posts=cur.fetchone()
        return render_template("admin/index.html",users=users,total_user=total_user,total_posts=total_posts)
    else:
        return redirect("/admin_login")



@admin.route("/admin_login",methods=["GET","POST"])
def admin_login():
    if request.method=="POST":
        email=request.form.get("email") 
        password=request.form.get("password")

        if email=="admin@gmail.com" and password=="12345":
            session["admin"]=email
            return redirect("/dashboard") 
        else:
            flash("wrong mail or password", category="error")
    return render_template("admin/login.html")



@admin.route("/admin_logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/")


@admin.route("/all_user")
def all_user():
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users")
        users=cur.fetchall()

        cur=db.connection.cursor()
        cur.execute("SELECT count(sno) from users ")
        total_user=cur.fetchone()
        return render_template("admin/user.html",total_user=total_user,users=users)

    else:
        return redirect("/admin_login")


@admin.route("/delete_user/<int:sno>")
def delete_user(sno):
    cur=db.connection.cursor()
    cur.execute("Delete FROM users where sno=%s",(sno,))
    db.connection.commit()
    return redirect("/dashboard")


@admin.route("/all_posts")
def all_posts():
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM posts")
        posts=cur.fetchall()

        cur=db.connection.cursor()
        cur.execute("SELECT count(post_id) from posts ")
        total_post=cur.fetchone()
        return render_template("admin/posts.html",total_post=total_post,posts=posts)

    else:
        return redirect("/admin_login")


    
@admin.route("/delete_post/<int:sno>")
def delete_post(sno):
    cur=db.connection.cursor()
    cur.execute("Delete FROM posts where post_id=%s",(sno,))
    db.connection.commit()
    return redirect("/all_posts")
