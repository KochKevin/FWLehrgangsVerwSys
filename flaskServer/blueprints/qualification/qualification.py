from flask import Blueprint,session, render_template, redirect, request

bp = Blueprint("qualification", __name__, static_folder="static", template_folder="templates")

@bp.route("/qualification")
def indexPage():
    
    qualification_id = request.args.get("id")
    
    #If user is not logged in redirect him to login
    if "user_ID" not in session:
        
        if qualification_id:
            return redirect("/login?redirect=qualification?id=" + qualification_id)
        else:
            return redirect("/login?redirect=qualification" )
    
    return render_template("qualification.html", method=["GET"])