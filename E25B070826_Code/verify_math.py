"""Mathematical verification script for M3 Eigenvalues & Eigenvectors animation.

Verifies every matrix, characteristic polynomial, eigenvalue, eigenvector,
null-space system, substitution check, unit-square transformation, area
scaling, and unit-circle angle sweep used in the animation.
"""

import math
import numpy as np
import sympy as sp


def main() -> None:
    # Exact symbolic verification with SymPy
    lam = sp.Symbol("lambda")
    A_sym = sp.Matrix([[2, 1], [1, 2]])
    I_sym = sp.eye(2)

    print("=== 1. Matrix & Characteristic Polynomial (SymPy) ===")
    print("A =", A_sym.tolist())
    print("det(A) =", A_sym.det())
    print("trace(A) =", A_sym.trace())

    M_lam = A_sym - lam * I_sym
    print("A - lambda*I =", M_lam.tolist())

    char_poly_raw = sp.expand(M_lam.det())
    char_poly_factored = sp.factor(char_poly_raw)
    print("det(A - lambda*I) expanded =", char_poly_raw)
    print("det(A - lambda*I) factored =", char_poly_factored)

    assert sp.expand((2 - lam) ** 2 - 1) == char_poly_raw
    assert char_poly_raw == lam**2 - 4 * lam + 3
    assert sp.expand((lam - 1) * (lam - 3)) == char_poly_raw

    eigenvals = sp.solve(char_poly_raw, lam)
    print("Eigenvalues (ascending):", eigenvals)
    assert eigenvals == [1, 3]

    print("\n=== 2. Null Spaces & Eigenvectors (SymPy) ===")
    lam1 = 3
    M1 = A_sym - lam1 * I_sym
    v1 = sp.Matrix([1, 1])
    print(f"For lambda1 = {lam1}: A - 3I = {M1.tolist()}")
    assert M1 == sp.Matrix([[-1, 1], [1, -1]])
    assert M1 * v1 == sp.Matrix([0, 0])
    assert A_sym * v1 == lam1 * v1
    print(f"  Verify A * {tuple(v1)} = {tuple(A_sym * v1)} = {lam1} * {tuple(v1)}")

    lam2 = 1
    M2 = A_sym - lam2 * I_sym
    v2 = sp.Matrix([1, -1])
    print(f"For lambda2 = {lam2}: A - 1I = {M2.tolist()}")
    assert M2 == sp.Matrix([[1, 1], [1, 1]])
    assert M2 * v2 == sp.Matrix([0, 0])
    assert A_sym * v2 == lam2 * v2
    print(f"  Verify A * {tuple(v2)} = {tuple(A_sym * v2)} = {lam2} * {tuple(v2)}")

    # Check SymPy eigenvects() matches
    eig_info = A_sym.eigenvects()
    print("SymPy eigenvects:", [(val, mult, [tuple(vec) for vec in basis]) for val, mult, basis in eig_info])

    print("\n=== 3. Unit Square -> Parallelogram & Area Scaling ===")
    e1 = sp.Matrix([1, 0])
    e2 = sp.Matrix([0, 1])
    Ae1 = A_sym * e1
    Ae2 = A_sym * e2
    print(f"T(e1) = T(1,0) = {tuple(Ae1)}")
    print(f"T(e2) = T(0,1) = {tuple(Ae2)}")
    print(f"T(1,1) = {tuple(A_sym * sp.Matrix([1, 1]))}")
    area_unit = 1
    area_parallelogram = abs(A_sym.det()) * area_unit
    print(f"Unit square area = {area_unit}, transformed parallelogram area = {area_parallelogram}")
    assert area_parallelogram == lam1 * lam2 == 3

    print("\n=== 4. Numerical Check & Unit-Circle Angle Sweep (NumPy) ===")
    A_np = np.array([[2.0, 1.0], [1.0, 2.0]])
    w, V = np.linalg.eigh(A_np)
    print("NumPy eigenvalues:", w)
    print("NumPy unit eigenvectors (columns):\n", V)

    # Sample ordinary vectors used in Scene 1 & 3
    sample_vectors = [(1, 0), (0, 1), (1, 1), (1, -1), (2, 0), (-1, 2)]
    for vx, vy in sample_vectors:
        v = np.array([vx, vy], dtype=float)
        Av = A_np @ v
        cos_theta = np.clip(np.dot(v, Av) / (np.linalg.norm(v) * np.linalg.norm(Av)), -1.0, 1.0)
        angle_deg = math.degrees(math.acos(cos_theta))
        print(f"  v = ({vx:2d}, {vy:2d}) -> Av = ({Av[0]:4.1f}, {Av[1]:4.1f}), angle = {angle_deg:5.2f} deg")

    # Verify zero-angle directions on [0, 2*pi)
    thetas_deg = [45, 135, 225, 315]
    for deg in thetas_deg:
        rad = math.radians(deg)
        v = np.array([math.cos(rad), math.sin(rad)])
        Av = A_np @ v
        cos_theta = np.clip(np.dot(v, Av) / (np.linalg.norm(v) * np.linalg.norm(Av)), -1.0, 1.0)
        angle_deg = math.degrees(math.acos(cos_theta))
        scale = np.linalg.norm(Av) / np.linalg.norm(v)
        assert angle_deg < 1e-10, f"Expected 0 deg at {deg} deg, got {angle_deg}"
        print(f"  Eigen-direction theta = {deg:3d} deg: angle(v, Av) = {angle_deg:.2e} deg, ||Av||/||v|| = {scale:.1f}")

    print("\nALL MATHEMATICAL CHECKS PASSED.")


if __name__ == "__main__":
    main()
