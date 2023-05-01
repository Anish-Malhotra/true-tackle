from configuration import db
from sqlalchemy import exc
from errors import DataNotFoundException, SqlException, InvalidInputException


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
    
    @classmethod
    def read_all(
        cls,
        page: int = 1,
        size: int = 20,
        filter_options: dict = {}
    ) -> dict:
        if len(filter_options.keys()) > 0:
            query = cls.query.filter_by(**filter_options).paginate(page, size, False)
        else:
            query = cls.query.paginate(page, size, False)
        total = query.total
        items = query.items
        return {
            "page": page,
            "page_size": size,
            "total": total,
            "count": len(items),
            "resource_type": cls.__tablename__,
            "resources": [i.json() for i in items],
        }
    