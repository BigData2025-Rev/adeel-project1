from models import Item

class ItemService:
    def __init__(self, db):
        self.db = db
    
    def create_item(self, item):
        self.db.insert_one(item.to_dict())
        return item
    
    def get_all_items(self):
        return [Item.from_dict(Item, item) for item in self.db.find()]
    
    def get_items_by_category(self, category):
        print(category)
        return [Item.from_dict(Item, item) for item in self.db.find({"category": category})]
    
    def delete_item(self, item):
        self.db.delete_one({"_id": item._id})

    def add_stock(self, item, amount):
        if amount < 0:
            return
        self.db.update_one({"_id": item._id}, {"stock": item.stock + amount})

    def remove_stock(self, item, amount):
        if amount > item.stock:
            return
        self.db.update_one({"_id": item._id}, {"stock": item.stock - amount})
