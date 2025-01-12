from app import Menu
import sys
from app import ItemService, AccountService
from database import items, accounts
from utils import Messages, logger
AccountService = AccountService(accounts)
ItemService = ItemService(items)
from models import Account

def main():
    
    global account

    while True:
        # MAIN MENU OPTIONS
        logger.info("Start Application")
        menu_option = Menu.main_menu()

        if menu_option == 1:
            account = Menu.login()
        elif menu_option == 2:
            account = Menu.register()
        elif menu_option == 0:
            Messages.standard("Have a good day!")
            logger.info("Ending Application")
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
                                    a = Menu.update_address(account)
                                    if a:
                                        account = a
                                elif account_edit_select == 2:
                                    a = Menu.update_city(account)
                                    if a:
                                        account = a
                                elif account_edit_select == 3:
                                    a = Menu.update_state(account)
                                    if a:
                                        account = a
                                elif account_edit_select == 4:
                                    a = Menu.update_zip(account)
                                    if a:
                                        account = a
                                else:
                                    break
                        elif account_menu_select == 2:
                            Menu.change_password(account)
                            continue
                        else:
                            break

                elif (store_menu_option == 0):
                    break

        elif account and admin_select_option == 1:
            while True:
                admin_menu_option = Menu.admin_menu()
                if admin_menu_option == 0:
                    break
                elif admin_menu_option == 1:
                    while True:
                        acc = Menu.admin_account_menu()
                        if acc is not None:
                            Menu.admin_view_account(acc)
                            continue
                        break
                elif admin_menu_option == 2:
                    while True:
                            order = Menu.admin_orders_menu()
                            if order is not None:
                                Menu.admin_view_order(order)
                                continue
                            break
                elif admin_menu_option == 3:
                    while True:
                            item = Menu.admin_items_menu()
                            if item is not None:
                                Menu.admin_view_item(item)
                                continue
                            break
                elif admin_menu_option == 4:
                    Menu.admin_add_item_menu()

def test_main():
    adminpass = AccountService.hash_password("admin")
    admin = Account("Admin", "Account", "admin@admin.com", adminpass, "123 Admin Street", "Admin", "CA", "90503", "United States", True)
    AccountService.create_account(admin)
if __name__ == "__main__":
    main()