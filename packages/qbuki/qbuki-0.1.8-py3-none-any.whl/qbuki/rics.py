import numpy as np
from .utils import *
import sympy
import sympy.liealgebras.type_a

def mercedes_benz_frame():
    return np.array([[r.real, r.imag] for r in [np.exp(2j*np.pi*i/3) for i in range(3)]]).T*np.sqrt(2/3)

def circular_shifts(v):
    shifts = [v]
    for i in range(len(v)-1):
        u = shifts[-1][:]
        u.insert(0, u.pop()) 
        shifts.append(u)
    return shifts

def icosahedron_vertices():
    phi = (1+np.sqrt(5))/2
    return [np.array(v) for v in 
               circular_shifts([0, 1, phi]) + \
               circular_shifts([0, -1, -phi]) + \
               circular_shifts([0, 1, -phi]) + \
               circular_shifts([0, -1, phi])]

def icosahedron_frame():
    vertices = icosahedron_vertices()
    keep = []
    for i, a in enumerate(vertices):
        for j, b in enumerate(vertices):
            if i != j and np.allclose(a, -b) and j not in keep:
                keep.append(i)
    vertices = [normalize(e) for i, e in enumerate(vertices) if i in keep]
    return np.array(vertices).T*np.sqrt(3/len(vertices))

def petersen_frame():
    petersen_vertices = ["u1", "u2", "u3", "u4", "u5", "v1", "v2", "v3", "v4", "v5"]
    petersen_graph = \
        {"u1": ["v1", "u2", "u5"],
        "u2": ["u1", "v2", "u3"],
        "u3": ["u2", "v3", "u4"],
        "u4": ["u3", "v4", "u5"],
        "u5": ["u4", "v5", "u1"],
        "v1": ["u1", "v4", "v3"],
        "v2": ["u2", "v4", "v5"],
        "v3": ["v5", "v1", "u3"],
        "v4": ["u4", "v1", "v2"],
        "v5": ["u5", "v3", "v2"]}
    petersen_gram = np.array([[1 if a == b else (\
                               -2/3 if b in petersen_graph[a] else \
                               1/6) for b in petersen_vertices]\
                                        for a in petersen_vertices]) 
    U, D, V = np.linalg.svd(petersen_gram)
    return (V[:4].T @ np.sqrt(np.diag(D[:4]))*np.sqrt(4/10)).T

def honey_frame(d, full=False):
    n = d*(d+1)/2
    A = sympy.liealgebras.type_a.TypeA(d)
    roots = [np.array(root) for root in A.positive_roots().values()]
    if full:
        roots.extend([-r for r in roots])
    U, D, V = np.linalg.svd(np.array(roots).T)
    return np.array([state/np.linalg.norm(state) for state in V[:d].T]).T*np.sqrt(d/n)
