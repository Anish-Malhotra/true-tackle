import json

from models import Product
from schemas import ProductSchema

ProductSchema = ProductSchema()

# Error handlers are bound to the Flask app
# We need to throw the right exceptions in the 'model' classes, and Flask will handle the rest!

def create(body: dict):
    product_data = Product.create(body)
    return ProductSchema.dump(product_data)

def read_all(page: int, size: int):
    products_data = Product.read_all(page, size)
    return products_data

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