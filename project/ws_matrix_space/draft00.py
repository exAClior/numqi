import time
import numpy as np
import torch
import scipy.linalg

import numqi

dimA = 3
dimB = 3
dimC = 3
np_list = numqi.matrix_space.get_completed_entangled_subspace((dimA, dimB, dimC), kind='quant-ph/0409032')[0]

# mat0 = np_list.reshape(-1,dimA*dimB, dimC)
# # mat0 = np_list.transpose(0,1,3,2).reshape(-1,dimA*dimC,dimB)
# z0 = numqi.matrix_space.has_rank_hierarchical_method(mat0, rank=2, hierarchy_k=4)

# mat0 = np_list.reshape(-1,dimA*dimB, dimC)
# basis,basis_orth,space_char = numqi.matrix_space.get_matrix_orthogonal_basis(mat0, field='complex')
# model = numqi.matrix_space.DetectRankModel(basis_orth, space_char, rank=1)
# theta_optim = numqi.optimize.minimize(model, 'uniform', num_repeat=3, tol=1e-7)

# mat0 = np_list.reshape(-1,dimA*dimB, dimC)
# basis_orth = numqi.matrix_space.get_vector_orthogonal_basis(np_list.reshape(np_list[0], -1)).reshape(-1, dimA,dimB,dimC)
# basis,basis_orth,space_char = numqi.matrix_space.get_matrix_orthogonal_basis(mat0, field='complex')
# basis_orth = basis_orth.reshape(-1, dimA, dimB, dimC)


basis_orth = numqi.matrix_space.get_vector_orthogonal_basis(np_list.reshape(np_list.shape[0], -1)).reshape(-1, dimA,dimB,dimC)
print(f'[{dimA}x{dimB}x{dimC}] detect rank=2')
t0 = time.time()
model = numqi.matrix_space.DetectCPRankModel(basis_orth, rank=2)
theta_optim = numqi.optimize.minimize(model, 'uniform', num_repeat=3, tol=1e-12)
print(f'elapsed time: {time.time()-t0:3f}s', '\n')

print(f'[{dimA}x{dimB}x{dimC}] detect rank=1')
model = numqi.matrix_space.DetectCPRankModel(basis_orth, rank=1)
theta_optim = numqi.optimize.minimize(model, 'uniform', num_repeat=3, tol=1e-12)
print(f'elapsed time: {time.time()-t0:3f}s', '\n')


def demo_time_usage():
    case_list = [(2,2,2,2), (2,2,3,2), (2,2,4,2), (2,2,5,2), (2,2,6,2), (2,2,7,2),
                (2,2,8,2), (2,2,9,2), (2,3,3,3), (2,3,4,3), (2,3,5,3), (3,3,3,4)]
    kwargs = dict(theta0='uniform', num_repeat=3, tol=1e-12, print_every_round=0)
    for dimA,dimB,dimC,_ in case_list:
        np_list = numqi.matrix_space.get_completed_entangled_subspace((dimA, dimB, dimC), kind='quant-ph/0409032')[0]
        t0 = time.time()
        basis_orth = numqi.matrix_space.get_vector_orthogonal_basis(np_list.reshape(np_list.shape[0], -1)).reshape(-1, dimA,dimB,dimC)
        model = numqi.matrix_space.DetectCPRankModel(basis_orth, rank=2)
        theta_optim2 = numqi.optimize.minimize(model, **kwargs)
        model = numqi.matrix_space.DetectCPRankModel(basis_orth, rank=1)
        theta_optim1 = numqi.optimize.minimize(model, **kwargs)
        tmp0 = time.time()-t0
        print(f'[{dimA}x{dimB}x{dimC}][{tmp0:.3f}s] loss(r=2)= {theta_optim2.fun:.4e}, loss(r=1)= {theta_optim1.fun:.4e}')
        # [2x2x2][0.095s] loss(r=2)= 1.8304e-14, loss(r=1)= 2.5000e-01
        # [2x2x3][0.087s] loss(r=2)= 5.6645e-14, loss(r=1)= 9.9242e-02
        # [2x2x4][0.091s] loss(r=2)= 1.7311e-13, loss(r=1)= 4.5039e-02
        # [2x2x5][0.140s] loss(r=2)= 2.1488e-13, loss(r=1)= 2.2597e-02
        # [2x2x6][0.165s] loss(r=2)= 1.4117e-13, loss(r=1)= 1.2303e-02
        # [2x2x7][0.244s] loss(r=2)= 9.6170e-14, loss(r=1)= 7.1707e-03
        # [2x2x8][0.223s] loss(r=2)= 3.6233e-13, loss(r=1)= 4.4234e-03
        # [2x2x9][0.408s] loss(r=2)= 7.7931e-13, loss(r=1)= 2.8611e-03
        # [2x3x3][0.114s] loss(r=2)= 4.5884e-14, loss(r=1)= 3.5569e-02
        # [2x3x4][0.137s] loss(r=2)= 3.2846e-13, loss(r=1)= 1.4135e-02
        # [2x3x5][0.202s] loss(r=2)= 1.6536e-13, loss(r=1)= 6.1101e-03
        # [3x3x3][0.178s] loss(r=2)= 5.9082e-13, loss(r=1)= 1.1905e-02
