import boiler

def go(filename):
    print(f"results from {filename}:")
    # pick one:
    # sections = boiler.sections(filename)
    # lines = boiler.lines(filename)
    # words = boiler.words(filename)
    # digits = boiler.digits(filename)
    # chars = boiler.chars(filename)

if __name__ == '__main__':
    for f in boiler.files():
        go(f)
