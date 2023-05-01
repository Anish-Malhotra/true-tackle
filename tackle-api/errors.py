class DataNotFoundException(RuntimeError):
    def __init__(self, id):
        super().__init__(f"ID '{id}' not found.")
        
class OrderNotFoundException(DataNotFoundException):
    def __init__(self, id):
        super().__init__(id)
        self.resource_type = "Order"
        
class ProductNotFoundException(DataNotFoundException):
    def __init__(self, id):
        super().__init__(id)
        self.resource_type = "Product"
        
class VendorNotFoundException(DataNotFoundException):
    def __init__(self, id):
        super().__init__(id)
        self.resource_type = "Vendor"
        
def not_found_handler(error):
    return {
        "detail": str(error),
        "status": 404,
        "resource_type": error.resource_type,
    }, 404