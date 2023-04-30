from datetime import datetime
from dateutil.relativedelta import relativedelta

from config import db
from models import Vendor, Product, Order


def build_or_refresh_db():
    db.drop_all()
    db.create_all()
    load_db()
    print("data refreshed!")

def load_db():
    tackle = Vendor(name='Tackle.io')
    db.session.add(tackle)
    db.session.flush()

    ami_listing = Product(title="Tackle Amazon Machine Image", listing_type="ami", price=1000, vendor_id=tackle.id)
    govcloud_listing = Product(title="Tackle for GovCloud", listing_type="saas", price=5000, vendor_id=tackle.id)
    
    db.session.add(ami_listing)
    db.session.add(govcloud_listing)
    db.session.flush()

    orders = []
    orders.append(Order(full_name="Linus Torvalds", order_date=datetime.now() - relativedelta(months=1), quantity=1, product_id=ami_listing.id))
    orders.append(Order(full_name="Elon Musk", order_date=datetime.now() - relativedelta(months=1), quantity=2, product_id=ami_listing.id))
    orders.append(Order(full_name="Alan Turing", order_date=datetime.now() - relativedelta(months=4), quantity=4, product_id=ami_listing.id))
    orders.append(Order(full_name="Katherine Johnson", order_date=datetime.now() - relativedelta(months=4), quantity=1, product_id=ami_listing.id))
    orders.append(Order(full_name="Margaret Hamilton", order_date=datetime.now() - relativedelta(months=3), quantity=1, product_id=govcloud_listing.id))
    orders.append(Order(full_name="Grace Hopper", order_date=datetime.now() - relativedelta(months=6), quantity=3, product_id=govcloud_listing.id))

    for order in orders:
        db.session.add(order)

    db.session.commit()
