from flask_restful import Resource,reqparse
from db import query

class Sport(Resource):
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('sport_id',type=int,required=True,help="sport id cannot be left blank!")
        data=parser.parse_args()

        try:
            return query(f"""SELECT * FROM group10.sports WHERE sport_id={data['sport_id']}""")
        except:
            return {"message":"There was an error connecting to emp table."},500