from datetime import datetime

from configuration import db
from errors import OrderNotFoundException

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
    
    def json(self):
        return {
            'id':self.id,
            'product_id': self.product_id,
            'full_name': self.full_name,
            'order_date': self.order_date,
            'created_at': self.created_at
        }
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def from_obj(cls, obj) -> "Order":
        return cls(**obj)
    
    @classmethod
    def get_by_id(cls, id) -> dict:
        res = cls.query.filter_by(id=id).first()
        if not res:
            raise OrderNotFoundException(id=id)
        return res.json()
        
    @classmethod
    def create(cls, body: dict) -> dict:
        cls.from_obj(body).save()
        return body
    
    @classmethod
    def update(cls, id: int, body: dict) -> dict:
        res = cls.query.filter_by(id=id).first_or_404()
        cls.from_obj(body).save()
        return body
        
    @classmethod
    def delete(cls, id: int) -> dict:
        res = cls.query.filter_by(id=id).first_or_404()
        db.session.delete(res)
        db.session.commit()
        return res.json()
    
    """
    @classmethod
    def read_all(
        cls,
        page: int = 1,
        size: int = 20,
    ) -> models.PaginatedResponseData:
        query = cls.query.paginate(page, size, False)
        total = query.total
        items = query.items
        return models.PaginatedResponseData(
            page=page,
            size=size,
            total=total,
            count=len(items),
            resources=[i.to_obj() for i in items],
        )
    """
        