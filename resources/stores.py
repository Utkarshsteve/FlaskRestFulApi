import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blpStores = Blueprint("stores", __name__, description="Operations on stores")


@blpStores.route('/store/<int:store_id>')
class StoreGetAndDelete(MethodView):
    @blpStores.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id) # retrieve store by primary key
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id) # retrieve store by primary key
        db.session.delete(store)
        db.session.commit()
        return {'message': f'Store with store id:{store_id} deleted'}
            

@blpStores.route('/stores')
class StoreGetAllStores(MethodView):
    @blpStores.response(200, StoreSchema(many=True))
    def get(self):
        stores = StoreModel.query.all() # retrieve item by primary key
        if stores:
            response = stores
            print(f'There are stores in the db...')
        else:
            response = {'message': 'There are no stores in the db. Please try again...'}
        return response
        
    
@blpStores.route('/store')
class StoreCreateAnStore(MethodView):
    @blpStores.arguments(StoreSchema)
    @blpStores.response(201, StoreSchema)
    def post(self, request_data):
        store = StoreModel(**request_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the store")
            
        return store