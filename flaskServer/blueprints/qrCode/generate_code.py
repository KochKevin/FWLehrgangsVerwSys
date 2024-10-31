#Add better error handling
from flask import Blueprint, render_template, session, redirect

bp = Blueprint("generate-code", __name__, static_folder="static", template_folder="templates")

@bp.route("/generate-code")
def indexPage():
    
    #If user is not logged in redirect him to login
    if "user_ID" not in session:
        return redirect("/login?redirect=generate-code")
    
    if "user_rank" not in session:
        #Error something went wrong
        return redirect("/dashboard")
    
    if session["user_rank"] < 1:
        #Error not enough rights to see that page
        return redirect("/dashboard")
    
    return render_template("generate-code.html")



