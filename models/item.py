from bson import ObjectId

class Item:
    def __init__(self, name, price, description, category, stock, weight, _id = None):
        self._id = _id or ObjectId()
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.stock = stock
        self.weight = weight

    def __str__(self):
        stock_status = f"{self.stock} left" if self.stock > 0 else "Out of Stock"
        return (
            f"Item: {self.name}\n"
            f"Price: ${self.price:.2f}\n"
            f"Description: {self.description}\n"
            f"Category: {self.category}\n"
            f"Stock: {stock_status}\n"
        )

    def short_str(self):
        return f"{self.name} - ${self.price}"
    
    def add_stock(self, amount):
        self.stock += amount
    
    def remove_stock(self, amount):
        self.stock -= amount
    
    def set_stock(self, amount):
        self.stock = amount
    
    def weight_to_shipprice(self):
        return self.weight * 0.1
    
    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)