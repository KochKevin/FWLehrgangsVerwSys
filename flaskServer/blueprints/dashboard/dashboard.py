from flask import Blueprint, render_template, session, redirect

bp = Blueprint("dashboard", __name__, static_folder="static", template_folder="templates")

@bp.route("/dashboard")
def indexPage():
    
    #If user is not logged in redirect him to login
    if "user_ID" not in session:
        return redirect("/login?redirect=dashboard")
    
    return render_template("dashboard.html")

    