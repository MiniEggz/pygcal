def wrapp(func):
    def wrapper():
        print("this is the wrapper")
        func()

    return wrapper


@wrapp
def other_function():
    print("this is the wrapped function")


if __name__ == "__main__":
    other_function()
