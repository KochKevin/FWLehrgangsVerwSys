from flask import Flask

#Api
from blueprints.auth import auth
from blueprints.api.qualifications import get_qualifications
from blueprints.api.get_training_units import get_training_units

#PDF
from blueprints.api.pdf import generate_pdf  #Old
#QR Code
from blueprints.api.QRCode import create_code_data
from blueprints.api.QRCode import update_code_data
from blueprints.api.QRCode import check_for_code
from blueprints.api.QRCode import get_codes
from blueprints.api.QRCode import delete_code
from blueprints.api.QRCode import get_code_creation_settings
#User
from blueprints.api.user import get_user_information
#User - Sessions
from blueprints.api.user_session import set_user_session_as_done
from blueprints.api.user_session import reset_user_session

#Sites
from blueprints.index import index
from blueprints.login import loginPage
from blueprints.signup import signup
from blueprints.dashboard import dashboard
from blueprints.qualification import qualification
from blueprints.qrCode import generate_code
from blueprints.qrCode import scann_code


app = Flask(__name__)

#KEYS:
#https://flask.palletsprojects.com/en/latest/config/#SECRET_KEY
app.secret_key = "0VNw4kBnKFdWOJdxmKsBmA"
#SET ON TRUE IN PRODUCTION
app.config['SESSION_COOKIE_SECURE'] = False


#Api
app.register_blueprint(auth.bp)
app.register_blueprint(get_qualifications.bp)
app.register_blueprint(get_training_units.bp)
app.register_blueprint(set_user_session_as_done.bp)
app.register_blueprint(reset_user_session.bp)
app.register_blueprint(generate_pdf.bp)
app.register_blueprint(create_code_data.bp)
app.register_blueprint(update_code_data.bp)
app.register_blueprint(check_for_code.bp)
app.register_blueprint(get_codes.bp)
app.register_blueprint(get_user_information.bp)
app.register_blueprint(delete_code.bp)
app.register_blueprint(get_code_creation_settings.bp)

#Sites
app.register_blueprint(index.bp)
app.register_blueprint(loginPage.bp)
app.register_blueprint(signup.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(qualification.bp)
app.register_blueprint(generate_code.bp)
app.register_blueprint(scann_code.bp)


if __name__ == "__main__":
    #ssl_context='adhoc' for https | host = "0.0.0.0" to have it public in the network
    app.run(debug=True, ssl_context='adhoc', host = "0.0.0.0")
