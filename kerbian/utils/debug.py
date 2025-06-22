import sys
import traceback
from kerbian.utils.logger import error

def print_exception():
    exc_type, exc_value, exc_tb = sys.exc_info()
    formatted = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    error(formatted)