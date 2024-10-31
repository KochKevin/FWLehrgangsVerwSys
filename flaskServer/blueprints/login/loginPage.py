from flask import Blueprint, render_template

bp = Blueprint("login", __name__, static_folder="static", template_folder="templates")

@bp.route("/login")
def index_page():
   
    return render_template("login.html")
