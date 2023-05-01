import json

from models import Order
from schemas import OrderSchema

OrderSchema = OrderSchema()

def create(body: dict):
    order_data = Order.create(body)
    return OrderSchema.dump(order_data)

def read_all(product_id, page, size):
    pass

def get_by_id(order_id: int):
    order_data = Order.get_by_id(order_id)
    return OrderSchema.dump(order_data)

def update(order_id: int, body: dict):
    body_json = json.loads(body.decode("utf-8"))
    order_data = Order.update(order_id, body_json)
    return OrderSchema.dump(order_data)

def delete(order_id):
    order_data = Order.delete(order_id)
    return OrderSchema.dump(order_data)