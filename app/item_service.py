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
        return [Item.from_dict(Item, item) for item in self.db.find({"category": category})]