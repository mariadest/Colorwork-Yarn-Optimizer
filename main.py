import get_gaps as gg
import numpy as np
import dp_model as dp
import float20 as c20
import OBSOLETE2 as dp1
import OBSOLETE1 as c202

def load_pattern(path):
    chart = np.load(path)
    return chart 


if __name__ == "__main__":
    chart = load_pattern("test.npy")
    #chart = load_pattern("50x50_0.95_#1.npy")
    gaps_col1 = gg.get_gaps(chart, 0)
    #print(gaps_col1)
    #print(c20.float20(gaps_col1))
    """cost = dp.dp_cost(gaps_col1)
    print(cost)
    total = c20.float20(gaps_col1)
    print(total)"""
    """
    gaps_col2 = gg.get_gaps(chart, 1)
    
    total, actions = dp.dp_cost(gaps_col1)
    print(f"cost dp: {total}")
    #print(actions)
    total, _ = dp1.dp_cost_one_skein(gaps_col1)
    print(f"cost dp one skein: {total}")
    
    cost = c20.float20(gaps_col1)

    print(f"cost float20: {cost}")
    
    cost = c202.float20_two_skeins(gaps_col1)
    print(f"cost float20 2 skein: {cost}")"""
