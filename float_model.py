import math

def one_skein_cost(gaps, max_float_length=20):
    cost = 20  # initial penalty for the loose ends at start and end

    for i in range(len(gaps)):
        current_gap = gaps[i]
        gap_len = math.dist(current_gap[0], current_gap[1])

        # Float if ≤ 20 stitches, cut if > 20 (can be adjusted in the function call but here we always use 20)
        if gap_len <= max_float_length:
            cost += gap_len
        else:
            cost += 20

    return cost

def two_skein_cost(gaps, cut_cost=20, end_penalty_per_skein=20):
    UNDEF = (-1, -1)
    n = len(gaps)

    p1, p2 = UNDEF, UNDEF   # skein 1 and skein 2 are initially not used
    used1 = used2 = 0
    cost = 0.0

    for i, (b_i, e_i) in enumerate(gaps):
        # compute how expensive choosing skein A and skein B is 
        move_a = 0.0 if p1 == UNDEF else min(math.dist(p1, e_i), cut_cost)
        move_b = 0.0 if p2 == UNDEF else min(math.dist(p2, e_i), cut_cost)

        # choose the cheaper skein, default is skein A
        use_a = (move_a <= move_b)

        if use_a:
            cost += move_a
            used1 = 1
            # jump to the start of the next gap (as if knitting across the sequence of color)
            if i != n - 1:
                p1 = gaps[i + 1][0]
        else:
            cost += move_b
            used2 = 1
            if i != n - 1:
                p2 = gaps[i + 1][0]

    # end penalty per skein used
    cost += end_penalty_per_skein * (used1 + used2)
    return cost

