from utils import Messages, logger
from database import accounts, items, orders
from app.account_service import AccountService
from app.item_service import ItemService
from app.order_service import OrderService
from models import Account, Item, Order
import getpass
import os
from datetime import datetime, timedelta

ItemService = ItemService(items)
AccountService = AccountService(accounts)
OrderService = OrderService(orders)

INVALID_OPTION = "Invalid option! Please try again...\n"
PASS_DO_NOT_MATCH = "Passwords do not match! Please try again...\n"
PASSWORD_ERROR = "Too many failed attemps, please try again later...\n"
PASSWORD_CHANGE_ERROR = "Password change failed! Please try again...\n"
STATE_ERROR = "Please enter a valid two character state abbreviation\n"
EMAIL_TAKEN = "Email already in use! Please login instead\n"
ACCOUNT_UPDATED = "Successfully updated account!\n"
BLANK_ENTRY = "Entry cannot be blank, please try again...\n"
INVALID_INPUT = "Invalid input, please try again..."

category = ["Laptops", "Phones", "Watches", "Headphones", "Accessories", "All Products"]

state_abbreviations = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

def get_valid_password() -> str:
    retry_attempts = 3
    password = ""
    while retry_attempts >= 0:
        password = getpass.getpass("Password: ")
        confirm_password = getpass.getpass("Confirm Password: ")
        if password != confirm_password:
            Messages.error(PASS_DO_NOT_MATCH)
            retry_attempts -= 1
            Messages.error("You have " + str(retry_attempts) + " attempts left")
            continue
        break
    
    if retry_attempts < 0:
        Messages.error(PASSWORD_ERROR)
        return None

    return password

def get_valid_state() -> str:
    retry_attempts = 3
    state = ""
    while retry_attempts >= 0:
        state = input("State: ")
        if state.upper() not in state_abbreviations:
            Messages.error(STATE_ERROR)
            retry_attempts -= 1
            Messages.error("You have " + str(retry_attempts) + " attempts left")
            continue
        break
    
    if retry_attempts < 0:
        Messages.error(PASSWORD_ERROR)
        return None
    
    return state.upper()

def clear_console():
    os.system("cls")

class Menu:

# MAIN MENU

    def main_menu() -> int:
        clear_console()
        while True:
            Messages.title("TECH STORE")
            Messages.menu_option(1, "Login")
            Messages.menu_option(2, "Register")
            Messages.menu_option(0, "Exit")

            try:
                user_input = int(input("Enter selection: "))

            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue

            if user_input not in [1, 2, 0]:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue

            return user_input

# AUTHENTACTION MENUS

    def login() -> str:
        retry_attemps = 3
        clear_console()
        while retry_attemps >= 0:
            Messages.title("LOGIN")
            Messages.standard("Please enter your information below")

            email = input("Email: ")
            password = getpass.getpass("Password: ")
            account = AccountService.login(email, password)
            if account is None:
                clear_console()
                Messages.error("Invalid email or password! Please try again...\n\n")
                retry_attemps -= 1
                Messages.error("You have " + str(retry_attemps) + " attempts left")
                continue
            Messages.success("Logged in successfully!")
            logger.info(f"Logged in [{account.email}]")
            Messages.pause()
            return account
        if retry_attemps < 0:
            Messages.error("Unable to login, please try again later")
            logger.info("Failed log-in attempt")
            Messages.pause()


    def register() -> str:
        clear_console()
        while True:
            Messages.title("REGISTER")
            Messages.standard("Please enter your information below")

            first_name = input("First Name: ")

            if not first_name:
                clear_console()
                Messages.error(BLANK_ENTRY)
                continue

            last_name = input("Last Name: ")
            if not last_name:
                clear_console()
                Messages.error(BLANK_ENTRY)
                continue

            email = input("Email: ").lower()

            if not email:
                clear_console()
                Messages.error(BLANK_ENTRY)
                continue
            if AccountService.validate_email(email):
                Messages.error(EMAIL_TAKEN)
                return None

            password = get_valid_password()
            if password is None:
                break
            password = AccountService.hash_password(password)
            
            address = input("Street Address: ")

            if not address:
                clear_console()
                Messages.error(BLANK_ENTRY)
                continue

            city = input("City: ")
            if not city:
                clear_console()
                Messages.error(BLANK_ENTRY)
                continue

            state = get_valid_state()
            if state is None:
                return None
            
            zip = input("Zip Code: ")
            
            newAccount = Account(first_name.title(), last_name.title(), email, password, address, city.title(), state, zip)
            if AccountService.create_account(newAccount):
                Messages.success("Account created successfully!")
                logger.info(f"New user [{newAccount.email}]")
                Messages.pause()
                return newAccount
            return None

    # ADMIN MENUS

    def admin_select_option():
        clear_console()
        while True:
            Messages.title("ADMIN SELECT")
            Messages.standard("Would you like to view the admin or user menu?")
            Messages.menu_option(1, "Admin")
            Messages.menu_option(2, "User")
            Messages.menu_option(0, "Exit")
            try:
                user_input = int(input("Enter selection: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input not in [1, 2, 0]:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return user_input

    def admin_menu():
        clear_console()
        while True:
            Messages.title("ADMIN")
            Messages.menu_option(1, "Accounts")
            Messages.menu_option(2, "Orders")
            Messages.menu_option(3, "Items")
            Messages.menu_option(4, "Add Item")
            Messages.menu_option(0, "Return to Main Menu")
            try:
                user_input = int(input("Enter selection: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input not in [1, 2, 3, 4, 0]:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return user_input

    def admin_account_menu():
        clear_console()
        while True:
            Messages.title("ACCOUNTS")
            accounts = AccountService.get_all_accounts()
            if not accounts:
                Messages.standard("No accounts found")
                Messages.pause()
                break
            for index, account in enumerate(accounts):
                Messages.menu_option(index + 1, account.short_str())
            Messages.menu_option(0, "Return to Menu")
            try:
                user_input = int(input("Enter selection: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input not in range(len(accounts) + 1):
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return None if user_input == 0 else accounts[user_input - 1]

    def admin_view_account(account):
        clear_console()
        Messages.title(account.email)
        print(account)
        Messages.menu_option(1, "Delete Account")
        if not account.admin:
            Messages.menu_option(2, "Make Admin")
        Messages.menu_option(0, "Return to Accounts")
        try:
            user_input = int(input("Enter selection: "))
        except ValueError:
            clear_console()
            Messages.error(INVALID_OPTION)
            return
        if user_input not in [0, 1, 2]:
            clear_console()
            Messages.error(INVALID_OPTION)
        if user_input == 1:
            confirm = input("Are you sure you want to delete this account? (Y/N): ")
            if confirm.lower() in ["ye", "y", "yes"]:
                if account.admin == True:
                    Messages.error("Cannot delete admin account!")
                    Messages.pause()
                    return
                else:
                    AccountService.delete_account(account)
                    Messages.success("Successfully deleted account")
                    Messages.pause()
        if user_input == 2:
            if account.admin == True:
                return
            else:
                confirm = input("Are you sure you want to make this user an admin? (Y/N): ")
                if confirm.lower() in ["ye", "y", "yes"]:
                    AccountService.make_admin(account)
                    Messages.success("Made user admin!")
        return

    def admin_items_menu():
        clear_console()
        while True:
            Messages.title("ITEMS")
            items = ItemService.get_all_items()
            if not items:
                Messages.standard("No items found")
                Messages.pause()
                break
            for index, item in enumerate(items):
                Messages.menu_option(index + 1, item.short_str())
            Messages.menu_option(0, "Return to Menu")
            try:
                user_input = int(input("Enter selection: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input not in range(len(items) + 1):
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return None if user_input == 0 else items[user_input - 1]

    def admin_view_item(item):
        clear_console()
        Messages.title(item.name)
        print(item)
        Messages.menu_option(1, "Delete Item")
        Messages.menu_option(2, "Add Stock")
        Messages.menu_option(3, "Remove Stock")
        Messages.menu_option(0, "Return to Items")
        try:
            user_input = int(input("Enter selection: "))
        except ValueError:
            clear_console()
            Messages.error(INVALID_OPTION)
            return
        if user_input not in [0, 1, 2, 3]:
            clear_console()
            Messages.error(INVALID_OPTION)
        if user_input == 1:
            confirm = input("Are you sure you want to delete this item? (Y/N): ")
            if confirm.lower() in ["ye", "y", "yes"]:
                ItemService.delete_item(item)
                Messages.success("Successfully deleted item")
                Messages.pause()
        elif user_input == 2:
            try:
                amount = int(input("How much stock would you like to add? "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_INPUT)
                return
            if amount <= 0:
                Messages.error("Cannot add less than 1")
                Messages.pause()
                return
            ItemService.add_stock(item, amount)
            Messages.success(f"Added {amount} from {item.name}.")
            Messages.pause()
        elif user_input == 3:
            try:
                amount = int(input("How much stock would you like to remove? "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_INPUT)
                return
            if amount > item.stock:
                Messages.error(f"Cannot remove more than {item.stock}")
                Messages.pause()
                return
            ItemService.remove_stock(item, amount)
            Messages.success(f"Removed {amount} from {item.name}.")
            Messages.pause()
        return
    
    def admin_add_item_menu():
        clear_console()
        while True:
            Messages.title("ADD ITEM")

            name = input("Item Name: ")
            if not name:
                clear_console()
                Messages.error(BLANK_ENTRY)
                continue

            description = input("Description: ")
            if not description:
                clear_console()
                Messages.error(BLANK_ENTRY)
                continue
            
            try:
                price = int(input("Price: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_INPUT)
                continue

            if not price:
                clear_console()
                Messages.error(BLANK_ENTRY)
                continue

            if price <= 0:
                clear_console()
                Messages.error("Price cannot be less than $0.01")
                continue
            
            try:
                stock = int(input("Stock: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_INPUT)
                continue

            if stock < 0:
                clear_console()
                Messages.error("Stock cannot be less than 0")

            print(category)
            cat = input("Category: ")
            if not cat or cat not in category:
                clear_console()
                Messages.error(INVALID_INPUT)
                return
            try:
                weight = int(input("Weight: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_INPUT)
            
            if weight < 0.01:
                clear_console()
                Messages.error("Weight cannot be less than 0.01!")
                continue
            
            new_item = Item(name, price, description, cat, stock, weight)
            if ItemService.create_item(new_item):
                Messages.success("Item added successfully!")
                print(new_item)
                Messages.pause()
                return True
            
            return None

    def admin_orders_menu():
        clear_console()
        while True:
            Messages.title("ORDERS")
            orders = OrderService.get_all_orders()
            if not orders:
                Messages.standard("No orders found")
                Messages.pause()
                break
            for index, order in enumerate(orders):
                Messages.menu_option(index + 1, order.short_str())
            Messages.menu_option(0, "Return to Menu")
            try:
                user_input = int(input("Enter selection: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input not in range(len(orders) + 1):
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return None if user_input == 0 else orders[user_input - 1]

    def admin_view_order(order):
        clear_console()
        Messages.title("ORDER")
        print(order)
        Messages.menu_option(1, "Delete Order")
        Messages.menu_option(0, "Return to Orders")
        try:
            user_input = int(input("Enter selection: "))
        except ValueError:
            clear_console()
            Messages.error(INVALID_OPTION)
            return
        if user_input not in [0, 1]:
            clear_console()
            Messages.error(INVALID_OPTION)
        if user_input == 1:
            confirm = input("Are you sure you want to delete this order? (Y/N): ")
            if confirm.lower() in ["ye", "y", "yes"]:
                OrderService.delete_order(order)
                Messages.success("Successfully deleted order")
                Messages.pause()
        return

    # USER STORE MENUS

    def store_menu(account) -> int:
        clear_console()
        while True:
            Messages.title("STORE")
            Messages.menu_option(1, "Browse Products")
            Messages.menu_option(2, "View Cart")
            Messages.menu_option(3, "Order History")
            Messages.menu_option(4, "Account")
            Messages.menu_option(0, "Exit")
            try:
                user_input = int(input("Enter selection: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input not in [1, 2, 3, 4, 0]:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return user_input

    def product_category_menu() -> int:
        clear_console()
        while True:
            Messages.title("CATEGORIES")
            Messages.menu_option(1, "Laptops")
            Messages.menu_option(2, "Phones")
            Messages.menu_option(3, "Watches")
            Messages.menu_option(4, "Headphones")
            Messages.menu_option(5, "Accessories")
            Messages.menu_option(6, "All Products")
            Messages.menu_option(0, "Return to Menu")
            try:
                user_input = int(input("Enter selection: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input not in [1, 2, 3, 4, 5, 6, 0]:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return user_input

    def view_cart_menu(account):
        clear_console()
        while True:
            Messages.title("CART")
            cart = AccountService.get_cart(account)
            user_choices = []
            if not cart:
                Messages.standard("Your cart is empty!")
                user_choices = [0]
            else:
                user_choices = [0, 1, 2]
            for item in cart:
                print(item.short_str())
            print("\n")
            total = sum(item.price for item in cart)
            shipping = sum(item.weight_to_shipprice() for item in cart) 
            if shipping > 20:
                shipping = 20
            print("Sub Total: " + "{:.2f}".format(total))
            print("Shipping: " + "{:.2f}".format(shipping))
            print("Total: " + "{:.2f}".format(total + shipping))
            print("\n")
            if cart:
                Messages.menu_option(1, "Checkout")
                Messages.menu_option(2, "Remove Item")
            Messages.menu_option(0, "Return to Store")
            try:
                user_input = int(input("Enter selection: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input not in user_choices:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return user_input

    def account_menu(account):
        clear_console()
        while True:
            Messages.title("ACCOUNT")
            print(account)
            Messages.menu_option(1, "Edit Information")
            Messages.menu_option(2, "Change Password")
            Messages.menu_option(0, "Return to Store") 
            try:
                user_input = int(input("Enter selection: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input not in [1, 2, 0]:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return user_input

    def view_order_history(account):
        clear_console()
        while True:
            Messages.title("ORDER HISTORY")
            orders = OrderService.get_orders_by_account(account.email)
            if not orders:
                Messages.standard("You have no orders!")
                Messages.pause()
                break
            for index, order in enumerate(orders):
                Messages.menu_option(index + 1, order.short_str())
            Messages.menu_option(0, "Return to Menu")
            try:
                user_input = int(input("Enter selection: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input not in range(len(orders) + 1):
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return None if user_input == 0 else orders[user_input - 1]

    def checkout(account):
        clear_console()
        cart = AccountService.get_cart(account)
        for item in cart:
            if item.stock == 0:
                Messages.error("Cannot check out with out of stock item!")
                print(item)
                Messages.standard("Please remove this item and try again!")
                Messages.pause()
                return None
        subtotal = sum(item.price for item in cart)
        shipping = sum(item.weight_to_shipprice() for item in cart)
        total = subtotal + shipping
        now = datetime.now()
        delivery_date = now + timedelta(days=3)
        order = Order(account.to_dict(), AccountService.get_cart_dict(account), subtotal, total, shipping, delivery_date.strftime("%m/%d/%Y, %H:%M:%S"), now.strftime("%m/%d/%Y, %H:%M:%S"))
        success = OrderService.create_order(order)
        if success:
            for item in cart:
                ItemService.remove_stock(item, 1)
                AccountService.remove_from_cart(account, item)
            print(order)
            Messages.success("Order placed!")
            Messages.pause()

        else:
            Messages.error("An unknown error occured, please try again...")
            Messages.pause()

    def remove_cart_menu(account):
        clear_console()
        while True:
            Messages.title("REMOVE ITEM")
            cart = AccountService.get_cart(account)
            if not cart:
                Messages.standard("Your cart is empty!")
                Messages.pause()
                break
            for index, item in enumerate(cart):
                Messages.menu_option(index+1, item.short_str())
            Messages.menu_option(0, "Return to Cart")
            try:
                user_input = int(input("Enter selection: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input not in range(len(cart) + 1):
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input == 0:
                return False
            AccountService.remove_from_cart(account, cart[user_input - 1])
            return True

    def view_order(order):
        clear_console()
        while True:
            Messages.title("ORDER")
            print(order)
            Messages.menu_option(0, "Return to Order History")
            try:
                user_input = int(input("Enter selection: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input not in [0]:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return None

    def view_product_category_menu(category_number) -> int:
        clear_console()
        while True:
            Messages.title(category[category_number - 1])
            items = []
            if category_number == 6:
                items = ItemService.get_all_items()
            else:
                items = ItemService.get_items_by_category(category[category_number - 1])
            for index, item in enumerate(items):
                Messages.menu_option(index + 1, item.short_str())
            Messages.menu_option(0, "Return to Catagories")
            try:
                user_input = int(input("Enter selection: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input not in range(len(items) + 1):
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return None if user_input == 0 else items[user_input - 1]

    def view_item(item, account):
        clear_console()
        while True:
            Messages.title(item.name)
            print(item)
            user_choices = []
            if item.stock > 0:
                Messages.menu_option(1, "Add to Cart")
                user_choices = [0, 1]
            else:
                Messages.menu_option("X", "Add to Cart")
                user_choices = [0]
            Messages.menu_option(0, "Return to Category")
            try:
                user_input = int(input("Enter selection: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input not in user_choices:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input == 1:
                AccountService.add_to_cart(account, item)
                return True
            return False

    def update_account_menu(account):
        clear_console()
        while True:
            Messages.title("UPDATE ACCOUNT")
            Messages.menu_option(1, "Update Street Address")
            Messages.menu_option(2, "Update City")
            Messages.menu_option(3, "Update State")
            Messages.menu_option(4, "Update Zip")
            Messages.menu_option(0, "Return to Menu")
            try:
                user_input = int(input("Enter selection: "))
            except ValueError:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            if user_input not in [1, 2, 3, 4, 5, 0]:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return user_input

    def change_password(account):
        clear_console()
        while True:
            Messages.title("CHANGE PASSWORD")
            password = get_valid_password()
            if password is None:
                print(PASSWORD_CHANGE_ERROR)
                return None
            password = AccountService.hash_password(password)
            success = AccountService.change_password(account, password)
            if success:
                account = AccountService.refresh(account)
                Messages.success("Password updated successfully!")
                Messages.pause()
                return account
            return None

    def update_address(account):
        address = input("Street Address: ")

        if not address:
            clear_console()
            Messages.error(BLANK_ENTRY)
            Messages.pause()
            return None
        success = AccountService.update_address(account, address)
        if success:
            account = AccountService.refresh(account)
            Messages.success("Address updated successfully!")
            Messages.pause()
            return account
        return None

    def update_city(account):
        city = input("City: ")
        if not city:
            clear_console()
            Messages.error(BLANK_ENTRY)
            Messages.pause()
            return None
        success = AccountService.update_city(account, city)
        if success:
            account = AccountService.refresh(account)
            Messages.success("City updated successfully!")
            Messages.pause()
            return account
        return None

    def update_state(account):
        state = get_valid_state()
        if state:
            success = AccountService.update_state(account, state)
            if success:
                account = AccountService.refresh(account)
                Messages.success("State updated successfully!")
                Messages.pause()
                return account
        else:
            Messages.pause()
        return None

    def update_zip(account):
        zip = input("Zip Code: ")
        if not zip:
            clear_console()
            Messages.error(BLANK_ENTRY)
            Messages.pause()
            return None
        success = AccountService.update_zip(account, zip)
        if success:
            account = AccountService.refresh(account)
            Messages.success("Zip updated successfully!")
            Messages.pause()
            return account
        return None