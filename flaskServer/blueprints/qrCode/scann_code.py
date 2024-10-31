from flask import Blueprint, render_template, session, redirect, request

bp = Blueprint("scann-code", __name__, static_folder="static", template_folder="templates")

@bp.route("/scann-code")
def indexPage():
    
    
    qr_code = request.args.get("c")
    
    #If user is not logged in redirect him to login
    if "user_ID" not in session:
        
        if qr_code:
            return redirect("/login?redirect=scann-code?c=" + qr_code)
        else:
            return redirect("/login?redirect=scann-code" )
    
   
        
        
    
    return render_template("scann-code.html")