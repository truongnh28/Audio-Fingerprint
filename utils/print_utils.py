from termcolor import colored


def print_error(message):
    """
         print error message
         :param message: error message
         :return: None
    """
    print(colored(message, 'red'))
    pass


def print_message(message):
    """
         Print normal information
         :param message: normal prompt message
         :return: None
    """
    print(colored(message, 'cyan'))
    pass


def print_warning(message):
    """
         print warning message
         :param message: warning message
         :return: None
    """
    print(colored(message, 'yellow'))
    pass







