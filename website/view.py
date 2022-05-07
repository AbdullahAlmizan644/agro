from flask import Blueprint, render_template
from website.__init__ import db,create_app

view=Blueprint('view',__name__)


@view.route("/")
def index():
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM posts")
    posts=cur.fetchall()
    return render_template("view/index.html",posts=posts)



@view.route("/contact")
def contact():
    return render_template("view/contact.html")



@view.route("/about")
def about():
    return render_template("view/about.html")


@view.route("/service")
def service():
    return render_template("view/services.html")


@view.route("/experts")
def experts():
    return render_template("view/expert.html")