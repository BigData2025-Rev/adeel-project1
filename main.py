from app import Menu
from utils import Messages
import sys

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
            
if __name__ == "__main__":
    main()