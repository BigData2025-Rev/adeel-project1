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
        # MAIN MENU OPTIONS
        menu_option = Menu.main_menu()

        if menu_option == 1:
            account = Menu.login()
        elif menu_option == 2:
            account = Menu.register()
        elif menu_option == 0:
            Messages.standard("Have a good day!")
            sys.exit()
        
        admin_select_option = 2

        # IF ADMIN PROMPT FOR WHICH MENU
        if account and account.admin == True:
            admin_select_option = Menu.admin_select_option()
        
        # REGULAR USER MENU
        if account and admin_select_option == 2:
            Messages.standard(f"Welcome {account.first_name} {account.last_name}!")
            while True:
                # ACTUAL STORE MENU
                store_menu_option = Menu.store_menu(account)
                
                if (store_menu_option == 1):
                    while True:
                        category_selected = Menu.product_category_menu()
                        while True:
                            if category_selected == 0:
                                break
                            elif category_selected in [1, 2, 3, 4, 5, 6]:
                                item_selected = Menu.view_product_category_menu(category_selected)
                                carted = Menu.view_item(item_selected, account)
                                if carted:
                                    Messages.success("Item added to cart!")
                                    Messages.pause()
                                else:
                                    break
                            else:
                                Messages.error("Unknown Error. Please try again.")
                                break
                elif (store_menu_option == 2):
                    Menu.view_cart_menu(account)
        elif account and admin_select_option == 1:
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