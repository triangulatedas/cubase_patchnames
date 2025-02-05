

class TextProgressBar:

    def __init__(self, total_items: int, length=100, fill='█', prefix='', suffix='', start_value: int = 0, num_decimals: int = 2, print_end="\r"):
        self._total_items: int = total_items
        self._value = start_value
        self._decimals = num_decimals
        self._prefix = prefix
        self._suffix = suffix
        self._length = length
        self._fill = fill
        self._print_end = print_end

    def _print_progress_bar (self):
        percent = ("{0:." + str(self._decimals) + "f}").format(100 * (self._value / float(self._total_items)))
        filled_length = int(self._length * self._value // self._total_items)
        bar = self._fill * filled_length + '-' * (self._length - filled_length)
        print(f'\r{self._prefix} |{bar}| {percent}% {self._suffix}', end = self._print_end)
        # Initial Call

    def set_items(self, items: int):
        self._total_items = items

    def update_progress(self, count=1):
        self._value += count
        self._print_progress_bar()
        if self._value >= self._total_items:
            print()


text_bar = TextProgressBar(0)

