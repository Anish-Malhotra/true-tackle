from datetime import datetime

from config import db

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(u'id', db.INTEGER(), primary_key=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    created_at = db.Column(u'created_at', db.DATE(), nullable=False)

    full_name = db.Column(u'full_name', db.VARCHAR(length=128), nullable=False)
    order_date = db.Column(u'order_date', db.DATE(), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return "<Order('%d', '%s')>" % (self.id, self.full_name)