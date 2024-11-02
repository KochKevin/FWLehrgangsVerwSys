from flask import Blueprint, request, session, jsonify
import bcrypt
import blueprints.db


import time

bp = Blueprint("auth", __name__, static_folder="static", template_folder="templates")



#Auth Login

@bp.route("/auth/login", methods=["POST"])
def on_auth_login():
    data = request.json
    
    email = data.get("email")
    plain_password = data.get("password")

    #Get User Data with Mail from DB
    user_data = blueprints.db.get_user_by_mail(email)
    
    if user_data is None:
        print("ERROR: User login: User does not exist")
        return jsonify({"login_status": "bad", "error_message" : "Nutzer nicht gefunden. Überprüfen Sie ihre Email"}), 200
    
    #user_data[4] is the hashed password
    if not check_password(plain_password, user_data[4]):
        print("ERROR: User login: Password incorrect")
        return jsonify({"login_status": "bad", "error_message" : "Passwort Ungültig"}), 200
    
     
    set_session_data(user_data[0], user_data[5])
    
    print("User succesfully logged in")

    return jsonify({"login_status": "good", "redirect_url" : "/dashboard"}), 200




#Auth Signup
#Change to api/v2/auth/signup
@bp.route("/auth/signup", methods=["POST"])
def on_auth_signup():
    
    
    
    data = request.json
    
    print("Signup Data: ", data)

    municipalitie = data.get("municipalitie")
    fire_station = data.get("fire_station")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    plain_password = data.get("password")
    
    #Set up user Data
    if not blueprints.db.check_if_mail_is_available(email):
        print("ERROR: User signup: Email already exist")
        return jsonify({"login_status": "bad", "error_message" : "Ihre Email wird bereits genutzt"}), 200
    
    
    #Hash Password and add user to db
    hashed_password = hash_password(plain_password)
    user_ID = blueprints.db.add_user(municipalitie, fire_station, first_name, last_name, email, hashed_password, 2)
    
    print(user_ID)
    
    #Später ändern
    #       -> Eventuell die eingetragenen Daten direkt wieder aus DB lesen
    set_session_data(user_ID, 0)
    
    
    # add course data:
    add_course_data(user_ID)
    
    
    print("User succesfully signed up")
     
    return jsonify({"login_status": "good", "redirect_url" : "/dashboard"}), 200


@bp.route("/auth/logout", methods=["POST"])
def on_auth_logout():
    
    if "user_ID" not in session:
        return jsonify({"logout_status": "bad"}), 200
    
    
    print("User Logged out")
    session.clear()
    return jsonify({"logout_status": "good", "redirect_url" : "/"}), 200




#Hashing
def hash_password(plain_password):
    #Hash password and convert it to utf-8, so that it can be saved in db
    #Change salt to a not const value
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")

def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

#Managing Session
def set_session_data(user_ID, user_rank):
    session["user_ID"] = user_ID
    session["user_rank"] = user_rank
    
    session["user_agent"] = request.headers.get("User-Agent")
    session["ip_address"] = request.remote_addr
    
    print("SESSION DATA: USER ID: ", session["user_ID"]," USER RANK: ", session["user_rank"] , " userAgent: ", session["user_agent"], " ipAdress: ", session["ip_address"])
    
    return



@bp.route("/auth/test")
def on_test():
    #add_course_data(1)
    #add_course_data(2)
    return 



def add_course_data(user_id):

    
    start_time = time.time()
    
    
    #tupel
    qualification_ids = blueprints.db.get_qualification_ids()
    blueprints.db.add_qualifications_to_user(user_id, qualification_ids)
    print("Status: added qualification to user #", user_id)

    #tupel
    training_units = blueprints.db.get_training_units(qualification_ids)
    blueprints.db.add_training_units_users(training_units, user_id)
    print("Status: added training_units to user #", user_id)
    
    
    blueprints.db.add_all_user_sessions(user_id)
    print("Status: added user_sessions to user #", user_id)
    
    
    
    end_time = time.time()
    
    print("Total Time needed to procces: ", (end_time - start_time)/60, "min")
    
    return