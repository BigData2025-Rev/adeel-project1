import datetime
from bson import ObjectId

class Order:
    def __init__(self, account, items, total, shipping, delivery_date, time_placed, _id = None):
        self._id = _id or ObjectId()
        self.account = account
        self.items = items
        self.total = total
        self.shipping = shipping
        self.delivery_date = delivery_date
        self.time_placed = time_placed or datetime.now()().strftime("%m/%d/%Y, %H:%M:%S")
    
    def __str__(self):
        return f"Order {self._id} - ${self.total}\n{self.time_placed}\n{self.delivery_date}" + self.items_str()
    
    def items_str(self):
        return "\n".join([item.short_str() for item in self.items])

    def short_str(self):
        return f"{self._id} - {self.total}"
    
    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(self, cls, data):
        return cls(**data)
    
    def short_str(self):
        return f"Order {self._id} - ${self.total}"