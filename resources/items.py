import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

blpItems = Blueprint("items", __name__, description="Operations on items")


@blpItems.route('/item/<int:item_id>')
class ItemGetPutAndDelete(MethodView):
    @blpItems.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(
            item_id)  # retrieve item by primary key
        return item

    @blpItems.arguments(ItemUpdateSchema)
    @blpItems.response(200, ItemSchema)
    def put(self, request_data, item_id):
        item = ItemModel.query.get(item_id)  # retrieve item by primary key
        if item:
            item.price = request_data['price']
            item.name = request_data['name']
        else:
            item = ItemModel(id=item_id, **request_data)

        db.session.add(item)
        db.session.commit(item)

        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(
            item_id)  # retrieve item by primary key
        db.session.delete(item)
        db.session.commit()
        return {'message': f'Store with item id:{item_id} deleted'}


@blpItems.route('/items')
class ItemGetAllItems(MethodView):
    @blpItems.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()  # retrieve item by primary key
        if items:
            print(f'There are items in the db...')
        else:
            response = {
                'message': 'There are no items in the db. Please try again...'}
            return response
        return items


@blpItems.route('/item')
class ItemPostCreateAStore(MethodView):
    @blpItems.arguments(ItemSchema)
    @blpItems.response(201, ItemSchema)
    def post(self, request_data):
        # unpacking dictionary into key and value pairs
        item = ItemModel(**request_data)
        print(
            f'Logging the item when trying to psot an item to db...{request_data}')
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item.")

        return item
