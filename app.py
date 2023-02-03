import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


########################################### Store Endpoints ###########################################

@app.get('/stores')
def getAllStores():
    return {"stores": list(stores.values())}


@app.get('/store/<string:store_id>')
def getAParticularStore(store_id):
    try:
        return stores.get(store_id)
    except KeyError as e:
        print(f'Keyerror:{e}')
        abort(404, message=f'Store not found')


@app.post('/store')
def addAStore():
    request_data = request.get_json()
    storeName = request_data.get('name', None)
    for store in stores.values():
        if storeName == store['name']:
            abort(400, message=f'Store already exists')
    if storeName:
        print(f'Logging Store Name:{storeName}')
        store_id = uuid.uuid4().hex
        new_store = {**request_data, "id": store_id}
        stores[store_id] = new_store
        return new_store, 201
    abort(
        400, message=f'Not able to create store as storeName:{storeName} is not valid')


@app.delete('/store/<string:store_id>')
def deleteAParticularStore(store_id):
    try:
        del stores[store_id]
        return {'message': f'store with store id:{store_id} successfully'}
    except KeyError as e:
        print(f'Keyerror:{e}')
        abort(404, message=f'Store with store id:{store_id} not found')


########################################### Item Endpoints ###########################################
@app.get('/items')
def getAllItems():
    return {"items": list(items.values())}


@app.get('/item/<string:item_id>')
def getAParticularItem(item_id):
    try:
        return items.get(item_id)
    except KeyError as e:
        print(f'Keyerror:{e}')
        abort(404, message=f'Item not found')


@app.get('/store/<string:store_id>/item')
def getAllItemsFromAParticularStore(store_id):
    # use list comprehension
    filtered_items = {k: v for k, v in items.items(
    ) if v['store_id'] == str(store_id)}.values()
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


@app.post('/item')
def addItemToExisitngStore():
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


@app.put('/item/<string:item_id>')
def updateAnExisitngItem(item_id):
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


@app.delete('/item/<string:item_id>')
def deleteAParticularItem(item_id):
    try:
        del items[item_id]
        return {'message': f'store with item_id :{item_id} deleted successfully'}
    except KeyError as e:
        print(f'Keyerror:{e}')
        abort(404, message=f'Item with item_id:{item_id} not found')
