from models import Item

class ItemService:
    def __init__(self, db):
        self.db = db
    
    def create_item(self, item):
        self.db.items.insert_one(item.to_dict())
        return item
    
    def get_all_items(self):
        return [Item.from_dict(item) for item in self.db.items.find()]
    
    def get_item_by_category(self, category):
        return [Item.from_dict(item) for item in self.db.items.find({"category": category})]