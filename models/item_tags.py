from db import db

class ItemTagsModel(db.Model):
    __tablename__ = "Item_Tags"
    
    id = db.Column(db.Integer, primary_key = True)
    item_id = db.Column(db.Integer, db.ForeignKey("Items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("Tags.id"))