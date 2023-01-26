from flask import Flask, request

app = Flask(__name__)

# dummy db

stores = [
    {
        "name": "HaldiRam",
        "items":[
            {
                "name":"Mixture",
                "price": 20
            }
        ]
    }
]

@app.get('/stores')
def getAllStores():
    return {"stores": stores}

@app.post('/store')
def addAStore():
    request_data = request.get_json()
    storeName = request_data.get('name', None)
    if storeName:
        print(f'Logging Store Name:{storeName}')
        new_store = {"name": storeName, "items":[]}
        stores.append(new_store)
        return new_store, 201
    else:
        return {'message':f'Not able to create store as storeName:{storeName} is not valid'}
    
@app.post('/store/<string:name>/item')
def addItemToExisitngStore(name):
    request_data = request.get_json()
    item_name = request_data.get('name',None)
    price = request_data.get('price', None)
    
    if(item_name and price):
        for store in stores:
            print(f'Logging store name:{store["name"]}')
            if store['name'] == name:
                new_item = {"name":item_name, "price": price}
                store['items'].append(new_item)
                return new_item, 201
            
        return {'message':f'Store with store name:{name} Not Found, please send a valid store name'}, 404
    else:
        return {'message':f'Either the item name:{item_name} or price:{price} is not valid'}, 404
    
@app.get('/store/<string:name>/item')
def getAllItemsFromAParticularStore(name):
        for store in stores:
            if store['name'] == name:
                return {'Items': store['items']}, 200
        return {'message': f'Store with store name:{name} not found'}, 404