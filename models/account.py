class Account:
    def __init__(self, id, name, email, address, city, state, zip, points = 100, admin = False):
        self.id = id
        self.name = name
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.country = "United States"
        self.points = points
        self.admin = admin
        self.cart = []
    
    def __str__(self):
        return f"{self.name} - {self.email}\n{self.address}\n{self.city}, {self.state} {self.zip}\nADMIN ACCOUNT" if self.admin else f"{self.name} - {self.email}\n{self.address}\n{self.city}, {self.state} {self.zip}\nPoints: {self.points}"