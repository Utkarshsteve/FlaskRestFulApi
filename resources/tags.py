from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema, TagAndItemSchema
from models import TagModel, StoreModel, ItemTagsModel, ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

blpTags = Blueprint("tags", __name__, description="Operations on tags")


@blpTags.route('/store/<string:store_id>/tag')
class TagGetAndPost(MethodView):
    @blpTags.response(200, TagSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(
            store_id)  # retrieve store by primary key
        return store.tags.all()

    @blpTags.arguments(TagSchema)
    @blpTags.response(201, TagSchema)
    def post(self, request_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id).first():
            abort(400, message='A tag with that id already exists')
        tag = TagModel(**request_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the store")

        return tag


@blpTags.route('/tags')
class TagGetAllTags(MethodView):
    @blpTags.response(200, TagSchema(many=True))
    def get(self):
        tags = TagModel.query.all()  # retrieve item by primary key
        if tags:
            response = tags
            print(f'There are tags in the db...')
        else:
            response = {
                'message': 'There are no tags in the db. Please try again...'}
        return response


@blpTags.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blpTags.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")
        return tag

    @blpTags.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the tag.")
        return {"message": f"Item removed from tag, item:{item}, tag:{tag}"}


@blpTags.route('/tag/<string:tag_id>')
class TagCreateATag(MethodView):
    @blpTags.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blpTags.response(202,
                      description="Deletes a tag if no item is tagged with it.",
                      example={'message': "Tag Deleted"}
                      )
    @blpTags.alt_response(404, description="Tag not found.")
    @blpTags.alt_response(400, description="Returned if the tags if assigned to one or more items. In this case, the tag is not deleted.")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            try:
                db.session.delete(tag)
                db.session.commit()
                return {'message': 'Tag deleted.'}
            except SQLAlchemyError:
                abort(400, message="An error occurred while deleting the tag.")
