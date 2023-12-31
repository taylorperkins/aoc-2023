import datetime


def getInput(fp):
    with open(fp) as f:
        content = f.read()

    return content


def timeit(f):
    def inner(*args, **kwargs):
        start = datetime.datetime.now()
        result = f(*args, **kwargs)
        end = datetime.datetime.now()

        print(f"Took {round((end - start).total_seconds(), 5)}s, "
              f"{round((end - start).total_seconds() * 1000, 5)}ms")
        return result
    return inner
