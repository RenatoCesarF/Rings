from Engine.timer import Timer

delta = 0.017


def test_time_in_seconds():
    timer_ins = Timer(5000)
    seconds = timer_ins.time_missing_in_seconds()
    assert seconds == 5


def test_time_in_seconds_passing_tree_seconds():
    timer_ins = Timer(5000)
    seconds_to_pass = 3 * 60  # 3 seconds

    for i in range(0, seconds_to_pass + 1):
        timer_ins.update_timer(delta)

    assert round(timer_ins.time_missing_in_seconds()) == 2
