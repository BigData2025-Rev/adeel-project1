class Color:
    RED = '\033[91m'
    END = '\033[0m'
    GREEN = '\033[32m'
    CYAN = '\033[36m'
    YELLOW = '\033[33m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    MAGENTA = '\033[35m'

class Errors:
    INVALID_OPTION = "Invalid option! Please try again...\n"
    PASS_DO_NOT_MATCH = "Passwords do not match! Please try again...\n"
    PASSWORD_ERROR = "Too many failed attemps, please try again later...\n"
    PASSWORD_CHANGE_ERROR = "Password change failed! Please try again...\n"
    STATE_ERROR = "Please enter a valid two character state abbreviation\n"
    EMAIL_TAKEN = "Email already in use! Please login instead\n"
    NOT_VALID_INPUT = "Invalid input, please try again...\n"

class Messages:
    def menu_option(option, message: str):
        if option == 0 or option == "X":
            print(Color.RED + "[" + str(option) + "] " + Color.END, end="")
        else:
            print(Color.MAGENTA + "[" + str(option) + "] " + Color.END, end="")
        print(message)
    def error(message: str):
        print("\n"  + Color.RED + message + Color.END + "\n" )
    def success(message: str):
        print("\n" + Color.GREEN + message + Color.END + "\n" )
    def standard(message: str):
        print("\n"  + Color.CYAN + message + Color.END + "\n" )
    def title(message: str):
        print("================")
        print(message.center(16))
        print("================")
    def pause():
        input('Press ENTER to continue... ')
    def end_message():
        print("================\n")