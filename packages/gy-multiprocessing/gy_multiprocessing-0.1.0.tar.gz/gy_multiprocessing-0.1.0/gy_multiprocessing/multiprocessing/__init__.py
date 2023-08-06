import time

from gy_multiprocessing.multiprocessing import multi_process
from gy_multiprocessing.multiprocessing import multi_process_withqueue


def init() -> dict:
    return {
        'process_list': [],
        'start_time': time.time(),
        'process_result_list': []
    }
