import numpy as np

import numpyqi

np_rng = np.random.default_rng()
hf_randc = lambda *size: np_rng.normal(size=size) + 1j*np_rng.normal(size=size)

def test_matrix_to_gellman_basis():
    for N0 in [3,4,5]:
        np0 = np.random.rand(N0,N0) + np.random.rand(N0,N0)*1j
        coeff = numpyqi.gellmann.matrix_to_gellmann_basis(np0, norm_I='sqrt(2/d)') #default
        tmp0 = numpyqi.gellmann.all_gellmann_matrix(N0)
        ret0 = sum(x*y for x,y in zip(coeff,tmp0))
        assert np.abs(np0-ret0).max()<1e-7
        for norm_I in ['1/d', 'sqrt(2/d)']:
            np1 = numpyqi.gellmann.matrix_to_gellmann_basis(np0, norm_I=norm_I)
            np2 = numpyqi.gellmann.gellmann_basis_to_matrix(np1, norm_I=norm_I)
            assert np.abs(np0-np2).max() < 1e-7

def test_all_gellmann_matrix():
    # https://arxiv.org/abs/1705.01523
    for d in [3,4,5]:
        all_term = numpyqi.gellmann.all_gellmann_matrix(d, with_I=False)
        for ind0,x in enumerate(all_term):
            for ind1,y in enumerate(all_term):
                assert abs(np.trace(x @ y)-2*(ind0==ind1)) < 1e-7

def test_trace0_orthongal_matrix():
    dim = 4
    N0 = 5
    np_rng = np.random.default_rng()
    theta = np_rng.normal(size=(dim**2-1,dim**2-1))
    tmp0 = numpyqi.param.real_matrix_to_special_unitary(theta, tag_real=True)[:N0]*(1/np.sqrt(2))
    z0 = numpyqi.gellmann.gellmann_basis_to_matrix(np.concatenate([tmp0[:N0], np.zeros((N0,1))], axis=1))
    assert np.abs(np.trace(z0, axis1=1, axis2=2)).max() < 1e-7
    assert np.abs(z0-z0.transpose(0,2,1).conj()).max() < 1e-7
    tmp0 = np.array([[np.trace(x@y) for y in z0] for x in z0])
    assert np.abs(np.eye(len(tmp0)) - tmp0).max() < 1e-7


def test_gellmann_basis_to_dm():
    for N0 in [3,4,5,6]:
        dm0 = numpyqi.random.rand_density_matrix(N0)
        tmp0 = numpyqi.gellmann.dm_to_gellmann_basis(dm0)
        assert np.abs(numpyqi.gellmann.gellmann_basis_to_dm(tmp0) - dm0).max() < 1e-7
