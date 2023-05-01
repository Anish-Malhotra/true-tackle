from config import ma
from models import Order


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True