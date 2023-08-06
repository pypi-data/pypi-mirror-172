import time
import typing

from python_qa.logging.logging import Logging


def wait_for_condition(
        func: typing.Callable,
        expected_condition: typing.Callable[[object], bool],
        wait_time: int = 10,
        step_time: int = 0.5,
):
    res = None
    end_time = time.time() + wait_time
    while time.time() < end_time:
        time.sleep(step_time)
        try:
            res = func()
            if expected_condition(res):
                return res
        except Exception as e:
            Logging.logger.warning(f"An error: {e} occurred while waiting\nContinue waiting ...")
    return res

    wait = wait_for_condition


def wait_for_creation(
        func: typing.Callable, status: int = 200, wait_iter: int = 5, wait_step: int = 0.5
):
    iter = 0
    while iter < wait_iter:
        res = func()
        if res.status_code == status:
            return res
        iter += 1
        time.sleep(wait_step)

    wc = wait_for_creation
