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
    start_time = time.perf_counter()
    print("start:", model, path)
    chart = load_pattern(path)
    gaps_0 = gg.get_gaps(chart, 0)
    gaps_1 = gg.get_gaps(chart, 1)

    if model == "f1s":
        cost_0, loose_ends_0, cuts_0, floats_0 = flo.one_skein_cost(gaps_0)
        cost_1, loose_ends_1, cuts_1, floats_1 = flo.one_skein_cost(gaps_1)
        skeins_used_0 = 1    # always use one skein per color
        skeins_used_1 = 1
    elif model == "f2s":
        cost_0, loose_ends_0, skeins_used_0, cuts_0, floats_0 = flo.two_skein_cost(gaps_0)
        cost_1, loose_ends_1, skeins_used_1, cuts_1, floats_1 = flo.two_skein_cost(gaps_1)
    elif model == "dp":
        cost_0, loose_ends_0, skeins_used_0, cuts_0, floats_0 = dp.dp_cost(gaps_0)
        cost_1, loose_ends_1, skeins_used_1, cuts_1, floats_1 = dp.dp_cost(gaps_1)

    #print(f"Experiment took {time.time() - start_time}s")
    total = round(cost_0 + cost_1, 3)
    runtime = round(time.perf_counter() - start_time, 5)
    loose_ends = loose_ends_0 + loose_ends_1
    skeins_used = skeins_used_0 + skeins_used_1
    cuts = cuts_0 + cuts_1
    floats = floats_0 + floats_1
    return total, runtime, loose_ends, skeins_used, cuts, floats

# thread gets larger stack so greater recursion depth can be reached 
# 100x100 charts won't run otherwise :(
def run_big_experiment(model, path, stack_mb=64):
    threading.stack_size(stack_mb * 1024 * 1024)  
    q = queue.Queue()   # used to store the results

    def worker():
        try:
            cost, runtime = run_experiment(model, path)
            q.put(("ok", cost, runtime))
        except Exception as e:
            q.put(("err", (e, traceback.format_exc())))

    t = threading.Thread(target=worker)     # start experiment in new thread
    t.start()
    t.join()        # wait for thread to be done

    status, cost, runtime = q.get()
    if status == "ok":
        return cost, runtime
    else:
        e, tb = cost
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
    
    cluster_probabilities = [
        "0.05",
        "0.25",
        "0.5",
        "0.75",
        "0.95"
    ]
    cluster_probabilities = [0.05, 0.95]

    """results_small = []
    for model in models:
        for cluster_prob in cluster_probabilities:
            for i in range(1, 3):
                cost, runtime, loose_ends, skeins_used, cuts, floats = run_experiment(model, f"Patterns/25x25_{cluster_prob}/25x25_{cluster_prob}_#{i}.npy")
                results_small.append({
                    "model": model,
                    "cluster probability": cluster_prob,
                    "chart number": i,
                    "cost": cost,
                    "time": runtime,
                    "loose ends": loose_ends,
                    "skeins used": skeins_used,
                    "cuts": cuts,
                    "floats": floats
                })
                print(f"{model} solved 25x25_{cluster_prob}_#{i} with cost {cost}")

    df = pd.DataFrame(results_small)
    df.to_csv("25x25_results.csv", index=False)"""
    
    """results_medium = []
    for model in models:
        for cluster_prob in cluster_probabilities:
            for i in range(1, 21):
                cost, runtime = run_experiment(model, f"Patterns/50x50_{cluster_prob}/50x50_{cluster_prob}_#{i}.npy")
                results_medium.append({
                    "model": model,
                    "cluster probability": cluster_prob,
                    "chart number": i,
                    "cost": cost,
                    "time": runtime,
                })
                print(f"{model} solved 50x50_{cluster_prob}_#{i} with cost {cost}")

    df = pd.DataFrame(results_medium)
    df.to_csv("50x50_results.csv", index=False)
    
    results_large = []
    for model in models:
        for cluster_prob in cluster_probabilities:
            for i in range(1, 21):
                cost, runtime = run_big_experiment(model, f"Patterns/100x100_{cluster_prob}/100x100_{cluster_prob}_#{i}.npy")
                results_large.append({
                    "model": model,
                    "cluster probability": cluster_prob,
                    "chart number": i,
                    "cost": cost,
                    "time": runtime,
                })
                print(f"{model} solved 100x100_{cluster_prob}_#{i} with cost {cost}")

    df = pd.DataFrame(results_large)
    df.to_csv("100x100_results.csv", index=False)"""
