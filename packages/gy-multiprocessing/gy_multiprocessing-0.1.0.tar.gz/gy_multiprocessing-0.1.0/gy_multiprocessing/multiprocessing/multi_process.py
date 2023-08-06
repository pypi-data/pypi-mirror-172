import multiprocessing
import time


class MultiProcess:
    def __init__(self, init: dict, outer_loop_times: int, current_loop_index: int, process_name: str = "",
                 max_threads: int = multiprocessing.cpu_count(), timeout: int = 2 * 60, process_log: bool = False):
        # set max processing pool equals to the cpu core number
        self.max_threads = max_threads
        # every single process could only have 2 min runtime
        self.timeout = timeout
        # a processing list
        self.process_list = init['process_list']
        # start timing for main loop
        self.start_time = init['start_time']
        # outer loop times
        self.outer_loop_times = outer_loop_times
        # current loop index
        self.current_loop_index = current_loop_index
        # process name
        self.process_name = process_name
        # showing process log when closing to end
        self.process_log = process_log

    def start_process(self, func, func_args: tuple) -> (list, list):

        process_list = self.process_list

        # initialize multiprocessing for core loop function
        process = multiprocessing.Process(target=func, args=func_args)

        # start timing for each process
        process_start_time = time.time()

        # set dict inside the process list
        process_list_dict = {'process': process, 'start_time': process_start_time}
        process_list.append(process_list_dict)

        # start the process
        process.start()

        print(f"process: {str(process_list_dict['process'].name)} with {self.process_name} starts") \
            if self.process_name is not "" else \
            print(f"process: {str(process_list_dict['process'].name)} starts")

        return process_list

    def run(self, func, func_args: tuple):

        process_list = self.start_process(func, func_args)

        while True:
            # while loop for setting max process to max_threads

            if len(self.process_list) < self.max_threads \
                    and self.current_loop_index > self.outer_loop_times - self.max_threads \
                    and self.process_log:
                # if the process is ending with less than max_threads undergoing processes
                # print current processes
                for each_process in process_list:
                    print(
                        f"{each_process['process'].name}, runtime: {format(time.time() - each_process['start_time'], '.1f')}s, name: {self.process_name}") \
                        if self.process_name is not "" else \
                        print(
                            f"{each_process['process'].name}, runtime: {format(time.time() - each_process['start_time'], '.1f')}s")
                print("-----")

            if process_list:
                # if there is any process in the list

                for index, each_process in enumerate(process_list):
                    # check each process
                    current_time = time.time()
                    time_cost = current_time - each_process['start_time']

                    if not each_process['process'].is_alive():
                        # if any process is dead
                        time_cost = current_time - each_process['start_time']
                        print(
                            f"process: {str(each_process['process'].name)} done in: {format(time_cost, '.1f')}s with {self.process_name}") \
                            if self.process_name is not "" else \
                            print(f"process: {str(each_process['process'].name)} done in: {format(time_cost, '.1f')}s")
                        try:
                            each_process['process'].terminate()
                            each_process['process'].close()
                        except ValueError:
                            pass
                        process_list.pop(index)
                    elif time_cost >= self.timeout:
                        # or any process takes too long to finish (longer than the timeout)
                        # TODO! not working perfectly, one time out will cause all processes to terminate?
                        print(
                            f"process: {str(each_process['process'].name)} with {self.process_name} is terminated due to timeout") \
                            if self.process_name is not "" else \
                            print(
                                f"process: {str(each_process['process'].name)} is terminated due to timeout")
                        try:
                            each_process['process'].terminate()
                            each_process['process'].close()
                        except ValueError:

                            pass
                        process_list.pop(index)
                    elif time_cost >= self.timeout - 10:
                        # only 10s to timeout
                        print(
                            f"process: {str(each_process['process'].name)} closing to timeout with name: {self.process_name}") \
                            if self.process_name is not "" else \
                            print(f"process: {str(each_process['process'].name)} closing to timeout")

                if len(process_list) < self.max_threads and self.current_loop_index != self.outer_loop_times - 1:
                    # if all tasks are in the pool then wait until all tasks are finished
                    # or break the loop to add a new task in the pool
                    break
            else:
                # if all tasks in the pool are done
                break

            # check every 2 seconds
            time.sleep(2)

        return {
            'process_list': process_list,
            'start_time': self.start_time,
            'process_result_list': []
        }
