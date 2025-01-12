import datetime
from bson import ObjectId
from models import Item

class Order:
    def __init__(self, account, items, subtotal, total, shipping, delivery_date, time_placed, _id = None):
        self._id = _id or ObjectId()
        self.account = account
        self.items = items
        self.subtotal = subtotal
        self.total = total
        self.shipping = shipping
        self.delivery_date = delivery_date
        self.time_placed = time_placed or datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    
    def __str__(self):
        subtotal = self.total - self.shipping
        formatted_items = self.items_str()
        return (
            f"Order Summary\n"
            f"==============\n"
            f"Order ID: {self._id}\n"
            f"Subtotal: ${subtotal:.2f}\n"
            f"Shipping: ${self.shipping:.2f}\n"
            f"Total:    ${self.total:.2f}\n"
            f"Time Placed: {self.time_placed}\n"
            f"Delivery Date: {self.delivery_date}\n"
            f"Items:\n{formatted_items if formatted_items else 'No items in this order'}\n"
            )

    def items_str(self):
        return "\n".join([
            Item.from_dict(item).short_str() if isinstance(item, dict) else item.short_str()
            for item in self.items
        ])

    def short_str(self):
        return f"{self._id} - ${self.total}"
    
    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    