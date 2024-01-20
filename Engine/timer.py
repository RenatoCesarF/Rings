class Timer:
    _finished: bool
    miliseconds: int
    timer: float

    def __init__(self, miliseconds: int, start_loaded: bool = False):
        self._finished = start_loaded
        self.miliseconds = miliseconds
        self.timer = miliseconds

    def has_finished(self) -> bool:
        return self._finished or self.timer <= 0

    def update_timer(self, delta_time):
        if self.timer <= 0:
            self._finished = True
            return
        self.timer -= delta_time * 1000

    def reset(self):
        self._finished = False
        self.timer = self.miliseconds

    def add_to_timer(self, milisenconds):
        self.timer += milisenconds

    def time_missing_in_seconds(self) -> float:
        return self.timer / 1000

    def __str__(self) -> str:
        return (
            f'finished: {self.has_finished()} ; timer: {self.timer} '
            + f'miliseconds: {self.miliseconds}'
            + f'seconds missing:  {self.time_missing_in_seconds()}'
        )
