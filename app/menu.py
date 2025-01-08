from utils import Messages
from database import accounts
from app.account_service import AccountService
from models import Account
import getpass
import os

AccountService = AccountService(accounts)

INVALID_OPTION = "Invalid option! Please try again...\n"
PASS_DO_NOT_MATCH = "Passwords do not match! Please try again...\n"
PASSWORD_ERROR = "Too many failed attemps, please try again later...\n"
STATE_ERROR = "Please enter a valid two character state abbreviation\n"
EMAIL_TAKEN = "Email already in use! Please login instead\n"

catagory = ["Laptops", "Phones", "Watches", "Headphones", "Accessories", "All Products"]

state_abbreviations = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

def get_valid_password() -> str:
    retry_attemps = 3
    while retry_attemps > 0:
        password = getpass.getpass("Password: ")
        confirm_password = getpass.getpass("Confirm Password: ")
        if password != confirm_password:
            Messages.error(PASS_DO_NOT_MATCH)
            Messages.error("You have " + str(retry_attemps) + " attempts left")
            continue
        break
    if retry_attemps == 0:
        Messages.error(PASSWORD_ERROR)
        return None
    return password

def get_valid_state() -> str:
    retry_attemps = 3

    while retry_attemps > 0:
        state = input("State: ")
        if state not in state_abbreviations:
            Messages.error(STATE_ERROR)
            Messages.error("You have " + str(retry_attemps) + " attempts left")
            continue
        break
    if retry_attemps == 0:
        Messages.error(PASSWORD_ERROR)
        return None
    return state

def clear_console():
    os.system("cls")

class Menu:
    def main_menu() -> int:
        clear_console()
        while True:
            Messages.title("TECH STORE")
            Messages.menu_option(1, "Login")
            Messages.menu_option(2, "Register")
            Messages.menu_option(0, "Exit")

            user_input = int(input("Enter option: "))
            if user_input not in [1, 2, 0]:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return user_input

    def login() -> str:
        retry_attemps = 3
        clear_console()
        while retry_attemps > 0:
            Messages.title("LOG-IN")
            Messages.standard("Please enter your information below")

            email = input("Email: ")
            password = getpass.getpass("Password: ")
            account = AccountService.login(email, password)
            if account is None:
                clear_console()
                Messages.error("Invalid email or password! Please try again...\n\n")
                Messages.error("You have " + str(retry_attemps) + " attempts left")
                retry_attemps -= 1
                continue
            Messages.success("Logged in successfully!")
            return account


    def register() -> str:
        clear_console()
        Messages.title("REGISTER")
        Messages.standard("Please enter your information below")

        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ").lower()

        if AccountService.validate_email(email):
            Messages.error(EMAIL_TAKEN)
            return None

        password = get_valid_password()
        if password is None:
            return None
        password = AccountService.hash_password(password)
        
        address = input("Street Address: ")
        city = input("City: ")

        state = get_valid_state()
        if state is None:
            return None
        
        zip = input("Zip Code: ")
        
        newAccount = Account(first_name, last_name, email, password, address, city, state, zip)
        if AccountService.create_account(newAccount):
            Messages.success("Account created successfully!")
            return newAccount
        return None
    
    def store_menu(account) -> int:
        clear_console()
        while True:
            Messages.title("STORE MENU")
            Messages.menu_option(1, "Browse Products")
            Messages.menu_option(2, "View Cart")
            Messages.menu_option(3, "Order History")
            Messages.menu_option(4, "Account")
            Messages.menu_option(0, "Exit")

            user_input = int(input("Enter option: "))
            if user_input not in [1, 2, 3, 4, 0]:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return user_input
    
    def product_catagoery_menu() -> int:
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

            user_input = int(input("Enter option: "))
            if user_input not in [1, 2, 3, 4, 5, 6, 0]:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return user_input
    
    def view_product_catagory_menu(catagory_number) -> int:
        clear_console()
        while True:
            Messages.title(catagory[catagory_number - 1])
            Messages.menu_option(1, "View Products")
            Messages.menu_option(2, "Search Products")
            Messages.menu_option(0, "Return to Menu")

            user_input = int(input("Enter option: "))
            if user_input not in [1, 2, 0]:
                clear_console()
                Messages.error(INVALID_OPTION)
                continue
            return user_input
    
    def view_cart_menu(account):
        clear_console
        while True:
            Messages.title("CART")
            cart = AccountService.get_cart(account)
            if not cart:
                Messages.standard("Your cart is empty!")
                Messages.pause()
                break
            for item in cart:
                print(item)
            print("\n")
            total = sum(item.price for item in cart)
            shipping = sum(item.weight_to_shipprice() for item in cart) 
            if shipping > 20:
                shipping = 20
            print("Sub Total: " + "{:.2f}".format(str(total)))
            print("Shipping: " + "{:.2f}".format(str(shipping)))
            print("Total: " + "{:.2f}".format(str(total + shipping)))
            Messages.pause()
