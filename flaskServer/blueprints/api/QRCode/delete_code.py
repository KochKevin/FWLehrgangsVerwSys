import json
from flask import Blueprint, session,request, jsonify
import blueprints.db

bp = Blueprint("delete_code", __name__, static_folder="static", template_folder="templates")

@bp.route("/api/v1/delete_code",methods=["POST"] )
def delete_qr_code():
    
    
    print("API CALL: v1/delete_code")
        
    if not session["user_ID"]:
        #HTTPS Code: Forbidden
        return jsonify({"error_message" : "No user is logged in"}), 403


    if "user_rank" not in session:
        #Error something went wrong
         return jsonify({"error_message" : "Session Error"}), 403
    
    if session["user_rank"] < 1:
        #Error not enough rights to see that page
        return jsonify({"error_message" : ""}), 403
    
    
    data = request.json
    qr_code_id = data.get("qr_code_id")

    user_id = session["user_ID"]
    
    blueprints.db.delete_qualification_certificate(qr_code_id, user_id)
    
    plain_data = {
        "status" : "good"
    }
    
    
    return jsonify(plain_data), 200