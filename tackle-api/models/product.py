from datetime import datetime

from config import db

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(u'id', db.INTEGER(), primary_key=True, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendor.id"), nullable=False)
    created_at = db.Column(u'created_at', db.DATE(), nullable=False)

    title = db.Column(u'title', db.VARCHAR(length=128), nullable=False)
    listing_type = db.Column(u'listing_type', db.Enum(u'saas', u'ami'), default=u'saas', nullable=False)
    price = db.Column(u'price', db.INTEGER(), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return "<Product('%d', '%s')>" % (self.id, self.title)

    orders = db.relation('Order', primaryjoin="Order.product_id==Product.id")