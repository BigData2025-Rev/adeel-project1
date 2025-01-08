from bson import ObjectId

class Account:
    def __init__(self, first_name, last_name, email, password, address, city, state, zip, country = "United States", admin = False, _id = None, cart = []):
        self._id = _id or ObjectId()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country
        self.admin = admin
        self.cart = cart
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}\n{self.address}\n{self.city}, {self.state} {self.zip}\nADMIN ACCOUNT" if self.admin else f"{self.first_name} {self.last_name} - {self.email}\n{self.address}\n{self.city}, {self.state} {self.zip}\nPoints: {self.points}"
    
    def add_to_cart(self, item):
        self.cart.append(item)
    
    def remove_from_cart(self, item):
        self.cart.remove(item)
    
    def clear_cart(self):
        self.cart = []
    
    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(self, cls, data):
        return cls(**data)
