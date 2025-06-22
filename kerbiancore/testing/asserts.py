class Assert:
    @staticmethod
    def equal(a, b, msg=None):
        if a != b:
            raise AssertionError(msg or f"Expected {a!r} == {b!r}")

    @staticmethod
    def not_equal(a, b, msg=None):
        if a == b:
            raise AssertionError(msg or f"Expected {a!r} != {b!r}")

    @staticmethod
    def true(expr, msg=None):
        if not expr:
            raise AssertionError(msg or f"Expected expression to be true but got {expr!r}")

    @staticmethod
    def false(expr, msg=None):
        if expr:
            raise AssertionError(msg or f"Expected expression to be false but got {expr!r}")

    @staticmethod
    def is_none(expr, msg=None):
        if expr is not None:
            raise AssertionError(msg or f"Expected None but got {expr!r}")

    @staticmethod
    def not_none(expr, msg=None):
        if expr is None:
            raise AssertionError(msg or f"Expected non-None value but got None")

    @staticmethod
    def raises(exc_type, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            if not isinstance(e, exc_type):
                raise AssertionError(f"Expected {exc_type.__name__}, got {type(e).__name__}")
            return
        raise AssertionError(f"Expected exception {exc_type.__name__} but none was raised")