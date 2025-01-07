class Item:
    def __init__(self, name, price, description, stock, weight):
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock
        self.oos = True if stock <= 0 else False
        self.weight = weight
    
    def __str__(self):
        return f"{self.name} - ${self.price}\n{self.description}\n{self.stock} left" if not self.oos else f"{self.name} - ${self.price}\n{self.description}\nOut of Stock"
    