#Create new entry in db

from time import timezone
from flask import Blueprint, session,request, jsonify
import blueprints.db
import datetime
import hashlib


bp = Blueprint("create_qr_code", __name__, static_folder="static", template_folder="templates")

@bp.route("/api/v1/create-qr-code-data", methods=["POST"]) 
def create_qr_code():
    
    
    print("API CALL: v1/create-qr-code")
    
    if not session["user_ID"]:
        #HTTPS Code: Forbidden
        return jsonify({"error_message" : "No user is logged in"}), 403

    if "user_rank" not in session:
        #Error something went wrong
         return jsonify({"error_message" : "Session Error"}), 403
    
    if session["user_rank"] < 1:
        #Error not enough rights to see that page
        return jsonify({"error_message" : "No user is logged in"}), 403



    #Add check if amount of user made codes is greater than the max_amount_codes from setting


    user_id = session["user_ID"]

    data = request.json

    qualification_id = data.get("qualification_level")
    max_user_amount = data.get("max_user_amount")
    
    
    #end timestamp current time + 24 hours
    active_hours = 24
    end_timestamp = datetime.datetime.now() + datetime.timedelta(hours=active_hours)
    
    qr_code_id = blueprints.db.add_QRCode_qualification_certificate(qualification_id, user_id, end_timestamp)
    
    
    qr_code = ""
    
    generate = True
    while(generate):
        qr_code = generate_4_digits_code(qr_code_id)
        
        if not blueprints.db.check_if_QRCode_already_exist(qr_code):
            generate = False
        else:
            print("Code already in use")
    
    
    
    blueprints.db.set_qrCode_qualification_certificate_code(qr_code_id, qr_code)
    
    
    
    plain_data = {
        "code": qr_code
    }
    
    return jsonify(plain_data), 200





def generate_4_digits_code(number):
    hash = hashlib.sha256(str(number).encode())
    hash_int = int(hash.hexdigest(), 16)
    base36_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    base36_code = ""
    for _ in range(4):
        base36_code = base36_chars[hash_int % 36] + base36_code
        hash_int //= 36
        
    return base36_code