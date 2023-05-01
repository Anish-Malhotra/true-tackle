from datetime import datetime

from config import db

class Vendor(db.Model):
    __tablename__ = 'vendor'

    id = db.Column(u'id', db.INTEGER(), primary_key=True, nullable=False)
    created_at = db.Column(u'created_at', db.DATE(), nullable=False)

    name = db.Column(u'name', db.VARCHAR(length=128), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return "<Vendor('%d', '%s')>" % (self.id, self.name)

    products = db.relation('Product', primaryjoin="Product.vendor_id==Vendor.id")