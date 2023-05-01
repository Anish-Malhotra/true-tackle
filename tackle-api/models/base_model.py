from configuration import db
from sqlalchemy import exc
from errors import DataNotFoundException, SqlException, InvalidInputException

"""
Base class for all SQLAlchemy DAO classes

Although SQLAlchemy doesn't support inheritance (requiring a valid table name when inherting from db.Model),
all of the CRUD operations are implemented in this base class as a way to reuse code

The actual DAO classes inherit from both BaseModel and db.Model, since they are 1:1 with database tables
"""
class BaseModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()
        
    def json(self) -> dict:
        raise NotImplementedError
        
    @classmethod
    def from_obj(cls, obj) -> object:
        raise NotImplementedError
    
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
            raise InvalidInputException(e, resource_type=cls.__tablename__).with_traceback(e.__traceback__)
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
            raise InvalidInputException(e, resource_type=cls.__tablename__).with_traceback(e.__traceback__)
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
    
    @classmethod
    def read_all(
        cls,
        page: int,
        size: int,
        filter_options: dict = {}
    ) -> dict:
        if len(filter_options.keys()) > 0:
            query = cls.query.filter_by(**filter_options).paginate(page=page, per_page=size, error_out=False)
        else:
            query = cls.query.paginate(page=page, per_page=size, error_out=False)
        total = query.total
        items = query.items
        
        page_data = {
            "count": total,
            "data": [i.json() for i in items]
        }
        
        if page * size < total:
            page_data["next_id"] = page + 1
        if page > 1:
            page_data["prev_id"] = page - 1
        
        return page_data
    