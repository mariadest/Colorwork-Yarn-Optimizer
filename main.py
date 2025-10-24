import get_gaps as gg
import numpy as np
import dp_model as dp
import float_model as flo
import pandas as pd
import sys 

sys.setrecursionlimit(100000)

def load_pattern(path):
    chart = np.load(path)
    return chart 

# possible models are:
#   f1s: float20 using one skein
#   f2s: float20 using two skeins
#   dp: dp model using two skeins
def run_experiment(model, path):
    print("start")
    chart = load_pattern(path)
    gaps_0 = gg.get_gaps(chart, 0)
    gaps_1 = gg.get_gaps(chart, 1)
    
    cost_0 = 0.0
    cost_1 = 0.0
    
    if model == "f1s":
        cost_0 = flo.one_skein_cost(gaps_0)
        cost_1 = flo.one_skein_cost(gaps_1)
    elif model == "f2s":
        cost_0 = flo.two_skein_cost(gaps_0)
        cost_1 = flo.two_skein_cost(gaps_1)
    elif model == "dp":
        cost_0 = dp.dp_cost(gaps_0)
        cost_1 = dp.dp_cost(gaps_1)
    
    total = cost_0 + cost_1           
    return round(total, 3)
            

if __name__ == "__main__":
    
    models = [
        "dp",
        "f1s",
        "f2s",
    ]
    
    categories = [
        "25x25_0.05",
        "25x25_0.25",
        "25x25_0.5",
        "25x25_0.75",
        "25x25_0.95",
        "50x50_0.05",
        "50x50_0.25",
        "50x50_0.5",
        "50x50_0.75",
        "50x50_0.95",        
        "100x100_0.05",
        "100x100_0.25",
        "100x100_0.5",
        "100x100_0.75",
        "100x100_0.95",
    ]

    results = []
    """for model in models:
        for category in categories:
            for i in range(1, 21):
                
                cost = run_experiment(model, f"Patterns/{category}/{category}_#{i}.npy")
            
                results.append({
                    "model": model,
                    "category": category,
                    "cost": cost
                })
                
                print(f"{model} solved {category}/{category}_#{i} with cost {cost}")
                
    df = pd.DataFrame(results)
    df.to_csv("experiment_cost_results.csv", index=False)"""
    
    cost = run_experiment("dp", "Patterns/100x100_0.05/100x100_0.05_#1.npy")
    print(cost)
