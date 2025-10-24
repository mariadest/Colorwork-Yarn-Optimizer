import get_gaps as gg
import numpy as np
import dp_model as dp
import float_model as flo
import pandas as pd
import time

import sys, threading, traceback, queue

sys.setrecursionlimit(50000)    # upping the recursion limit so the large charts actually finish

def load_pattern(path):
    return np.load(path)

# Base version (small patterns)
def run_experiment(model, path):
    start_time = time.time() 
    print("start:", model, path)
    chart = load_pattern(path)
    gaps_0 = gg.get_gaps(chart, 0)
    gaps_1 = gg.get_gaps(chart, 1)

    if model == "f1s":
        cost_0 = flo.one_skein_cost(gaps_0)
        cost_1 = flo.one_skein_cost(gaps_1)
    elif model == "f2s":
        cost_0 = flo.two_skein_cost(gaps_0)
        cost_1 = flo.two_skein_cost(gaps_1)
    elif model == "dp":
        cost_0 = dp.dp_cost(gaps_0)
        cost_1 = dp.dp_cost(gaps_1)

    print(f"Experiment took {time.time() - start_time}s")
    return round(cost_0 + cost_1, 3)

# thread gets larger stack so greater recursion depth can be reached 
# 100x100 charts won't run otherwise :(
def run_big_experiment(model, path, stack_mb=64):
    threading.stack_size(stack_mb * 1024 * 1024)  
    q = queue.Queue()   # used to store the results

    def worker():
        try:
            result = run_experiment(model, path)
            q.put(("ok", result))
        except Exception as e:
            q.put(("err", (e, traceback.format_exc())))

    t = threading.Thread(target=worker)     # start experiment in new thread
    t.start()
    t.join()        # wait for thread to be done

    status, value = q.get()
    if status == "ok":
        return value
    else:
        e, tb = value
        print("Error inside big-stack thread:\n" + tb)
        raise e


if __name__ == "__main__":

    models = [
        "dp",
        "f1s",
        "f2s",
    ]
    
    small_categories = [
        "25x25_0.05",
        "25x25_0.25",
        "25x25_0.5",
        "25x25_0.75",
        "25x25_0.95", 
    ]

    medium_categories = [
        "50x50_0.05",
        "50x50_0.25",
        "50x50_0.5",
        "50x50_0.75",
        "50x50_0.95", 
    ]
    
    large_categories = [
        "100x100_0.05",
        "100x100_0.25",
        "100x100_0.5",
        "100x100_0.75",
        "100x100_0.95", 
    ]

    results = []
    for model in models:
        for category in medium_categories:
            for i in range(1, 21):
                cost = run_experiment(model, f"Patterns/{category}/{category}_#{i}.npy")
                results.append({
                    "model": model,
                    "chart number": i,
                    "cost": cost
                })
                print(f"{model} solved {category}/{category}_#{i} with cost {cost}")

    df = pd.DataFrame(results)
    df.to_csv("50x50_results.csv", index=False)
    
    """for model in models:
        for category in large_categories:
            for i in range(1, 21):
                cost = run_big_experiment(model, f"Patterns/{category}/{category}_#{i}.npy")
                results.append({
                    "model": model,
                    "chart number": i,
                    "cost": cost
                })
                print(f"{model} solved {category}/{category}_#{i} with cost {cost}")

    df = pd.DataFrame(results)
    df.to_csv("100x100_results.csv", index=False)"""
