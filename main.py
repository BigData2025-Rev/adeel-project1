from app import Menu
from utils import Messages
import sys
from app import ItemService, AccountService
from models import Item, Account
from database import items, accounts
ItemService = ItemService(items)
AccountService = AccountService(accounts)

def main():
    
    while True:
        menu_option = Menu.main_menu()

        if menu_option == 1:
            account = Menu.login()
        elif menu_option == 2:
            account = Menu.register()
        elif menu_option == 0:
            Messages.standard("Have a good day!")
            sys.exit()

        if account and account.admin == False:
            Messages.standard(f"Welcome {account.first_name} {account.last_name}!")
            while True:
                store_menu_option = Menu.store_menu(account)
                
                if (store_menu_option == 1):
                    category_menu_option = Menu.product_category_menu()
                    
                elif (store_menu_option == 2):
                    Menu.view_cart_menu(account)
        elif account and account.admin == True:
            while True:
                admin_menu_option = Menu.admin_menu(account)

def test_main():
    #item = Item("Laptop", 1000, "A laptop", "Laptops", 10, 5)
    #ItemService.create_item(item)
    #print(len(ItemService.get_all_items()))

    test_account = AccountService.login("test@testing.com", "password")
    print(test_account)
    items = ItemService.get_all_items()
    #AccountService.add_to_cart(test_account, items[0])
    print(AccountService.get_cart(test_account))
    Messages.pause()


if __name__ == "__main__":
    test_main()