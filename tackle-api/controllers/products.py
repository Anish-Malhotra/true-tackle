import json

from models import Product
from schemas import ProductSchema

ProductSchema = ProductSchema()

def create(body: dict):
    product_data = Product.create(body)
    return ProductSchema.dump(product_data)

def read_all(page, size):
    pass

def get_by_id(product_id: int):
    product_data = Product.get_by_id(product_id)
    return ProductSchema.dump(product_data)

def update(product_id: int, body: dict):
    body_json = json.loads(body.decode("utf-8"))
    product_data = Product.update(product_id, body_json)
    return ProductSchema.dump(product_data)

def delete(product_id):
    product_data = Product.delete(product_id)
    return ProductSchema.dump(product_data)