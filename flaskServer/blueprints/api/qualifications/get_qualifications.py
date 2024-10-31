from flask import Blueprint, session, jsonify
import blueprints.db

bp = Blueprint("get_qualifications", __name__, static_folder="static", template_folder="templates")

#Return all qualifications for from DB as JSON
@bp.route("/api/get_qualifications_for_user", methods=["POST"]) 
def on_get_qualifications():
    

    if not session["user_ID"]:
        #HTTPS Code: Forbidden
        return jsonify({"error_message" : "No user is logged in"}), 403
    
    user_id = session["user_ID"]
    
    qualifications = blueprints.db.get_qualifications_for_user(user_id)
    
    plain_data = []
    
    for row in qualifications:
        plain_data.append({"id" : row[0], "qualification-level" : row[1], "titel" : row[2], "total_session_amount" : row[3], "sessions_done_amount" : row[4], "is_done" : row[5]})
    
    
    plain_data = {
        "qualifications": plain_data
    }
    
    return jsonify(plain_data), 200


