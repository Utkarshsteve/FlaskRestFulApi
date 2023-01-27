import uuid
from flask import Flask, request
from db import items, stores

app = Flask(__name__)


@app.get('/stores')
def getAllStores():
    return {"stores": list(stores.values())}

    
@app.get('/items')
def getAllItems():
    return {"items": list(items.values())}

@app.post('/store')
def addAStore():
    request_data = request.get_json()
    storeName = request_data.get('name', None)
    if storeName:
        print(f'Logging Store Name:{storeName}')
        store_id = uuid.uuid4().hex
        new_store = {**request_data, "id": store_id}
        stores[store_id] = new_store
        return new_store, 201
    else:
        return {'message':f'Not able to create store as storeName:{storeName} is not valid'}
    
@app.post('/item')
def addItemToExisitngStore():
    request_data = request.get_json()
    item_name = request_data.get('name',None)
    price = request_data.get('price', None)
    store_id = request_data.get('store_id', None)
    payload_validation = item_name and price and store_id
    if(payload_validation and store_id in stores):
        item_id = uuid.uuid4().hex
        item = {**request_data, "id":item_id}
        items[item_id] = item
        return item, 201
    else:
        return {'message':f'Either the item name:{item_name} or price:{price} is not valid or store with id:{store_id} does not exists'}, 404
    
@app.get('/store/<string:store_id>/item')
#TODO: improve this
def getAllItemsFromAParticularStore(store_id):
    #use list comprehension
    filtered_items = {k:v for k,v in items.items() if v['store_id'] == str(store_id)}.values()
    if filtered_items:
        item = []
        for i in range (len(filtered_items)):
            res = {
                'name': list(filtered_items)[i]['name'],
                'price': list(filtered_items)[i]['price']
                }
            item.append(res)
        return item
    return {'message': f'Store with store name:{store_id} not found'}, 404
    
@app.get('/store/<string:store_id>')
def getAParticularStore(store_id):
    try:
        return stores.get[store_id]
    except KeyError as e:
        print(f'Keyerror:{e}')
        return {'message':f'Store not found'}, 404
    
@app.get('/item/<string:item_id>')
def getAParticularItem(item_id):
    try:
        return items.get[item_id]
    except KeyError as e:
        print(f'Keyerror:{e}')
        return {'message':f'Item not found'}, 404