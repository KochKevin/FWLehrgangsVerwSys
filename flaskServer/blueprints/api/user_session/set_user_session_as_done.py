from flask import Blueprint, session,request, jsonify
import blueprints.db

#from datetime import datetime

bp = Blueprint("set_user_session_as_done", __name__, static_folder="static", template_folder="templates")

@bp.route("/api/set_user_session_as_done", methods=["POST"]) 
def set_user_session_as_done():
    

    if not session["user_ID"]:
        #HTTPS Code: Forbidden
        return jsonify({"error_message" : "No user is logged in"}), 403
    
    
    data = request.json
    
    session_id = data.get("session_id")
    #session_id = 279
    is_done_timestamp = data.get("is_done_timestamp")
    #get time stap here
    #is_done_timestamp = ""
    user_id = session["user_ID"]
    #user_id = 35
    
    
    blueprints.db.set_session_is_done(user_id, session_id, is_done_timestamp)

    new_session_data = blueprints.db.get_session(user_id, session_id)

    print("New sessions data:", new_session_data)


    qualification_id = new_session_data[0][2]
    print("QUAL ID 1: ", qualification_id)

    blueprints.db.update_user_sessions_done(user_id, qualification_id, 1)

    if blueprints.db.check_if_user_has_done_all_sessions(user_id, qualification_id):
        #User completed all sessions and it sets the qualifiaction as done
        blueprints.db.set_qualification_as_completed(qualification_id, user_id, 1)
    else:
        blueprints.db.set_qualification_as_completed(qualification_id, user_id, 0)



    plain_data = {
        
        "session_id" : session_id,
        "trainig_unit_id" : new_session_data[0][1],
        "qualification_id" : new_session_data[0][3],
        "type" : new_session_data[0][4],
        "is_done" : new_session_data[0][5],
        "is_done_timestamp" : new_session_data[0][6],

    }   
    

    return jsonify({"session" : plain_data,}), 200