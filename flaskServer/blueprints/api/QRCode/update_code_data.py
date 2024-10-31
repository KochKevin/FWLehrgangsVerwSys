#Modfy entrie in db

from flask import Blueprint, session,request, jsonify
import blueprints.db

bp = Blueprint("update_qr_code_data", __name__, static_folder="static", template_folder="templates")

@bp.route("/api/v1/update-qr-code-data", methods=["POST"]) 
def create_qr_code():
    return