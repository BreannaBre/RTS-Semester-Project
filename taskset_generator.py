import random
import math
import numpy as np

# returns a list of utilzations for a taskset
def utilization_distributor(num_tasks, util_sum):
    utilizaitons = []
    for task_index in range(1, num_tasks):
        random_value = random.random()
        # calculate task's utilization
        current_task_utilization = util_sum * (1 - random_value ** (1 / (num_tasks - task_index)))
        # update remaining sum to take up
        util_sum -= current_task_utilization
        utilizaitons.append(current_task_utilization)
    # last task gets remaining utilization left unused
    utilizaitons.append(util_sum)
    return utilizaitons

# returns a list of tuples, where each tuple is a task
# The tuple contains (period, criticality (bool, high=1), c_low, c_high)
def create_taskset(num_tasks, util_sum, r):
    utilizations = utilization_distributor(num_tasks, util_sum)
    random.shuffle(utilizations)
    taskset = []
    high_pri_tasks = num_tasks//2
    for util in utilizations:
        # period is randomly determined with different frequencies due to different kinds of tasks in pump
        period = 10**np.random.uniform(math.log10(10), math.log10(100))
        # assign criticality
        # TODO allow high priority tasks to be half of tasks or less?
        if high_pri_tasks > 0:
            criticality = 1
            high_pri_tasks -= 1
        else:
            criticality = 0

        c_low = util * period
        if criticality:
            c_high = c_low * r
        else:
            c_high = c_low
        taskset.append((period, criticality, c_low, c_high))
    return taskset


