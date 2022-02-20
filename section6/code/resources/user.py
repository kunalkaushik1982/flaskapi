from flask_restful import Resource,reqparse
from models.user import UserModel
import sqlite3 

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str,required=True,help="This field can't be blank.")
    parser.add_argument('password', type=str,required=True,help="This field can't be blank.")
    
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message":"A user with that name already present"},400        
        user = UserModel(**data)
        user.save_to_db()
        
        return {"message":"User created successfully."},201