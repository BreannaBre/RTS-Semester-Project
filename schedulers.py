import math

# for readability of taskset tuples
PERIOD = 0
CRITICALITY = 1
C_LOW = 2
C_HIGH = 3
def test_schedulability_EDF_VD(taskset):
    # utilization = summation of C(criticality_first)/period
    # no hi_low util since C_low=C_high on low critical tasks
    util_low_low = 0
    util_low_hi = 0
    util_hi_hi = 0
    # determine all listed utilizations
    for i in range(len(taskset)):
        if taskset[i][CRITICALITY]:
            util_low_hi += taskset[i][C_LOW]/taskset[i][PERIOD]
            util_hi_hi += taskset[i][C_HIGH]/taskset[i][PERIOD]
        else:
            util_low_low += taskset[i][C_LOW]/taskset[i][PERIOD]
    # first, check necessary schedulability criteria for EDF-VD:
    if util_low_low + util_low_hi <= 1 and util_hi_hi <= 1:
        # checking for lower bound of scaling factor x verifies that deadlines are met in LO mode
        # checking for upper bound of scaling factor x verifies that deadlines are met in HI mode
        low_x_bound = util_low_hi/(1-util_low_low)
        high_x_bound = (1-util_hi_hi)/util_low_low
        x = 1-(util_hi_hi-util_low_hi)
        if x >= low_x_bound and x <= high_x_bound:
            return True
    return False

# NOTE: since we don't care about response times for this test, we return a bool instead
# if you want response times, change "return True" to "return response_times"
def test_schedulability_AMC(taskset):
    # sort by period for priority
    taskset.sort()
    response_times = []

    for i in range(len(taskset)):
        # check if ALL higher priority tasks than i meet first criteria (C_LOW=C_HIGH)
        first_criteria_met = True
        for j in range(i):
            if taskset[j][C_LOW] != taskset[j][C_HIGH]:
                first_criteria_met = False
                break
        if first_criteria_met:
            # if met, perform standard real-time analysis
            r = 0
            new_r = 1
            # loop until convergence (or infinity)
            while new_r != r:
                r = new_r
                r_summation = 0
                for j in range(i):
                    r_summation += math.ceil(r/taskset[j][PERIOD])*taskset[j][C_LOW]
                new_r = taskset[i][C_LOW] + r_summation
                if new_r == float("inf"):
                    return False
            # if response time < deadline(period), then it's not schedulable
            if r > taskset[i][0]:
                return False
            else:
                response_times.append(r)
                continue

        # second criteria to (alternatively) check: Criticality(j)=Criticality(i)
        second_criteria_met = True
        for j in range(i):
            if taskset[j][CRITICALITY] != taskset[i][CRITICALITY]:
                second_criteria_met = False
        if second_criteria_met:
            # standard real-time analysis but slightly different
            r = 0
            new_r = 1
            # loop until convergence
            while new_r != r:
                r = new_r
                r_summation = 0
                # WGET used is based on the task i's criticality
                if taskset[i][CRITICALITY]:
                    c_to_use = C_HIGH
                else:
                    c_to_use = C_LOW

                for j in range(i):
                    r_summation += math.ceil(r / taskset[j][PERIOD]) * taskset[j][c_to_use]
                new_r = taskset[i][c_to_use] + r_summation
                if new_r == float("inf"):
                    return False
            # again, not schedulable if response time > period
            if r > taskset[i][PERIOD]:
                return False
            else:
                response_times.append(r)
                continue
        # gross algorithm to examine all possible MC instances if other criteria do not match
        else:
            # find r_low as an upper bound for mode switch time
            r_low = 0
            new_r = 1
            # loop until convergence
            while new_r != r_low:
                r_low = new_r
                r_summation = 0
                for j in range(i):
                    r_summation += math.ceil(r_low / taskset[j][PERIOD]) * taskset[j][C_LOW]
                new_r = taskset[i][C_LOW] + r_summation
                if new_r == float("inf"):
                    return False

            # find critical points for when mode switches
            critical_mode_points = {0, r_low}
            for j in range(i):
                for val in range(0, math.ceil(r_low/taskset[j][PERIOD])):
                    v = val*taskset[j][PERIOD]
                    if v < r_low:
                        critical_mode_points.add(v)
            # iterate though all critical points to find r_k
            max_rk = 0
            for crit_t in sorted(critical_mode_points):
                r_kg = r_low
                while True:
                    # find low and high interference
                    inf_low = 0
                    inf_hi = 0
                    for j in range(i):
                        inf_low += math.ceil(min(crit_t, r_kg)/taskset[j][PERIOD])*taskset[j][C_LOW]
                        if taskset[j][1]:
                            inf_hi += math.ceil(r_kg/taskset[j][PERIOD])*taskset[j][C_HIGH]

                    new_r = taskset[i][C_HIGH] + inf_low + inf_hi
                    if new_r > taskset[i][PERIOD]:
                        return False
                    if new_r == r_kg:
                        break
                    r_kg = new_r
                max_rk = max(max_rk, r_kg)
            response_times.append(max_rk)
    return True