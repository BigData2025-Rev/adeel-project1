from app import Menu
import sys
from app import ItemService, AccountService
from models import Item, Account
from database import items, accounts
ItemService = ItemService(items)
from utils import Messages, logger
AccountService = AccountService(accounts)

account = None

def main():
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
                                    a = Menu.update_email(account)
                                    if a:
                                        account = a
                                elif account_edit_select == 2:
                                    a = Menu.update_address(account)
                                    if a:
                                        account = a
                                elif account_edit_select == 3:
                                    a = Menu.update_city(account)
                                    if a:
                                        account = a
                                elif account_edit_select == 4:
                                    a = Menu.update_state(account)
                                    if a:
                                        account = a
                                elif account_edit_select == 5:
                                    a = Menu.update_zip(account)
                                    if a:
                                        account = a
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

import random

def test_main():


    items = [
        # Laptops
        Item("Basic Laptop", 600, "All you need to get started", "Laptops", random.randint(5, 100), 10),
        Item("Standard Laptop", 800, "A reliable laptop for daily use", "Laptops", random.randint(5, 100), 10),
        Item("Advanced Laptop", 1000, "Powerful performance for professionals", "Laptops", random.randint(5, 100), 10),
        Item("Gaming Laptop", 1500, "High performance for gaming enthusiasts", "Laptops", random.randint(5, 100), 10),
        Item("Ultra Laptop", 2000, "Top-notch specs for demanding users", "Laptops", random.randint(5, 100), 10),
        
        # Phones
        Item("Basic Phone", 300, "Entry-level smartphone with essential features", "Phones", random.randint(5, 100), 1),
        Item("Standard Phone", 500, "Mid-range smartphone with great performance", "Phones", random.randint(5, 100), 1),
        Item("Pro Phone", 800, "High-end smartphone with advanced features", "Phones", random.randint(5, 100), 1),
        Item("Ultra Phone", 1200, "Flagship phone with cutting-edge technology", "Phones", random.randint(5, 100), 1),
        Item("Luxury Phone", 1500, "Premium smartphone with luxury design", "Phones", random.randint(5, 100), 1),
        
        # Watches
        Item("Basic Watch", 50, "Simple and stylish analog watch", "Watches", random.randint(5, 100), 0.5),
        Item("Smart Watch", 150, "Track your fitness and stay connected", "Watches", random.randint(5, 100), 0.5),
        Item("Luxury Watch", 500, "Elegant watch with premium craftsmanship", "Watches", random.randint(5, 100), 0.5),
        
        # Headphones
        Item("Basic Headphones", 30, "Affordable headphones with decent sound quality", "Headphones", random.randint(5, 100), 0.8),
        Item("Wireless Headphones", 100, "Convenient wireless headphones with great sound", "Headphones", random.randint(5, 100), 0.8),
        Item("Noise Cancelling Headphones", 250, "Block out noise with premium sound quality", "Headphones", random.randint(5, 100), 0.8),
        
        # Accessories
        Item("Phone Case", 15, "Protect your phone with this durable case", "Accessories", random.randint(5, 100), 0.3),
        Item("Laptop Sleeve", 25, "Protective sleeve for laptops", "Accessories", random.randint(5, 100), 0.5),
        Item("Wireless Mouse", 20, "Portable and ergonomic wireless mouse", "Accessories", random.randint(5, 100), 0.4),
        Item("External Hard Drive", 80, "Store and back up your data securely", "Accessories", random.randint(5, 100), 1),
        Item("USB-C Hub", 40, "Expand your laptop’s connectivity options", "Accessories", random.randint(5, 100), 0.6),
        Item("Keyboard", 30, "Comfortable and reliable keyboard", "Accessories", random.randint(5, 100), 0.7),
        Item("Headphone Stand", 20, "Keep your headphones organized", "Accessories", random.randint(5, 100), 0.5),
        Item("Portable Charger", 50, "Charge your devices on the go", "Accessories", random.randint(5, 100), 0.9),
        Item("Stylus Pen", 25, "Enhance your touchscreen experience", "Accessories", random.randint(5, 100), 0.2),
        Item("Screen Protector", 10, "Protect your screen from scratches", "Accessories", random.randint(5, 100), 0.1),
    ]


    for item in items:
        item = ItemService.create_item(item)
        print(item)



if __name__ == "__main__":
    main()