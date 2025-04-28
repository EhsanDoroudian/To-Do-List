class UserOptionInputError(Exception):
    def __init__(self, message, num_input):
        self.message = message
        self.num_input = num_input


class TasksInputOutOfRangeError(Exception):
    def __init__(self, message, len_tasks_list):
        self.message = message
        self.len_tasks_list = len_tasks_list


class ZeroUserInput(Exception):
    def __init__(self, message):
        self.message = message


class NegetiveInputNumber(Exception):
    def __init__(self, message):
        self.message = message