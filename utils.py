#  util.py  使用中的一些工具：将训练数据变为dataloader，保存每一轮采样得到的蛋白序列，日志文件设置

import os
import torch
import torchvision
from PIL import Image
from matplotlib import pyplot as plt
from torch.utils.data import DataLoader
from torch.utils.data import WeightedRandomSampler
from protein_sequences_embedding import *
import time


device = torch.device('cuda:0')


def save_sequence(sequences, path, **kwargs):
    print("begin save sequence!")
    total_amino = torch.tensor([
        [0.15, -1.11, -1.35, -0.92, 0.02, -0.91, 0.36, -0.48],
        [0.18, -1.67, -0.46, -0.21, 0.00, 1.20, -1.61, -0.19],
        [-1.15, 0.67, -0.41, -0.01, -2.68, 1.31, 0.03, 0.56],
        [-1.18, 0.40, 0.10, 0.36, -2.16, -0.17, 0.91, 0.02],
        [1.52, 0.61, 0.96, -0.16, 0.25, 0.28, -1.33, -0.20],
        [-0.20, -1.53, -2.63, 2.28, -0.53, -1.18, 2.01, -1.34],
        [-0.43, -0.25, 0.37, 0.19, 0.51, 1.28, 0.93, 0.65],
        [1.27, -0.14, 0.30, -1.80, 0.30, -1.61, -0.16, -0.13],
        [-1.17, 0.70, 0.70, 0.80, 1.64, 0.67, 1.63, 0.13],
        [1.36, 0.07, 0.26, -0.80, 0.22, -1.37, 0.08, -0.62],
        [1.01, -0.53, 0.43, 0.00, 0.23, 0.10, -0.86, -0.68],
        [-0.99, 0.00, -0.37, 0.69, -0.55, 0.85, 0.73, -0.80],
        [0.22, -0.17, -0.50, 0.05, -0.01, -1.34, -0.19, 3.56],
        [-0.96, 0.12, 0.18, 0.16, 0.09, 0.42, -0.20, -0.41],
        [-1.47, 1.45, 1.24, 1.27, 1.55, 1.47, 1.30, 0.83],
        [-0.67, -0.86, -1.07, -0.41, -0.32, 0.27, -0.64, 0.11],
        [-0.34, -0.51, -0.55, -1.06, -0.06, -0.01, -0.79, 0.39],
        [0.76, -0.92, -0.17, -1.91, 0.22, -1.40, -0.24, -0.03],
        [1.50, 2.06, 1.79, 0.75, 0.75, -0.13, -1.01, -0.85],
        [0.61, 1.60, 1.17, 0.73, 0.53, 0.25, -0.96, -0.52],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    ]).to(device)
    
    alpha = 'ACDEFGHIKLMNPQRSTVWY-'
    seq_squeeze = torch.squeeze(sequences).to(device)     # 把维度是1的维度去掉
    protein_list = []

    for i in range(seq_squeeze.shape[0]):
        amino_seq = ''
        for j in range(seq_squeeze.shape[1]):
            min_dis = 100000000
            for k in range(len(total_amino)):
                temp_ed = torch.pairwise_distance(seq_squeeze[i][j], total_amino[k])
                temp_ed = temp_ed.to(device)
                if temp_ed < min_dis:
                    min_dis = temp_ed
                    index = k
            amino_seq += alpha[index]
        protein_list.append(amino_seq)

    with open(path, 'w') as fw:
        print(path)
        for i in range(len(protein_list)):
            fw.write('>id_{0}'.format(i))
            fw.write('\n')
            fw.write(protein_list[i])
            fw.write('\n')
    print("end save sequence!")


def get_data(args):
    seqs = read_seq_embedding(args.dataset_path)
    seqs = torch.tensor(seqs)
    seqs = torch.reshape(seqs, (-1, 1, 560, 8))         
    dataloader = DataLoader(seqs, batch_size=args.batch_size, shuffle=True, drop_last=True)
    return dataloader


def setup_logging(run_name):
    os.makedirs("models", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    os.makedirs(os.path.join("models", run_name), exist_ok=True)
    os.makedirs(os.path.join("results", run_name), exist_ok=True)
