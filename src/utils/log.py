from colorama import Fore, Back, Style, init

init()

def print_colored(text, color):
    print(color + str(text) + Style.RESET_ALL)

def info(text):
    print_colored(text, Fore.BLUE)

def warn(text):
    print_colored(text, Fore.YELLOW)

def error(text):
    print_colored(text, Fore.RED)

def text_highlighted(text):
    print_colored(text, Fore.BLACK + Back.WHITE)

def info_highlighted(text):
    print_colored(text, Fore.BLACK + Back.LIGHTGREEN_EX)

def warn_highlighted(text):
    print_colored(text, Fore.BLACK + Back.LIGHTYELLOW_EX)

def error_highlighted(text):
    print_colored(text, Fore.BLACK + Back.LIGHTRED_EX)
