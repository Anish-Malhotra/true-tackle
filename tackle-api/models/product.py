from datetime import datetime

from . import BaseModel
from configuration import db


class Product(db.Model, BaseModel):
    __tablename__ = 'product'

    id = db.Column(u'id', db.INTEGER(), primary_key=True, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendor.id"), nullable=False)
    created_at = db.Column(u'created_at', db.DATE(), nullable=False)

    title = db.Column(u'title', db.VARCHAR(length=128), nullable=False)
    listing_type = db.Column(u'listing_type', db.Enum(u'saas', u'ami'), default=u'saas', nullable=False)
    price = db.Column(u'price', db.INTEGER(), nullable=False)
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return "<Product('%d', '%s')>" % (self.id, self.title)
    
    def json(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'listing_type': self.listing_type,
            'price': self.price,
            'created_at': self.created_at,
            'vendor_id': self.vendor_id
        }
        
    @classmethod
    def from_obj(cls, obj) -> "Product":
        product = cls(**obj)
        return product

    orders = db.relation('Order', primaryjoin="Order.product_id==Product.id")