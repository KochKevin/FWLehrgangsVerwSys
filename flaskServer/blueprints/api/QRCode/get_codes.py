import json
from flask import Blueprint, session,request, jsonify
import blueprints.db

bp = Blueprint("get_qr_codes", __name__, static_folder="static", template_folder="templates")

@bp.route("/api/v1/get_qr_codes",methods=["POST"] )
def create_qr_code():
    
    
    print("API CALL: v1/get_qr_codes")
        
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
    
    qualification_certificate_created_by_user = blueprints.db.get_created_qualification_certificate_from_user(user_id)
    
    print(qualification_certificate_created_by_user)
    
    
    qualification_certificates_plain_data = []
    
    for row in qualification_certificate_created_by_user:
        qualification_certificates_plain_data.append({
            
            "id" : row[0],
            "code" : row[1],
            "qualification_level" : row[2],
            "created_timestamp" : row[4],
            "end_timestamp" : row[5],
            "amount_of_uses" : row[6]
        })
    
    
    plain_data = {
        "qualification_certificates" : qualification_certificates_plain_data
    }
    
    
    return jsonify(plain_data), 200