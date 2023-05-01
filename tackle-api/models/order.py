from datetime import datetime

from . import BaseModel
from configuration import db


class Order(db.Model, BaseModel):
    __tablename__ = 'order'

    id = db.Column(u'id', db.INTEGER(), primary_key=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    created_at = db.Column(u'created_at', db.DATE(), nullable=False)

    full_name = db.Column(u'full_name', db.VARCHAR(length=128), nullable=False)
    order_date = db.Column(u'order_date', db.DATE(), nullable=False)
    quantity = db.Column(u'quantity', db.INTEGER(), nullable=False)
    
    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return "<Order('%s', '%d', '%d', '%s', '%s')>" % (self.full_name, self.product_id, self.quantity, self.order_date, self.created_at)
    
    def json(self) -> dict:
        return {
            'id': self.id,
            'product_id': self.product_id,
            'full_name': self.full_name,
            'order_date': self.order_date,
            'created_at': self.created_at,
            'quantity': self.quantity,
        }
        
    @classmethod
    def from_obj(cls, obj) -> "Order":
        order = cls(**obj)
        order.order_date = datetime.strptime(order.order_date, "%Y-%m-%d").date()
        return order
        