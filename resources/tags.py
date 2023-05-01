from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema
from models import TagModel, StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

blpTags = Blueprint("tags", __name__, description="Operations on tags")

@blpTags.route('/store/<string:store_id>/tag')
class TagGetAndPost(MethodView):
    @blpTags.response(200, TagSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id) # retrieve store by primary key
        return store.tags.all()
    
    @blpTags.arguments(TagSchema)
    @blpTags.response(201, TagSchema)
    def post(self, request_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id).first():
            abort(400, message='A tag with that id already exists')
        tag = TagModel(**request_data, store_id = store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the store")
            
        return tag

    # def delete(self, store_id):
    #     store = TagModel.query.get_or_404(store_id) # retrieve store by primary key
    #     db.session.delete(store)
    #     db.session.commit()
    #     return {'message': f'Store with store id:{store_id} deleted'}
            

@blpTags.route('/tags')
class TagGetAllTags(MethodView):
    @blpTags.response(200, TagSchema(many=True))
    def get(self):
        tags = TagModel.query.all() # retrieve item by primary key
        if tags:
            response = tags
            print(f'There are tags in the db...')
        else:
            response = {'message': 'There are no tags in the db. Please try again...'}
        return response
        
    
@blpTags.route('/tag/<string:tag_id>')
class TagCreateATag(MethodView):
    @blpTags.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag