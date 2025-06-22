from kerbian.utils.logger import error

def catch_and_log(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            error(f"Exception in {func.__name__}: {exc}")
            raise
    return wrapper