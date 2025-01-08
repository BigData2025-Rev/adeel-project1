import bcrypt
from models import Account

class AccountService:
    def __init__(self, db):
        self.db = db

    def create_account(self, account):
        self.db.accounts.insert_one(account.to_dict())
        return account

    def validate_email(self, email):
        if self.db.accounts.find_one({"email": email}):
            return True
        return False
    
    def hash_password(self, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')
    
    def login(self, email, password):
        account = self.db.accounts.find_one({"email": email.lower()})
        if account:
            hashed_password = account["password"].encode("utf-8")
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                return Account.from_dict(account)
        return None