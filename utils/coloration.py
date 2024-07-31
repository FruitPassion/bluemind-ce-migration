from colorama import Fore, Style


def colour_print(text, type_text):
    if type_text == 'error':
        colour = Fore.RED
    elif type_text == 'success':
        colour = Fore.GREEN
    elif type_text == 'warning':
        colour = Fore.YELLOW
    elif type_text == 'info':
        colour = Fore.BLUE
    else:
        colour = Fore.WHITE

    print(colour + text + Style.RESET_ALL)
