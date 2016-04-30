from decorator07 import my_decorator

@my_decorator
def just_sm_function():
    print("Whee")

if __name__ == '__main__':
    just_sm_function()