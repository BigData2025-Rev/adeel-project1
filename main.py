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

        if account is not None:
            Messages.standard(f"Welcome {account.first_name} {account.last_name}!")
            while True:
                menu_option = Menu.store_menu(account)
                
                if (menu_option == 1):
                    Menu.product_catagoery_menu()
                elif (menu_option == 2):
                    Menu.view_cart_menu(account)
                
            
if __name__ == "__main__":
    main()