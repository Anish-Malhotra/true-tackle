from config import ma
from models import Vendor


class VendorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor
        load_instance = True