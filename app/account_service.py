import bcrypt
from models import Account, Item

class AccountService:
    def __init__(self, db):
        self.db = db

    def create_account(self, account):
        self.db.insert_one(account.to_dict())
        return account

    def get_all_accounts(self):
        return [Account.from_dict(account) for account in self.db.find()]

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
                return Account.from_dict(account)
        return None

    def view_all_accounts(self):
        return [Account.from_dict(account) for account in self.db.find()]
    
    def add_to_cart(self, account, item):
        response = self.db.update_one({"_id": account._id}, {"$push": {"cart": item.to_dict()}})
        return response.modified_count > 0
    
    def remove_from_cart(self, account, item):
        response = self.db.update_one({"_id": account._id}, {"$pull": {"cart": item.to_dict()}})
        return response.modified_count > 0

    def get_cart(self, account):
        return [Item.from_dict(item) for item in self.db.find_one({"_id": account._id})["cart"]]
    
    def get_cart_dict(self, account):
        return self.db.find_one({"_id": account._id})["cart"]
    
    def change_password(self, account, password):
        response = self.db.update_one({"_id": account._id}, {"$set": {"password": password}})
        return response.modified_count > 0
    
    def update_address(self, account, address):
        response = self.db.update_one({"_id": account._id}, {"$set": {"address": address}})
        return response.modified_count > 0
    
    def update_city(self, account, city):
        response = self.db.update_one({"_id": account._id}, {"$set": {"city": city}})
        return response.modified_count > 0

    def update_state(self, account, state):
        response = self.db.update_one({"_id": account._id}, {"$set": {"state": state}})
        return response.modified_count > 0

    def update_zip(self, account, zip):
        response = self.db.update_one({"_id": account._id}, {"$set": {"zip": zip}})
        return response.modified_count > 0
    
    def delete_account(self, account):
        response = self.db.delete_one({"_id": account._id})
        return response.deleted_count > 0

    def make_admin(self, account):
        response = self.db.update_one({"_id": account._id}, {"$set": {"admin": True}})
        return response.modified_count > 0
    
    def refresh(self, account):
        email = account.email
        account = self.db.find_one({"email": email.lower()})
        return Account.from_dict(account)