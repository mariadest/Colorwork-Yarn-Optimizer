import get_gaps as gg
import numpy as np
import dp_model as dp
import float_model as flo

def load_pattern(path):
    chart = np.load(path)
    return chart 


if __name__ == "__main__":

