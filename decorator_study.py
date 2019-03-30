#!//anaconda/bin/python
class Decoratorwitharguments(object):
    def __init__(self, f):
        """
        If there are no decorator arguments, the function
        to be decorated is passed to the constructor.
        """
        self.f = f

    def __call__(self, *args):
        """
        The __call__ method is not called until the
        decorated function is called.
        """
        self.f(*args)


def decoratorwithoutargument(func):
    def fun_name():
        print(func.__name__)
        return func()
    return fun_name()


@Decoratorwitharguments
def fan_test(x, y):
    print(x*y)
fan_test(6, 3)


@decoratorwithoutargument
def fan_test2():
    print('test 123')
