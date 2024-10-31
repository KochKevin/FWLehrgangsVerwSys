from flask import Blueprint,request, session, jsonify
import blueprints.db

bp = Blueprint("get_training_units", __name__, static_folder="static", template_folder="templates")

@bp.route("/api/get_training_units", methods=["POST"] )
def on_get_training_units():
    

    if "user_ID" not in session:
        #HTTPS Code: Forbidden
        return jsonify({"error_message" : "No user is logged in"}), 403
    
    
    data = request.json
    
    qualification_id = data.get("qualification_id")
    #qualification_id = 1
    
    user_id = session["user_ID"]
    
    training_units_and_sessions = blueprints.db.get_training_units_and_sessions(qualification_id, user_id)
    
    qualification_titel = blueprints.db.get_qualifications_titel(qualification_id)[0][0]
    
    #Arry for all training units
    training_unit_list = []
    
    #Last usec training_unit_id
    last_training_unit_id = 0
    
    for row in training_units_and_sessions:
        current_training_unit_id = row[0]
        
        if current_training_unit_id != last_training_unit_id:
            last_training_unit_id = current_training_unit_id
            
            training_unit = {}
            
            training_unit["titel"] = row[1]
            training_unit["number"] = row[2]
            training_unit["learngoals"] = row[3]
            training_unit["content"] = row[4]
            training_unit["comments"] = row[5]
            training_unit["sessions"] = []
            
            training_unit_list.append(training_unit)
            
            session_data = {}
            session_data["session_id"] = row[6]
            session_data["type"] = row[7]
            session_data["is_done"] = row[8]
            session_data["is_done_timestamp"] = row[9]
            
            #Access last element in list and add new session element
            training_unit_list[-1]["sessions"].append(session_data)
            
        else:
            session_data = {}
            session_data["session_id"] = row[6]
            session_data["type"] = row[7]
            session_data["is_done"] = row[8]
            session_data["is_done_timestamp"] = row[9]
            
            #Access last element in list and add new session element
            training_unit_list[-1]["sessions"].append(session_data)
               
    plain_data = {
        "qualification_titel" : qualification_titel, 
        "training_units": training_unit_list
    }
    
    return jsonify(plain_data), 200