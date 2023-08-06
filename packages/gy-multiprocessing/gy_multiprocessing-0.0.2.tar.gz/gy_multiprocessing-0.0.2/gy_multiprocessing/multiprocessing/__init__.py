import time


def init() -> dict:
    return {
        'process_list': [],
        'start_time': time.time(),
        'process_result_list': []
    }
