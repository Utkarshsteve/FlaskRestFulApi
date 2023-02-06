import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema


blpStores = Blueprint("stores", __name__, description="Operations on stores")


@blpStores.route('/store/<string:store_id>')
class StoreGetAndDelete(MethodView):
    @blpStores.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores.get(store_id)
        except KeyError as e:
            print(f'Keyerror:{e}')
            abort(404, message=f'Store not found')

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {'message': f'store with store id:{store_id} successfully'}
        except KeyError as e:
            print(f'Keyerror:{e}')
            abort(404, message=f'Store with store id:{store_id} not found')
            

@blpStores.route('/stores')
class StoreGetAllStores(MethodView):
    @blpStores.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()
    
    
@blpStores.route('/store')
class StoreCreateAnStore(MethodView):
    @blpStores.arguments(StoreSchema)
    @blpStores.response(201, StoreSchema)
    def post(self, request_data):
        storeName = request_data.get('name', None)
        for store in stores.values():
            if storeName == store['name']:
                abort(400, message=f'Store already exists')
        if storeName:
            print(f'Logging Store Name:{storeName}')
            store_id = uuid.uuid4().hex
            new_store = {**request_data, "id": store_id}
            stores[store_id] = new_store
            return new_store
        abort(
        400, message=f'Not able to create store as storeName:{storeName} is not valid')