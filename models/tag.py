from db import db


class TagModel(db.Model):
    __tablename__ = "Tags"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("Stores.id"), nullable=False)
    store = db.relationship("StoreModel", back_populates="tags")