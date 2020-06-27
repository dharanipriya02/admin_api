from flask import Flask,jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.admin import Adminlogin,Sport,Schedule,Team_details,Team_members,Modify_schedule,Add_schedule,Add_dates,Sport_category


app=Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['JWT_SECRET_KEY']='group10'
app.config['PREFERRED_URL_SCHEME']='http'
api=Api(app)
jwt=JWTManager(app)
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'authorization_required',
        "description": "Request does not contain an access token."
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'invalid_token',
        'message': 'Signature verification failed.'
    }), 401
api.add_resource(Adminlogin,'/Adminlogin')
api.add_resource(Sport,'/sportdetails')
api.add_resource(Schedule,'/schedule')
api.add_resource(Modify_schedule,'/Modify_schedule')
api.add_resource(Team_details,'/team_details')
api.add_resource(Team_members,'/team_members')
api.add_resource(Add_schedule,'/add_schedule')
api.add_resource(Add_dates,'/add_dates')

api.add_resource(Sport_category,'/sport_category')




if __name__ == "__main__":
    app.run(debug=True)
