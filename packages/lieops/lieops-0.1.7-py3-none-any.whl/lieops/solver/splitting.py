import numpy as np

class yoshida:
    
    def __init__(self, scheme=[1, 1/2]):
        '''
        Model a symplectic integrator which is symmetric according to Yoshida [1].
        
        Parameters
        ----------
        scheme: list, optional
            A list of length 2 defining the 2nd order symmetric symplectic integrator.
            If scheme = [s1, s2], then the integrator is assumed to have the form
            exp(h(A + B)) = exp(h*s2*A) o exp(h*s1*B) o exp(h*s2*A) + O(h**2)
            By default, the "leapfrog" scheme [1, 1/2] is used.
        
        References
        ----------
        [1] H. Yoshida: "Construction of higher order symplectic integrators", 
        Phys. Lett. A 12, volume 150, number 5,6,7 (1990).
        '''
        self.scheme = scheme
        
    @staticmethod
    def branch_factors(m: int, scheme=[1, 1/2]):
        '''
        Compute the quantities in Eq. (4.14) in Ref. [1].
        '''
        if m == 0:
            return scheme
        else:
            z0 = -2**(1/(m + 1))/(2 - 2**(1/(m + 1)))
            z1 = 1/(2 - 2**(1/(m + 1)))
            return z0, z1
        
    def build(self, n: int):
        '''
        Construct the coefficients for the symmetric Yoshida integrator according
        to Eqs. (4.12) and (4.14) in Ref. [1].
        
        Parameters
        ----------
        n: int
            The order of the integrator.
        '''
        z0, z1 = self.branch_factors(m=n, scheme=self.scheme)
        steps_k = [z1, z0, z1]
        for k in range(n):
            new_steps = []
            for step in steps_k:
                z0, z1 = self.branch_factors(m=n - k - 1, scheme=self.scheme)
                new_steps += [z1*step, z0*step, z1*step]
            steps_k = new_steps
            
        # In its final step, steps_k has the form
        # [a1, b1, a1, a2, b2, a2, a3, b3, a3, ..., bm, am]
        # where the aj's belong to the first operator and the bj's belong to the second operator.
        # Therefore, we have to add the inner aj's together. They belong to the index pairs
        # (2, 3), (5, 6), (8, 9), (11, 12), ...
        pair_start_indices = [j for j in range(2, len(steps_k) - 3, 3)]
        out = []
        k = 0
        while k < len(steps_k):
            if k in pair_start_indices:
                out.append(steps_k[k] + steps_k[k + 1])
                k += 2
            else:
                out.append(steps_k[k])
                k += 1
        return out
    
################
# General tools
################
    
def get_scheme_ordering(scheme):
    '''
    For a Yoshida-decomposition scheme obtain a list of indices defining
    the unique operators which have been created.
    '''
    # It is assumed that the given scheme defines an alternating decomposition of two operators. Therefore:
    scheme1 = [scheme[k] for k in range(0, len(scheme), 2)]
    scheme2 = [scheme[k] for k in range(1, len(scheme), 2)]
    unique_factors1 = np.unique(scheme1).tolist() # get unique elements but maintain order (see https://stackoverflow.com/questions/12926898/numpy-unique-without-sort)
    unique_factors2 = np.unique(scheme2).tolist()
    indices1 = [unique_factors1.index(f) for f in scheme1]
    indices2 = [unique_factors2.index(f) for f in scheme2]
    indices = []
    for k in range(len(scheme)):
        if k%2 == 0:
            indices.append(indices1[k//2])
        else:
            indices.append(indices2[(k - 1)//2] + max(indices1) + 1) # we add max(indices1) + 1 here to ensure the indices for operator 2 are different than for operator 1
    
    # Relabel the indices so that the first element has index 0 etc.
    max_index = 0
    index_map = {}
    for ind in indices:
        if ind in index_map.keys():
            continue
        else:
            index_map[ind] = max_index
            max_index += 1
    return [index_map[ind] for ind in indices]

    
def combine_equal_hamiltonians(hamiltonians):
    '''
    Combine Hamiltonians which are adjacent to each other and admit the same keys.
    '''
    n_parts = len(hamiltonians)
    new_hamiltonians = []
    k = 0
    while k < n_parts:
        part_k = hamiltonians[k]
        new_part = part_k
        for j in range(k + 1, n_parts):
            part_j = hamiltonians[j]
            if part_k.keys() == part_j.keys():
                new_part += part_j
                k = j
            else:
                break
        k += 1
        new_hamiltonians.append(new_part)
    return new_hamiltonians


def split_by_order(hamiltonian, scheme):
    '''
    Split a Hamiltonian according to its orders.
    '''
    maxdeg = hamiltonian.maxdeg()
    mindeg = hamiltonian.mindeg()
    hom_parts = [hamiltonian.homogeneous_part(k) for k in range(mindeg, maxdeg + 1)]
    hamiltonians = [hamiltonian]
    for k in range(len(hom_parts)):
        keys1 = [u for u in hom_parts[k].keys()]
        new_hamiltonians = []
        for e in hamiltonians:
            new_hamiltonians += [h for h in e.split(keys=keys1, scheme=scheme) if h != 0]
        hamiltonians = new_hamiltonians
    return combine_equal_hamiltonians(new_hamiltonians) # combine_equal_hamiltonians is necessary here, because otherwise there may be adjacent Hamiltonians having the same keys, using the above algorithm.


def recursive_monomial_split(*hamiltonians, scheme):
    '''
    Split a Hamiltonian into its monomials according to a given scheme,
    by recursively applying the scheme.
    '''
    new_hamiltonians = []
    recursion_required = False
    for h in hamiltonians:
        keys = list(h.keys())
        if len(keys) > 1:
            hsplits = h.split(keys=[keys[0]], scheme=scheme)
            recursion_required = True
        else:
            hsplits = [h]
        new_hamiltonians += hsplits
    if recursion_required:
        return recursive_monomial_split(*new_hamiltonians, scheme=scheme)
    else:
        return new_hamiltonians
