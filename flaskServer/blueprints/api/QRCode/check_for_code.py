from flask import Blueprint, session,request, jsonify
import blueprints.db
from datetime import datetime


bp = Blueprint("check_for_code", __name__, static_folder="static", template_folder="templates")

@bp.route("/api/v1/check-for-code", methods=["POST"]) 
def check_for_code():
    
    
    print("API CALL: v1/check-for-code")
    
    if not session["user_ID"]:
        #HTTPS Code: Forbidden
        return jsonify({"error_message" : "No user is logged in"}), 403
    
    
    data = request.json
    
    qualification_certificate_code = data.get("qualification_code")
    
    user_id = session["user_ID"]
    
    
    qualification_certificate_data = blueprints.db.find_qualification_certificate(qualification_certificate_code)


    print(qualification_certificate_data)

    if len(qualification_certificate_data) == 0:
            #Qualificatrion does not exist
            return jsonify({"status": 0, "error_message" : "Dieser Code existiert nicht mehr"}), 403
    
    
    qualification_certificate_id = qualification_certificate_data[0][0]
    qualification_id = qualification_certificate_data[0][2]
    
    
    #Check if code is still valid
    
    time_format = "%Y-%m-%d %H:%M:%S.%f"
    certificate_end_time = datetime.strptime(qualification_certificate_data[0][5], time_format)
    
    current_time = datetime.now()
    
    if current_time > certificate_end_time:
        #Code is expired
        return jsonify({"status": 0, "error_message" : "Dieser Code is abgelaufen"}), 403
    

    
    #Check if user has not already qualification
    
    if blueprints.db.check_if_user_has_qualification(user_id, qualification_id):
        #User has already the qualification
        return jsonify({"status": 0, "error_message" : "Qualifikation bereits erhalten"}), 403
    
    
    
    
    
    
    #Set Qualifiacation for user as completed  
    blueprints.db.set_qualification_as_completed(qualification_id, user_id, 1)
    
    #Increase amount of uses by one  
    blueprints.db.increase_amount_uses_of_qualification_certificate(qualification_certificate_id, 1)
    
    
    
    
    data = {
        "message" : "Herzlichen Glückwunsch zum Bestehen der Qualifikationstufe "  + str(qualification_id),
        "status" : 1
    }
 
    return jsonify(data), 200