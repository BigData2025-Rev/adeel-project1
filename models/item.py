from bson import ObjectId

class Item:
    def __init__(self, name, price, description, catagory, stock, weight, oos = None, _id = None):
        self._id = _id or ObjectId()
        self.name = name
        self.price = price
        self.description = description
        self.catagory = catagory
        self.stock = stock
        self.oos = oos or True if stock <= 0 else False
        self.weight = weight
    
    def __str__(self):
        return f"{self.name} - ${self.price}\n{self.catagory}\n{self.description}\n{self.stock} left" if not self.oos else f"{self.name} - ${self.price}\n{self.description}\nOut of Stock"

    def short_str(self):
        return f"{self.name} - ${self.price}"
    
    def add_stock(self, amount):
        self.stock += amount
        self.oos = False if self.stock > 0 else True
    
    def remove_stock(self, amount):
        self.stock -= amount
        self.oos = True if self.stock <= 0 else False
    
    def set_stock(self, amount):
        self.stock = amount
        self.oos = True if self.stock <= 0 else False
    
    def weight_to_shipprice(self):
        return self.weight * 0.1
    
    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(self, cls, data):
        return cls(**data)