import math
from functools import lru_cache

def dp_cost(gaps, cut_cost=20, skein_penalty=20):
    UNDEF = (-1, -1)
    n = len(gaps)
    
    def dist(a, b):
        return math.dist(a, b)

    @lru_cache(maxsize=None)
    def cost(i, p1, p2, used1, used2):
        # base case: reached when all gaps have been looked at
        if i == n:
            skeins_used = used1 + used2
            loose_ends = 2 * skeins_used
            total_cost = skein_penalty * skeins_used
            return total_cost, loose_ends, skeins_used, 0, 0

        _, e_i = gaps[i]

        # CHOOSE BETWEEN WHICH SKEIN TO USE 

        # Skein A: 
        move_a = 0 if p1 == UNDEF else min(math.dist(p1, e_i), cut_cost)    # attach for free if not in use, otherwise choose minimum of cutting or floating
        if p1 is UNDEF:
            move_a = 0.0        # can attach for free if we use a new skein
            cut_a = False
            float_a = False
        else:
            d = dist(p1, e_i)
            # choose between cutting and floating
            cut_a = d > cut_cost
            move_a = cut_cost if cut_a else d
            float_a = (d > 0 and not cut_a)
 
        if i != n - 1:
            sub_a = cost(i + 1, gaps[i + 1][0], p2, 1, used2)
        else:
            sub_a = cost(i + 1, p1, p2, 1, used2)

        sub_cost_a, sub_loose_a, sub_skeins_a, sub_cuts_a, sub_floats_a = sub_a
        total_cost_a  = move_a + sub_cost_a
        total_loose_a = sub_loose_a + (2 if cut_a else 0)
        total_cuts_a  = sub_cuts_a + (1 if cut_a else 0)
        total_floats_a = sub_floats_a + (1 if float_a else 0)

        # Skein B:
        if p2 is UNDEF:
            move_b = 0.0
            cut_b = False
            float_b = False
        else:
            d = dist(p2, e_i)
            cut_b = d > cut_cost
            move_b = cut_cost if cut_b else d
            float_b = (d > 0 and not cut_b)

        if i != n - 1:
            sub_b = cost(i + 1, p1, gaps[i + 1][0], used1, 1)
        else:
            sub_b = cost(i + 1, p1, p2, used1, 1)

        sub_cost_b, sub_loose_b, sub_skeins_b, sub_cuts_b, sub_floats_b = sub_b
        total_cost_b  = move_b + sub_cost_b
        total_loose_b = sub_loose_b + (2 if cut_b else 0)
        total_cuts_b  = sub_cuts_b + (1 if cut_b else 0)
        total_floats_b = sub_floats_b + (1 if float_b else 0)
            
        # choose which skein results in smaller cost
        if (total_cost_a, total_loose_a) <= (total_cost_b, total_loose_b):
            return total_cost_a, total_loose_a, sub_skeins_a, total_cuts_a, total_floats_a
        else:
            return total_cost_b, total_loose_b, sub_skeins_b, total_cuts_b, total_floats_b

    return cost(0, UNDEF, UNDEF, 0, 0)
