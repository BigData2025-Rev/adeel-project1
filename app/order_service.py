from models import Order

class OrderService:
    def __init__(self, db):
        self.db = db
    
    def get_orders(self, account):
        return [Order.from_dict(Order, order) for order in self.db.find({"account": account._id})]
    
    def create_order(self, order):
        self.db.insert_one(order.to_dict())
        return order
    
    def get_one_order(self, order_id):
        return Order.from_dict(Order, self.db.find_one({"_id": order_id}))

    def get_all_orders(self):
        return [Order.from_dict(Order, order) for order in self.db.find()]
    
    def delete_order(self, order):
        self.db.delete_one({"_id": order._id})