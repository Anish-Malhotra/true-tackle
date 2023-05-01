from datetime import date, datetime

from configuration import db
from sqlalchemy import exc
from errors import DataNotFoundException, SqlException, InvalidInputException


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
    
    def json(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'listing_type': self.listing_type,
            'price': self.price,
            'created_at': self.created_at,
            'vendor_id': self.vendor_id
        }
        
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def from_obj(cls, obj) -> "Product":
        product = cls(**obj)
        product.created_at = date.today()
        return product
    
    @classmethod
    def get_by_id(cls, id) -> dict:
        res = cls.query.filter_by(id=id).first()
        if not res:
            raise DataNotFoundException(id=id, resource_type=cls.__tablename__)
        return res.json()
        
    @classmethod
    def create(cls, body: dict) -> dict:
        try:
            res = cls.from_obj(body)
            res.save()
            return res.json()
        except ValueError as e:
            raise InvalidInputException(e, resource_type=cls.__tablename__).with_traceback(exc.__traceback__)
        except exc.SQLAlchemyError as e:
            raise SqlException(e, resource_type=cls.__tablename__)
    
    @classmethod
    def update(cls, id: int, body: dict) -> dict:
        res = cls.query.filter_by(id=id).first()
        if not res:
            raise DataNotFoundException(id=id, resource_type=cls.__tablename__)
        try:
            for key, value in body.items():
                setattr(res, key, value)
            res.save()
            return res.json()
        except ValueError as e:
            raise InvalidInputException(e, resource_type=cls.__tablename__).with_traceback(exc.__traceback__)
        except exc.SQLAlchemyError as e:
            raise SqlException(e, resource_type=cls.__tablename__)
        
    @classmethod
    def delete(cls, id: int) -> dict:
        res = cls.query.filter_by(id=id).first()
        if not res:
            raise DataNotFoundException(id=id, resource_type=cls.__tablename__)
        try:
            db.session.delete(res)
            db.session.commit()
            return res.json()
        except exc.SQLAlchemyError as e:
            raise SqlException(e, resource_type=cls.__tablename__)
    
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

    orders = db.relation('Order', primaryjoin="Order.product_id==Product.id")