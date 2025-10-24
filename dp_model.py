import math
from functools import lru_cache

def dp_cost(gaps, cut_cost=20, end_penalty_per_skein=20):
    UNDEF = (-1, -1)
    n = len(gaps)

    @lru_cache(maxsize=None)
    def cost(i, p1, p2, used1, used2):
        if i == n:
            return end_penalty_per_skein * (used1 + used2)

        _, e_i = gaps[i]

        # Skein A: 
        move_a = 0 if p1 == UNDEF else min(math.dist(p1, e_i), cut_cost)    # attach for free if not in use, otherwise choose minimum of cutting or floating
        if i != n-1:
            cost_a = move_a + cost(i + 1, gaps[i+1][0], p2, 1, used2)
        else: 
            cost_a = move_a + cost(i + 1, p1, p2, 1, used2)

        # Skein B:
        move_b = 0 if p2 == UNDEF else min(math.dist(p2, e_i), cut_cost)    # attach for free if not in use, otherwise choose minimum of cutting or floating
        if i != n-1:
            cost_b = move_b + cost(i + 1, p1, gaps[i+1][0], used1, 1)
        else: 
            cost_b = move_b + cost(i + 1, p1, p2, used1, 1)

        return cost_a if cost_a <= cost_b else cost_b       # choose the minimum cost of using either skein, default is skein A

    total_cost = cost(0, UNDEF, UNDEF, 0, 0)
    return total_cost
