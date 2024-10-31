from flask import Blueprint, session, jsonify
import blueprints.db

bp = Blueprint("get_user_information", __name__, static_folder="static", template_folder="templates")

@bp.route("/api/get_user_information", methods=["POST"]) 
def get_user_information():
    
    user_id = session["user_ID"]
    
    user_data = blueprints.db.get_user_data_by_id(user_id)
    user_data = user_data[0]
    print("User Data: ", user_data)
    
    #Eventuell name und mail rausnehmen, weil es zu sensible daten sind
    
    plain_data = {
        
        "user_id" : user_data[0],
        #"first_name" : user_data[1],
        #"last_name" : user_data[2],
        #"mail_adress" : user_data[3],
        "rank" : user_data[5],
        "is_activated" : user_data[6]
    }
    
    return jsonify(plain_data), 200