import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores


blpItems = Blueprint("items", __name__, description="Operations on items")


@blpItems.route('/item/<string:item_id>')
class ItemGetPutAndDelete(MethodView):
    def get(self, item_id):
        try:
            return items.get(item_id)
        except KeyError as e:
            print(f'Keyerror:{e}')
            abort(404, message=f'Item not found')

    def put(self, item_id):
        request_data = request.get_json()
        name = request_data.get('name', None)
        price = request_data.get('price', None)
        if name or price:
            try:
                item = items[item_id]
                item |= request_data
                return item
            except KeyError as e:
                print(f'KeyError:{e}')
                abort(404, message=f"Item with item_id:{item_id} Not Found")
        else:
            abort(
                400, message=f'Bad Request. Either item\'s price:{price} or item\'s name:{name} or both is missing')
            
    def delete(self, item_id):
        try:
            del items[item_id]
            return {'message': f'store with item_id :{item_id} deleted successfully'}
        except KeyError as e:
            print(f'Keyerror:{e}')
            abort(404, message=f'Item with item_id:{item_id} not found')    
            
@blpItems.route('/items')
class ItemGetAllItems(MethodView):
    def get(self):
        return {"items": list(items.values())}
    
@blpItems.route('/item')
class ItemPostCreateAStore(MethodView):
    def post(self):
        request_data = request.get_json()
        item_name = request_data.get('name', None)
        price = request_data.get('price', None)
        store_id = request_data.get('store_id', None)
        payload_validation = item_name and price and store_id

        for item in items.values():
            if (
                item_name == item['name'] and store_id == item['store_id']
            ):
                abort(
                    400, message=f'Item  with name:{item_name} and item_id:{item["id"]} already exists')

        if store_id not in stores:
            abort(404, message=f'Store with store id:{store_id} not found')

        if (payload_validation):
            item_id = uuid.uuid4().hex
            item = {**request_data, "id": item_id}
            items[item_id] = item
            return item, 201
        abort(
            400, message=f'Either the item name:{item_name} or price:{price} is not valid or store with id:{store_id} does not exists')
        
@blpItems.route('/store/<string:store_id>/item')
class ItemGetItemsFromAStore(MethodView):
    def get(self, store_id):
        filtered_items = {k: v for k, v in items.items() if v['store_id'] == str(store_id)}.values()
        if filtered_items:
            item = []
            for i in range(len(filtered_items)):
                res = {
                    'name': list(filtered_items)[i]['name'],
                    'price': list(filtered_items)[i]['price']
                }
                item.append(res)
            return item
        abort(404, message=f'Store with store name:{store_id} not found')