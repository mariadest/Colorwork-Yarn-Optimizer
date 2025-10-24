# converts regular coordinates to knitting and crochet coordinates where the origin is at the bottom right
def convert_coordinates(row0, col0, R, C):
    i = R - row0        
    j = C - col0        
    return (i, j)

def snake_iter_indices(R, C):
    for k, r0 in enumerate(range(R - 1, -1, -1)):
        cols = range(C - 1, -1, -1) if k % 2 == 0 else range(0, C)
        for c0 in cols:
            yield r0, c0

def get_gaps(chart, color):
    R, C = len(chart), len(chart[0])

    gaps= []
    run_start = None
    last_match = None
    first_b = None
    prev_e = None
    for r0, c0 in snake_iter_indices(R, C):
        print(f"({r0}, {c0})")
        coord = convert_coordinates(r0, c0, R, C)
        if chart[r0][c0] == color:
            if run_start is None:
                run_start = coord
                if first_b is None:
                    first_b = coord
            last_match = coord
        else:
            if run_start is not None:
                # close run
                b_i, e_i = run_start, last_match  # type: ignore[assignment]
                if prev_e is None:
                    # first gap is (b1, b1)
                    gaps.append((b_i, b_i))
                else:
                    gaps.append((prev_e, b_i))
                prev_e = e_i
                run_start = None
                last_match = None

    # close trailing run
    if run_start is not None:
        b_i, e_i = run_start, last_match  # type: ignore[assignment]
        if prev_e is None:
            gaps.append((b_i, b_i))
        else:
            gaps.append((prev_e, b_i))
        prev_e = e_i

    return gaps
