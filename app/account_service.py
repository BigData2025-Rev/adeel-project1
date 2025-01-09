import bcrypt
from models import Account, Item

class AccountService:
    def __init__(self, db):
        self.db = db

    def create_account(self, account):
        self.db.insert_one(account.to_dict())
        return account

    def get_all_accounts(self):
        return [Account.from_dict(Account, account) for account in self.db.find()]

    def validate_email(self, email):
        if self.db.find_one({"email": email}):
            return True
        return False
    
    def hash_password(self, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')
    
    def login(self, email, password):
        account = self.db.find_one({"email": email.lower()})
        if account:
            hashed_password = account["password"].encode("utf-8")
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                return Account.from_dict(Account, account)
        return None

    def view_all_accounts(self):
        return [Account.from_dict(Account, account) for account in self.db.find()]
    
    def add_to_cart(self, account, item):
        self.db.update_one({"_id": account._id}, {"$push": {"cart": item.to_dict()}})
    
    def remove_from_cart(self, account, item):
        self.db.update_one({"_id": account._id}, {"$pull": {"cart": item.to_dict()}})

    def get_cart(self, account):
        return [Item.from_dict(Item,item) for item in self.db.find_one({"_id": account._id})["cart"]]
    
    def change_password(self, account, password):
        self.db.update_one({"_id": account._id}, {"$set": {"password": self.hash_password(password)}})

    def update_address(self, account, address):
        self.db.update_one({"_id": account._id}, {"$set": {"address": address}})
    
    def update_city(self, account, city):
        self.db.update_one({"_id": account._id}, {"$set": {"city": city}})

    def update_state(self, account, state):
        self.db.update_one({"_id": account._id}, {"$set": {"state": state}})

    def update_zip(self, account, zip):
        self.db.update_one({"_id": account._id}, {"$set": {"zip": zip}})
    
    def update_email(self, account, email):
        self.db.update_one({"_id": account._id}, {"$set": {"email": email}})
    
    def delete_account(self, account):
        self.db.delete_one({"_id": account._id})

    def make_admin(self, account):
        self.db.update_one({"_id": account._id}, {"$set": {"admin": True}})