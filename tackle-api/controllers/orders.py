import json

from models import Order
from schemas import OrderSchema

OrderSchema = OrderSchema()

# Error handlers are bound to the Flask app
# We need to throw the right exceptions in the 'model' classes, and Flask will handle the rest!

def create(body: dict):
    order_data = Order.create(body)
    return OrderSchema.dump(order_data)

def read_all(page, size, product_id = None):
    filter_options = {}
    if product_id:
        filter_options["product_id"] = product_id
    
    orders_data = Order.read_all(page, size, filter_options)
    return orders_data

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

def revenue():
    revenue_data = Order.get_total_revenue()
    return {"amount": revenue_data}