from flask import Flask
from flask_restful import Api
from resources.sport import Sport

app=Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['PREFERRED_URL_SCHEME']='http'
api=Api(app)

api.add_resource(Sport,'/sportdetails')

if __name__ == "__main__":
    app.run()
