from time import time


class Timer:

    def __init__(self):
        self.start = time()

    def next(self, *message, reset=None):
        if isinstance(message[-1], bool) and reset is None:
            reset = message[-1]
            message = message[:-1]

        msg = ' '.join([f'{x}' for x in message])
        print(f'{msg}: {self.elapsed(reset)}s')

    def elapsed(self, reset=False):
        result = time() - self.start
        if reset:
            self.start = time()
        return result

    def __enter__(self):
        self.start = time()

    def __exit__(self, *_):
        print(f'Completed in {self.elapsed()}s')
