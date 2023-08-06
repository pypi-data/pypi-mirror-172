import multiprocessing
import time


class MultiProcess:
    def __init__(self, process_list: list, process_result_list: list, outer_loop_times: int, start_time,
                 max_threads: int = multiprocessing.cpu_count(), timeout: int = 2 * 60):
        # set max processing pool equals to the cpu core number
        self.max_threads = max_threads
        # every single process could only have 2 min runtime
        self.timeout = timeout
        # a processing list
        self.process_list = process_list
        # a corresponding list of returned values
        self.process_result_list = process_result_list
        # start timing for main loop
        self.start_time = start_time
        # a get context method for get return value
        self.ctx = multiprocessing.get_context('spawn')
        self.q = self.ctx.Queue()

        self.outer_loop_times = outer_loop_times

    def start_process(self, func, func_args: tuple, additional_dict: dict = None) -> (list, list):

        process_list = self.process_list
        process_result_list = self.process_result_list

        # initialize multiprocessing for core loop function
        process = multiprocessing.Process(target=func, args=func_args)

        # start timing for each process
        process_start_time = time.time()

        # set dict inside the process list
        process_list_dict = {'process': process, 'start_time': process_start_time}
        if additional_dict is not None:
            process_list_dict.update(additional_dict)
        process_list.append(process_list_dict)

        # start the process
        process.start()
        print(f"process: {str(process.name)} with {additional_dict} starts")

        # append the possible returned value in the result list
        process_result_list.append(self.q)

        return process_list, process_result_list

    def runtime(self, func, func_args: tuple, outer_loop_index: int, additional_dict: dict = None,
                process_log: bool = False):

        process_list, process_result_list = self.start_process(func, func_args + (self.q,), additional_dict)

        while True:
            # while loop for setting max process to max_threads

            if len(self.process_list) < self.max_threads \
                    and outer_loop_index > self.outer_loop_times - self.max_threads \
                    and process_log:
                # if the process is ending with less than max_threads undergoing processes
                # print current processes

                for each_process in process_list:
                    print(
                        f"{each_process['process'].name}, runtime: {format(time.time() - each_process['start_time'], '.1f')}s, name: {each_process['name']}")
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
                            f"process: {str(each_process['process'].name)} done in: {format(time_cost, '.1f')}s with {each_process['name']}: {process_result_list[index].get()}")
                        try:
                            each_process['process'].terminate()
                            each_process['process'].close()
                        except ValueError:
                            pass
                        process_list.pop(index)
                        process_result_list.pop(index)
                    elif time_cost >= self.timeout:
                        # or any process takes too long to finish (longer than the timeout)
                        print(
                            f"process: {str(each_process['process'].name)} with name: {each_process['name']} is terminated due to timeout")
                        try:
                            # TODO! not working perfectly, one time out will cause all processes to terminate?
                            each_process['process'].terminate()
                            each_process['process'].close()
                        except ValueError:
                            pass
                        process_list.pop(index)
                        process_result_list.pop(index)
                    elif time_cost >= self.timeout - 10:
                        # only 10s to timeout
                        print(
                            f"process: {str(each_process['process'].name)} closing to timeout with name: {each_process['name']}")

                if len(process_list) < self.max_threads and outer_loop_index != self.outer_loop_times - 1:
                    # if all tasks are in the pool then wait until all tasks are finished
                    # or break the loop to add a new task in the pool
                    break
            else:
                # if all tasks in the pool are done
                break

            # check every 2 seconds
            time.sleep(2)