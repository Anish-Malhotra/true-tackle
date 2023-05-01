from models import Order
from schemas import OrderSchema

OrderSchema = OrderSchema()

def create(body):
    pass

def read_all(product_id, page, size):
    pass

def get_by_id(order_id: int):
    order_data = Order.get_by_id(order_id)
    return OrderSchema.dump(order_data)

def update(order_id, body):
    pass

def delete(order_id):
    pass