import json

from models import Vendor
from schemas import VendorSchema

VendorSchema = VendorSchema()

def create(body: dict):
    vendor_data = Vendor.create(body)
    return VendorSchema.dump(vendor_data)

def read_all(page, size):
    vendors_data = Vendor.read_all(page, size)
    return vendors_data

def get_by_id(vendor_id: int):
    vendor_data = Vendor.get_by_id(vendor_id)
    return VendorSchema.dump(vendor_data)

def update(vendor_id: int, body: dict):
    body_json = json.loads(body.decode("utf-8"))
    vendor_data = Vendor.update(vendor_id, body_json)
    return VendorSchema.dump(vendor_data)

def delete(vendor_id):
    vendor_data = Vendor.delete(vendor_id)
    return VendorSchema.dump(vendor_data)