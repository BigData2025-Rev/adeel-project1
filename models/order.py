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
    
    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(self, cls, data):
        return cls(**data)