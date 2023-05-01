from datetime import datetime

from . import BaseModel
from configuration import db


class Vendor(db.Model, BaseModel):
    __tablename__ = 'vendor'

    id = db.Column(u'id', db.INTEGER(), primary_key=True, nullable=False)
    created_at = db.Column(u'created_at', db.DATE(), nullable=False)

    name = db.Column(u'name', db.VARCHAR(length=128), nullable=False)
    
    def __init__(self, **kwargs):
        super(Vendor, self).__init__(**kwargs)
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return "<Vendor('%d', '%s')>" % (self.id, self.name)
    
    def json(self) -> dict:
        return {
            'id': self.id,
            'created_at': self.created_at,
            'name': self.name,
        }
        
    @classmethod
    def from_obj(cls, obj) -> object:
        vendor = cls(**obj)
        return vendor

    products = db.relation('Product', primaryjoin="Product.vendor_id==Vendor.id")