import matplotlib.pyplot as plt
import numpy as np

import schedulers
import taskset_generator as tg

# set these variables as needed
num_tasks = 4
util_inc = 0.1
criticality_factor = 2

def test_and_get_data(crit_factor):
    x = []
    y_edf = []
    y_amc = []
    util_sum = 0.1
    while util_sum <= 1:
        schedulable_edf_tasksets = 0
        schedulable_amc_tasksets = 0
        # run 1000 tasksets at current util sum, and run schedulability test for both algorithms
        for i in range(1000):
            taskset = tg.create_taskset(num_tasks, util_sum, crit_factor)
            if schedulers.test_schedulability_AMC(taskset) == True:
                schedulable_amc_tasksets += 1
            if schedulers.test_schedulability_EDF_VD(taskset) == True:
                schedulable_edf_tasksets += 1
        # append for plotting later
        x.append(util_sum)
        y_amc.append(schedulable_amc_tasksets/1000)
        y_edf.append(schedulable_edf_tasksets/1000)
        util_sum += util_inc
    return x, y_amc, y_edf

def calcaulate_weighted_schedulability(xs, ys, crit_factor):
    top_sum = 0
    bottom_sum = np.sum(xs)
    for i in range(len(xs)):
        top_sum += xs[i] * ys[i]
    return top_sum/bottom_sum

x1, y_amc1, y_edf1 = test_and_get_data(1)
x2, y_amc2, y_edf2 = test_and_get_data(2)
x3, y_amc3, y_edf3 = test_and_get_data(3)
x4, y_amc4, y_edf4 = test_and_get_data(4)
x5, y_amc5, y_edf5 = test_and_get_data(5)


# plot data
plt.subplots(1,2)
plt.subplot(1,2,1)
plt.plot(x2,y_amc2,'-bo', label="AMC")
plt.plot(x2,y_edf2,'-go', label="EDF-VD")
plt.xticks(x2)
plt.yticks(np.arange(0,1.1,step=0.1))
plt.xlabel("Total Utilization of Taskset")
plt.ylabel("% Schedulable")
plt.title("Crit. Factor = 2")

plt.subplot(1,2,2)
plt.plot(x2,y_amc4,'-bo', label="AMC")
plt.plot(x2,y_edf4,'-go', label="EDF-VD")
plt.xticks(x4)
plt.yticks(np.arange(0,1.1,step=0.1))
plt.xlabel("Total Utilization of Taskset")
plt.ylabel("% Schedulable")
plt.title("Crit. Factor = 4")

plt.suptitle('Figure 1. Schedulability of Tasksets')
plt.legend()
plt.show()

# weighted schedulability plot
w_amc = []
w_edf = []
x = list(range(1,6))
w_amc.append(calcaulate_weighted_schedulability(x1, y_amc1, 1))
w_edf.append(calcaulate_weighted_schedulability(x1, y_edf1, 1))
w_amc.append(calcaulate_weighted_schedulability(x2, y_amc2, 2))
w_edf.append(calcaulate_weighted_schedulability(x2, y_edf2, 2))
w_amc.append(calcaulate_weighted_schedulability(x3, y_amc3, 3))
w_edf.append(calcaulate_weighted_schedulability(x3, y_edf3, 3))
w_amc.append(calcaulate_weighted_schedulability(x4, y_amc4, 4))
w_edf.append(calcaulate_weighted_schedulability(x4, y_edf4, 4))
w_amc.append(calcaulate_weighted_schedulability(x5, y_amc5, 5))
w_edf.append(calcaulate_weighted_schedulability(x5, y_edf5, 5))

plt.plot(x, w_amc, '-bo', label='AMC')
plt.plot(x, w_edf, '-go', label='EDF-VD')
plt.xticks(x)
plt.xlabel("Criticality Factor")
plt.ylabel("Weighted Schedulability Score")
plt.title("Figure 2. Weighted Schedulability based on Crit. Factor")

plt.legend()
plt.show()