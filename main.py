from models import Account

def main():
    #(self, first_name, last_name, email, password, address, city, state, zip, points = 100, admin = False, _id = None)
    newAcc = Account("Test", "Account", "test@test.com", "password", "123 Test St", "Test City", "TX", "12345")
    print(newAcc)
    dictAcc = newAcc.to_dict()
    print(dictAcc)
    print(Account.from_dict(Account, dictAcc))

if __name__ == "__main__":
    main()