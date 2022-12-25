from utils.print_utils import print_error, print_message, print_warning
import time


def start_time():
    return time.time()


def end_time(start_time, message):
    dur = time.time() - start_time
    print_warning(message + "：" + str(dur) + "s")
