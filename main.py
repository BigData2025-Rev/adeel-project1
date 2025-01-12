from app import Menu
import sys
from app import ItemService, AccountService
from models import Item, Account
from database import items, accounts
ItemService = ItemService(items)
from utils import Messages
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
                        if category_selected == 0:
                            break
                        if category_selected in [1, 2, 3, 4, 5, 6]:
                            while True:
                                item_selected = Menu.view_product_category_menu(category_selected)
                                if item_selected == None:
                                    break
                                carted = Menu.view_item(item_selected, account)
                                if carted:
                                    Messages.success("Item added to cart!")
                                    Messages.pause()
                                else:
                                    break
                elif (store_menu_option == 2):
                    while True:
                        user_checkout_option = Menu.view_cart_menu(account)
                        if user_checkout_option == 0:
                            break
                        elif user_checkout_option == 1:
                            success = Menu.checkout(account)
                            if success:
                                Messages.success("Checkout successful!")
                                Messages.pause()
                            break
                        elif user_checkout_option == 2:
                            while True:
                                success = Menu.remove_cart_menu(account)
                                if success:
                                    Messages.success("Item removed from cart!")
                                    Messages.pause()
                                    continue
                                else:
                                    break
                elif (store_menu_option == 3):
                    while True:
                        order_history_select = Menu.view_order_history(account)
                        if order_history_select:
                            Menu.view_order(order_history_select)
                            continue
                        else:
                            break
                elif (store_menu_option == 4):
                    while True:
                        account_menu_select = Menu.account_menu(account)
                        if account_menu_select == 1:
                            while True:
                                account_edit_select = Menu.update_account_menu(account)
                                if account_edit_select == 1:
                                    Menu.update_email(account)
                                elif account_edit_select == 2:
                                    Menu.update_address(account)
                                elif account_edit_select == 3:
                                    Menu.update_city(account)
                                elif account_edit_select == 4:
                                    Menu.update_state(account)
                                elif account_edit_select == 5:
                                    Menu.update_zip(account)
                                else:
                                    break

                        elif account_menu_select == 2:
                            Menu.change_password()
                            continue
                        else:
                            break

                elif (store_menu_option == 0):
                    break

        elif account and admin_select_option == 1:
            while True:
                admin_menu_option = Menu.admin_menu(account)
                if admin_menu_option == 0:
                    break
                elif admin_menu_option == 1:
                    while True:
                        account = Menu.admin_accounts_menu()
                        if account:
                            Menu.admin_view_account(account)
                            continue
                        break
                elif admin_menu_option == 2:
                    while True:
                            order = Menu.admin_orders_menu()
                            if order:
                                Menu.admin_view_order(order)
                                continue
                            break
                elif admin_menu_option == 3:
                    while True:
                            item = Menu.admin_items_menu()
                            if item:
                                Menu.admin_view_item(item)
                                continue
                            break


def test_main():
    item = Item("Laptop", 1000, "A laptop", "Laptops", 10, 5)
    ItemService.create_item(item)
    #print(len(ItemService.get_all_items()))

    #test_account = AccountService.login("test@testing.com", "password")
    #print(test_account)
    items = ItemService.get_all_items()
    #AccountService.add_to_cart(test_account, items[0])
    #print(AccountService.get_cart(test_account))
    #Messages.pause()


if __name__ == "__main__":
    main()