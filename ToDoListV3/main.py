import os
import datetime
import colorama
from colorama import Fore, Back, Style


colorama.init()
print(Fore.RED + "This text is red!")
print(Fore.GREEN + "This text is green!")


print(Fore.RED + 'This text is red')
print(Back.GREEN + 'This text has a green background')
print(Style.BRIGHT + 'This text is bright')
print(Style.RESET_ALL + 'Back to normal text')


# Print text with different colors and styles
print(Style.BRIGHT + Fore.RED + Back.GREEN + 'Bright red text on green background')


print(Style.BRIGHT + "This text is bright/bold")
print(Style.DIM + "This text is dim")
print(Style.NORMAL + "This text is normal")


print(Fore.RED + 'Red text')
# This will still be red
print('Normal text')  
# Reset styles
print(Style.RESET_ALL)  
print('Back to normal')


class ToDoList:
    def __init__(self):
        self.TASKS_LIST = "tasks.txt"
        self.COMPLETE_TASKS_LIST = "complete_tasks.txt"
        self._tasks = []
        self._complete_list = []
        self._create_date = datetime.datetime.now()
        self._number_of_tasks = 0

    def _load_tasks_file(self, filename):
        tasks_list = []
        if not os.path.exists(filename):
            return []
        
        with open(filename, 'r') as file:
            tasks_list = [line.strip() for line in file.readlines() if line.strip() and not line.startswith('----')]
        return tasks_list
    
    def _save_tasks_file(self, tasks_list, filename):
        with open(filename, 'w') as file:
            for task in tasks_list:
                file.write(f'{task}\n')
                file.write('----\n')
    
    def _add_task_to_tasks_file(self):
        self._tasks = self.load_tasks_file(self.TASKS_LIST)
        user_input = input('Add task: ').strip()
        if user_input:
            self._tasks.append(user_input)
            self.save_tasks_file(self._tasks, self.TASKS_LIST)
            print("Task added successfully!")
        else:
            print("No task entered. Nothing was added.")
