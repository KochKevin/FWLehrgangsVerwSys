import json
from flask import Blueprint, session,request, jsonify
import blueprints.db

bp = Blueprint("get_code_creation_settings", __name__, static_folder="static", template_folder="templates")

@bp.route("/api/v1/get_code_creation_settings",methods=["POST"] )
def get_code_creation_settings():
    
    print("API CALL: v1/get_code_creation_settings")
        
    if not session["user_ID"]:
        #HTTPS Code: Forbidden
        return jsonify({"error_message" : "No user is logged in"}), 403
    
    if "user_rank" not in session:
        #Error something went wrong
         return jsonify({"error_message" : "Session Error"}), 403
    
    if session["user_rank"] < 1:
        #Error not enough rights to see that page
        return jsonify({"error_message" : ""}), 403
    
    
    #Hard coded settings, should later be loaded from db
    
    qualification_levels = [
            {
                "id" : 1,
                "titel" :  "Einsatzfähigkeit"
            },
            {
                "id" : 2,
                "titel" :  "Selbständige Wahrnehmung der Truppmitgliedfunktion innerhalb einer Staffel oder Gruppe"
            },
            {
                "id" : 3,
                "titel" : "Befähigung zur selbständigen Wahrnehmung der Truppführerfunktion innerhalb der Staffel oder Gruppe"
            },
            {
                "id" : 4,
                "titel" :  "Sprechfunker"
            }
        ]
    
    
    amount_uses = {
        "min" : 1,
        "max" : 100
    }
    
    code_life_time = {
        "in_hours" : 24
    }
    
    plain_data = {
        "qualification_levels" : qualification_levels,
        "amount_uses" : amount_uses,
        "code_life_time" : code_life_time,
        "max_amount_codes" : 5
    }
    
    
    return jsonify(plain_data), 200