#Modfy entrie in db

from flask import Blueprint, session,request, jsonify
import blueprints.db

bp = Blueprint("update_qr_code_data", __name__, static_folder="static", template_folder="templates")

@bp.route("/api/v1/update-qr-code-data", methods=["POST"]) 
def create_qr_code():
    
    print("API CALL: v1/update-qr-code-data")
        
    if not session["user_ID"]:
        #HTTPS Code: Forbidden
        return jsonify({"error_message" : "No user is logged in"}), 403


    if "user_rank" not in session:
        #Error something went wrong
         return jsonify({"error_message" : "Session Error"}), 403
    
    if session["user_rank"] < 1:
        #Error not enough rights to see that page
        return jsonify({"error_message" : ""}), 403
    
    
    user_id = session["user_ID"]
    
    data = request.json
    certificate_id = data.get("certificate_id")
    qualification_id = data.get("qualification_id")
    max_amount_of_uses = data.get("max_amount_of_uses")
    
    
    
    blueprints.db.update_certificate(qualification_id, max_amount_of_uses, certificate_id, user_id)

    
    plain_data = {
        "status" : "good"
    }
    
    
    return jsonify(plain_data), 200