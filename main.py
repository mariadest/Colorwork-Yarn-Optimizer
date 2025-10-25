import get_gaps as gg
import numpy as np
import dp_model as dp
import float_model as flo
import pandas as pd
import time
import sys, traceback, threading, queue
import multiprocessing as mp


sys.setrecursionlimit(50000)    # upping the recursion limit so the large charts actually finish

import multiprocessing as mp

def _worker_run(model, path, q):
    try:
        # keep your big-stack thread inside the subprocess if you need it
        res = run_big_experiment(model, path) if model == "dp" else run_experiment(model, path)
        q.put(("ok", res))
    except Exception as e:
        import traceback
        q.put(("err", (str(e), traceback.format_exc())))

def run_in_subprocess(model, path):
    q = mp.Queue()
    p = mp.Process(target=_worker_run, args=(model, path, q))
    p.start()
    p.join()
    status, payload = q.get()
    if status == "ok":
        return payload
    else:
        err, tb = payload
        raise RuntimeError(f"Child failed: {err}\n{tb}")
    
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
    print(f"Finished in time {round(runtime)}")
    return total, runtime, loose_ends, skeins_used, cuts, floats

# thread gets larger stack so greater recursion depth can be reached 
# 100x100 charts won't run otherwise :(
def run_big_experiment(model, path, stack_mb=128):
    threading.stack_size(stack_mb * 1024 * 1024)
    q = queue.Queue()
    def worker():
        try:
            res = run_experiment(model, path) 
            q.put(("ok", res))
        except Exception as e:
            q.put(("err", (e, traceback.format_exc())))
    t = threading.Thread(target=worker)
    t.start()
    t.join()
    status, payload = q.get()
    if status == "ok":
        return payload  
    else:
        e, tb = payload
        print("Error inside big-stack thread:\n" + tb)
        raise e


if __name__ == "__main__":
    mp.freeze_support()

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
    #cost, runtime, loose_ends, skeins_used, cuts, floats = run_big_experiment("dp", f"Patterns/100x100_0.25/100x100_0.25_#12.npy")
    results_all = []
    for model in models:
        for cluster_prob in cluster_probabilities:
            # 25x25
            for i in range(1, 21):
                cost, runtime, loose_ends, skeins_used, cuts, floats = run_experiment(
                    model, f"Patterns/25x25_{cluster_prob}/25x25_{cluster_prob}_#{i}.npy"
                )
                results_all.append({
                    "model": model,
                    "size": "25x25",
                    "cluster_prob": cluster_prob,
                    "pattern_id": i,
                    "cost": cost,
                    "time_s": runtime,
                    "loose_ends": loose_ends,
                    "skeins_used": skeins_used,
                    "cuts": cuts,
                    "floats": floats,
                })
                print(f"{model} solved 25x25_{cluster_prob}_#{i} with cost {cost}")

            # 50x50
            for i in range(1, 21):
                cost, runtime, loose_ends, skeins_used, cuts, floats = run_experiment(
                    model, f"Patterns/50x50_{cluster_prob}/50x50_{cluster_prob}_#{i}.npy"
                )
                results_all.append({
                    "model": model,
                    "size": "50x50",
                    "cluster_prob": cluster_prob,
                    "pattern_id": i,
                    "cost": cost,
                    "time_s": runtime,
                    "loose_ends": loose_ends,
                    "skeins_used": skeins_used,
                    "cuts": cuts,
                    "floats": floats,
                })
                print(f"{model} solved 50x50_{cluster_prob}_#{i} with cost {cost}")

            # 100x100
            for i in range(1, 21):
                cost, runtime, loose_ends, skeins_used, cuts, floats = run_in_subprocess(
                    model, f"Patterns/100x100_{cluster_prob}/100x100_{cluster_prob}_#{i}.npy"
                )
                results_all.append({
                    "model": model,
                    "size": "100x100",
                    "cluster_prob": cluster_prob,
                    "pattern_id": i,
                    "cost": cost,
                    "time_s": runtime,
                    "loose_ends": loose_ends,
                    "skeins_used": skeins_used,
                    "cuts": cuts,
                    "floats": floats,
                })
                print(f"{model} solved 100x100_{cluster_prob}_#{i} with cost {cost}")

    df = pd.DataFrame(results_all)
    df.to_csv("results_big.csv", index=False)
