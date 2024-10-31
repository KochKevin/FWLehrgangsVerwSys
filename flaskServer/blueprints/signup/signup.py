from flask import Blueprint, render_template

bp = Blueprint("signup", __name__, static_folder="static", template_folder="templates")

@bp.route("/signup")
def indexPage():
    return render_template("signup.html")