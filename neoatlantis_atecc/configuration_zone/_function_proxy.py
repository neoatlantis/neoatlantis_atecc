
class FunctionProxy:
    """
        Allow to mask a function as an Object.
        https://stackoverflow.com/questions/31907060/python-3-enums-with-function-values
    """
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)
