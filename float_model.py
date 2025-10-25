import math

def one_skein_cost(gaps, max_float_length=20):
    loose_ends = 2  
    nr_of_cuts = 0
    nr_of_floats = 0
    cost = 20  # initial penalty for the loose ends at start and end

    for i in range(len(gaps)):
        current_gap = gaps[i]
        gap_len = math.dist(current_gap[0], current_gap[1])

        if gap_len <= max_float_length:
            cost += gap_len
            if gap_len != 0:    # don't count attaching a skein as a float
                nr_of_floats += 1
        else:
            cost += 20
            loose_ends += 2
            nr_of_cuts += 1

    return cost, loose_ends, nr_of_cuts, nr_of_floats

def two_skein_cost(gaps, cut_cost=20, end_penalty_per_skein=20):
    UNDEF = (-1, -1)
    n = len(gaps)

    p1, p2 = UNDEF, UNDEF   # skein 1 and skein 2 are initially not used
    used1 = used2 = 0
    cost = 0.0
    loose_ends = 0
    nr_of_floats = 0
    nr_of_cuts = 0

    for i, (b_i, e_i) in enumerate(gaps):
        
        cut_A = False
        cut_B = False
        # compute how expensive choosing skein A and skein B is 
        if p1 == UNDEF:
            move_a = 0.0
        elif math.dist(p1, e_i) > cut_cost:
            move_a = cut_cost
            cut_A = True
        else:
            move_a = math.dist(p1, e_i)
            
        if p2 == UNDEF:
            move_b = 0.0
        elif math.dist(p2, e_i) > cut_cost:
            move_b = cut_cost
            cut_B = True
        else:
            move_b = math.dist(p2, e_i)

        # choose the cheaper skein, default is skein A
        use_a = (move_a <= move_b)

        if use_a:
            if cut_A:
                loose_ends += 2
                nr_of_cuts += 1
            elif p1 != UNDEF and move_a > 0:    # don't count attaching a skein as a float
                nr_of_floats += 1
            cost += move_a
            used1 = 1
            # jump to the start of the next gap (as if you had knitted across the sequence of color)
            if i != n - 1:
                p1 = gaps[i + 1][0]
        else:
            if cut_B:
                loose_ends += 2
                nr_of_cuts += 1
            elif p2 != UNDEF and move_b > 0:
                nr_of_floats += 1
            cost += move_b
            used2 = 1
            if i != n - 1:
                p2 = gaps[i + 1][0]

    # end penalty per skein used
    skeins_used = used1 + used2
    cost += end_penalty_per_skein * skeins_used
    loose_ends += 2 * skeins_used
    return cost, loose_ends, skeins_used, nr_of_cuts, nr_of_floats

