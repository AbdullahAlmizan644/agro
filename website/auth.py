from distutils.log import error
from flask import Blueprint, redirect, render_template,request,flash,session
from datetime import datetime
from website.__init__ import db,create_app
auth=Blueprint('auth',__name__)



@auth.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        name=request.form.get("username")
        password=request.form.get("password")

        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users where username=%s and password=%s",(name,password))
        user=cur.fetchone()
        print(user)

        if user:
            session['user']=name
            flash("Login successfully!", category="success")
            return redirect("/profile")
        else:
            flash("Wrong username or password!", category="error")

    return render_template("auth/login.html")



@auth.route("/signup", methods=["GET","POST"])
def signup():    
    if request.method=="POST":
        username=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")

        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users where username=%s and password=%s",(username,password))
        user=cur.fetchone()

        if user:
            flash("username already exist!", category="error")

        elif len(username)<5:
            flash("Name must be greater than 5 digit", category="error")


        elif len(email)<5:
            flash("Email must be greate than 5 digit ", category="error")


        elif len(password)<8:
            flash("Name must be greater than 8 digit", category="error")


        else:
            cur=db.connection.cursor()
            cur.execute("INSERT INTO users(username,email,password,date) values(%s,%s,%s,%s)",(username,email,password,datetime.now()))
            db.connection.commit()
            cur.close()
            flash("Your account created successfully!", category="success")
            return redirect("/login")


    return render_template("auth/signup.html")




@auth.route("/profile")
def profile():
    if "user" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * from users where username=%s",(session["user"],))
        user_details=cur.fetchone()

        cur=db.connection.cursor()
        cur.execute("SELECT count(post_id) from posts where writer=%s",(session["user"],))
        total_posts=cur.fetchone()
        return render_template("auth/profile.html",user_details=user_details, total_posts=total_posts)

    else:
        return redirect("/login")


@auth.route("/delete_user_post/<int:sno>")
def delete_user_post(sno):
    cur=db.connection.cursor()
    cur.execute("Delete FROM posts where post_id=%s",(sno,))
    db.connection.commit()
    return redirect("/all_review")


@auth.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")
