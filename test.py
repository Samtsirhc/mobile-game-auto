def decorator(func):
    def my_dec():
        print(func.__name__)
        func()
        print(2)
    return my_dec

@decorator
def hhh():
    print("ha")

if __name__ == '__main__' :
    hhh()