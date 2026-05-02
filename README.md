# **Install Requirements**
```bash
pip install -r requirements.txt
```
# **Change Variables (Optional)**
In main.py:
* Change 'num_tasks' to however many tasks you want within a task set (half will be high criticality)
* Change 'util_inc' to change at what utilizations 1000 tasksets will be run at each time (for example, 0.1 will generate tasksets at U=0.1, 0.2, 0.3 ... 0.9, 1)

Then, simply run main.py.
