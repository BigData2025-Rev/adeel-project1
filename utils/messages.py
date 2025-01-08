class Color:
    RED = '\033[91m'
    END = '\033[0m'
    GREEN = '\033[32m'
    CYAN = '\033[36m'
    YELLOW = '\033[33m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    MAGENTA = '\033[35m'

class Messages:
    def menu_option(option: int, message: str):
        if message == "Exit":
            print(Color.RED + "[" + str(option) + "] " + Color.END, end=" ")
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