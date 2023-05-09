from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserSchema
from models import UserModel
from passlib.hash import pbkdf2_sha256
from db import db
from sqlalchemy.exc import SQLAlchemyError

blpUsers = Blueprint("Users", "users", description="Operations on users")

@blpUsers.route('/register')
class UserRegistration(MethodView):
    @blpUsers.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data['username']).first():
            abort(409, message = f"A user with the name:{user_data['username']} already exists")
            
        user = UserModel(
            username=user_data['username'],
            password = pbkdf2_sha256.hash(user_data['password'])
        )
        
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while saaving the user to db")
        return {'message':f'User created'}, 201
    
@blpUsers.route('/user/<int:user_id>')
class UserGetAndDelete(MethodView):
    @blpUsers.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the tag.")
        return {"message":"User deleted"}, 200