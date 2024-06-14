import numpy as np
import pdb

# the VHSE-scales of a amino: VHSE1 and VHSE2: Hydrophobic properties, VHSE3 and VHSE4: Steric properties, VHSE5 to VHSE8: Electronic properties
total_amino = [
    [0.15, -1.11, -1.35, -0.92, 0.02, -0.91, 0.36, -0.48],      # amino_A
    [0.18, -1.67, -0.46, -0.21, 0.00, 1.20, -1.61, -0.19],      # amino_C
    [-1.15, 0.67, -0.41, -0.01, -2.68, 1.31, 0.03, 0.56],       # amino_D
    [-1.18, 0.40, 0.10, 0.36, -2.16, -0.17, 0.91, 0.02],        # amino_E
    [1.52, 0.61, 0.96, -0.16, 0.25, 0.28, -1.33, -0.20],        # amino_F
    [-0.20, -1.53, -2.63, 2.28, -0.53, -1.18, 2.01, -1.34],     # amino_G
    [-0.43, -0.25, 0.37, 0.19, 0.51, 1.28, 0.93, 0.65],         # amino_H
    [1.27, -0.14, 0.30, -1.80, 0.30, -1.61, -0.16, -0.13],      # amino_I
    [-1.17, 0.70, 0.70, 0.80, 1.64, 0.67, 1.63, 0.13],          # amino_K
    [1.36, 0.07, 0.26, -0.80, 0.22, -1.37, 0.08, -0.62],        # amino_L
    [1.01, -0.53, 0.43, 0.00, 0.23, 0.10, -0.86, -0.68],        # amino_M
    [-0.99, 0.00, -0.37, 0.69, -0.55, 0.85, 0.73, -0.80],       # amino_N
    [0.22, -0.17, -0.50, 0.05, -0.01, -1.34, -0.19, 3.56],      # amino_P
    [-0.96, 0.12, 0.18, 0.16, 0.09, 0.42, -0.20, -0.41],        # amino_Q
    [-1.47, 1.45, 1.24, 1.27, 1.55, 1.47, 1.30, 0.83],          # amino_R
    [-0.67, -0.86, -1.07, -0.41, -0.32, 0.27, -0.64, 0.11],     # amino_S
    [-0.34, -0.51, -0.55, -1.06, -0.06, -0.01, -0.79, 0.39],    # amino_T
    [0.76, -0.92, -0.17, -1.91, 0.22, -1.40, -0.24, -0.03],     # amino_V
    [1.50, 2.06, 1.79, 0.75, 0.75, -0.13, -1.01, -0.85],        # amino_W
    [0.61, 1.60, 1.17, 0.73, 0.53, 0.25, -0.96, -0.52],         # amino_Y
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]            # amino_gap
]


def read_seq_embedding(seq_file):
    seq_list = []
    seq = ''
    with open(seq_file, 'r') as fp:
        index = 0
        for line in fp:
            if line[0] != '>':
                index += 1
                seq = line[:-1]
                seq_array = get_seq_array(seq)
                seq_list.append(seq_array)
        print("统计蛋白质的序列一共有：", index)
    return np.array(seq_list)


def get_seq_array(seq):
    alpha = 'ACDEFGHIKLMNPQRSTVWY'
    input_array = np.zeros((560, 8))
    for i, val in enumerate(seq):
        if val in alpha:
            try:
                index = alpha.index(val)
                input_array[i] = total_amino[index]
            except ValueError:
                pdb.set_trace()
        else:
            input_array[i] = np.array([0.0] * 8)
    return input_array


