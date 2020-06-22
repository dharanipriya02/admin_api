from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query
class Adminlogin(Resource):#admin login
    parser=reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True,help="Admin username cannot be left blank!")
    parser.add_argument('password',type=str,required=True,help="Password cannot be left blank!")
    
    def post(self):
        data=self.parser.parse_args()
        user=User.getUserById(data['username'])
        if user and safe_str_cmp(user.password,data['password']):
            access_token=create_access_token(identity=user.username,expires_delta=False)
            return {'access_token':access_token},200
        return {"message":"Invalid Credentials!"}, 401
class User():
    def __init__(self,username,password):
        self.username=username
        self.password=password
    @classmethod
    def getUserById(cls,username):
        result=query(f"""select username,password from admin where username='{username}'""",return_json=False)
        if len(result)>0:
            return User(result[0]['username'],result[0]['password'])
        else:
            return None

class Sport(Resource):#sport details
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('sport_name',type=str,required=True,help="sport name cannot be left blank!")
        data=parser.parse_args()

        try:
            return query(f"""SELECT * FROM group10.sports WHERE sport_name='{data['sport_name']}'""")
        except:
            return {"message":"There was an error connecting to sport table."},500
    @jwt_required
    def post(self):#adding sports to sports table
        parser=reqparse.RequestParser()
        parser.add_argument('sport_id',type=int,required=True,help="sport_id cannot be left blank!")
        parser.add_argument('sport_name',type=str,required=True,help="sport_name cannot be left blank!")
        parser.add_argument('sport_category',type=str,required=True,help="sport_category cannot be left blank!")
        parser.add_argument('mini_team_size',type=int,required=True,help="mini_team_size cannot be left blank!")
        parser.add_argument('max_team_size',type=int,required=True,help="max_team_size cannot be left blank!")
        data=parser.parse_args()
        try:
            x=query(f"""SELECT * FROM group10.sports WHERE sport_name='{data['sport_name']}'""",return_json=False)
            if len(x)>0: return {"message":"A sport with that sport name already exists."},400
        except:
            return {"message":"There was an error inserting into sport table."},500
        try:
            query(f"""INSERT INTO group10.sports (sport_id, sport_name, sport_category, mini_team_size, max_team_size) VALUES ({data['sport_id']},
            '{data['sport_name']}','{data['sport_category']}',{data['mini_team_size']},{data['max_team_size']});""")
        except:
            return {"message":"There was an error inserting into sport table."},500
        return {"message":"Successfully Inserted."},201
class Schedule(Resource):#viewing the schedule
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('sport_name',type=str,required=True,help="sport name cannot be left blank!")
        data=parser.parse_args()

        try:
            return query(f"""SELECT * FROM group10.schedule WHERE sport_name='{data['sport_name']}' """)
        except:
            return {"message":"There was an error connecting to sport table."},500
class Modify_schedule(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        #parser.add_argument('sport_name',type=str,required=True,help="sport name cannot be left blank!")
        parser.add_argument('team1_id',type=int,required=True,help="team1_id cannot be left blank!")
        parser.add_argument('team2_id',type=int,required=True,help="team2_id cannot be left blank!")
        parser.add_argument('start_timing',type=str,required=True,help="start_timing cannotstr left blank!")
        parser.add_argument('reporting_time',type=str,required=True,help="reporting_time cannot be left blank!")
        parser.add_argument('match_date',type=str,required=True,help="match_date cannot be left blank!")
        parser.add_argument('match_title',type=str,required=True,help="match_title cannot be left blank!")
        data=parser.parse_args()
        
        try:

            query(f"""update group10.schedule set start_time='{data['start_timing']}',reporting_time='{data['reporting_time']}',match_date='{data['match_date']}',
            match_title='{data['match_title']}' 
            where team1_id={data['team1_id']} and team2_id={data['team2_id']};""",return_json=False)
        except:
            return {"message":"There was an error inserting into schedule table."},500
        return {"message":"Successfully Inserted."},201



class Team_details(Resource):
    @jwt_required
    def get(self):#viewing registered teams
        parser=reqparse.RequestParser()
        parser.add_argument('sport_name',type=str,required=True,help="sport id cannot be left blank!")
        data=parser.parse_args()

        try:
            return query(f"""SELECT * FROM group10.teamdetails WHERE sport_name='{data['sport_name']}'""")
        except:
            return {"message":"There was an error connecting to team_details table."},500
    @jwt_required
    def post(self):#accepting the registration
        parser=reqparse.RequestParser()
        parser.add_argument('team_name',type=str,required=True,help="team name cannot be left blank!")
        data=parser.parse_args()
        try:
            query(f"""update teamdetails set status='accepted' where team_name='{data['team_name']}';""")
        except:
            return {"message":"There was an error inserting into team_details table."},500
        return {"message":"Successfully Inserted."},201
        
class Team_members(Resource):
    @jwt_required
    def get(self):#carrom table (individual team member  details)
        parser=reqparse.RequestParser()
        parser.add_argument('team_name',type=str,required=True,help="team name cannot be left blank!")
        parser.add_argument('sport_name',type=str,required=True,help="sport_name cannot be left blank!")
        data=parser.parse_args()
        #sport={'badminton':  query(f"""SELECT * FROM group10.badminton WHERE team_id={data['team_id']}"""),
         #       'basketball': query(f"""SELECT * FROM group10.basketball WHERE team_id={data['team_id']} """),
         #       'cricket': query(f"""SELECT * FROM group10.cricket WHERE team_id={data['team_id']}"""),
          #      'football': query(f"""SELECT * FROM group10.football WHERE team_id={data['team_id']}"""),
           #     'kabaddi': query(f"""SELECT * FROM group10.kabaddi WHERE team_id={data['team_id']}"""),
            #    'tabble tennis': query(f"""SELECT * FROM group10.table_tennis WHERE team_id={data['team_id']}"""),
             #   'volley ball': query(f"""SELECT * FROM group10.volley_ball WHERE team_id={data['team_id']}"""),
              #  'chess':  query(f"""SELECT * FROM group10.chess WHERE team_id={data['team_id']}"""),
               # 'carroms': query(f"""SELECT * FROM group10.carroms WHERE team_id={data['team_id']} """)
        #}
    
       # return sport[f"""{data['sport name']}"""]
       
        
        #return query(f""" select * from group10.{data['sport name']} WHERE team_id={data['team_id']};""") 
        try:
            return query(f"""SELECT * FROM group10.teamdetails WHERE sport_name='{data['sport_name']}' and team_name='{data['team_name']}'""")
        except:
            return {"message":"There was an error connecting to team_details table."},500
       


        
        
    
   
