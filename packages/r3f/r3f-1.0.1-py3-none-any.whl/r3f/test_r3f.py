import numpy as np
import matplotlib.pyplot as plt
import r3f

# --------------------
# General Array Checks
# --------------------

def input_vector(func):
    try: # ragged list
        vec = [[1, 2], [1, 2, 3]]
        func(vec)
        assert False
    except TypeError:
        assert True
    try: # wrong vector dimensions
        vec = np.random.randn(3, 3, 3)
        func(vec)
        assert False
    except TypeError:
        assert True
    try: # wrong vector shape
        vec = np.eye(2)
        func(vec)
        assert False
    except ValueError:
        assert True


def input_axang(func):
    try: # ragged list
        ax = [[1, 2], [1, 2, 3]]
        func(ax, np.array([0.1, 0.2]))
        assert False
    except TypeError:
        assert True
    try: # good list
        ax = [1, 2, 4]
        func(ax, 1.0)
        assert True
    except TypeError:
        assert False
    try: # wrong axis dimensions
        ax = 5
        func(ax, 1.0)
        assert False
    except TypeError:
        assert True
    try: # wrong axis shape
        ax = np.eye(2)
        func(ax, 1.0)
        assert False
    except ValueError:
        assert True
    try: # list angle type
        ax = np.array([1, 2, 3])
        func(ax, [1.0])
        assert True
    except TypeError:
        assert False
    try: # angle dimensions too many
        ax = np.array([[1, 2], [3, 4], [5, 6]])
        ang = np.array([[1, 2], [3, 4], [5, 6]])
        func(ax, ang)
        assert False
    except TypeError:
        assert True
    try: # length mismatch
        ax = np.array([[1, 2], [3, 4], [5, 6]])
        ang = np.array([0.1, 0.2, 0.3])
        func(ax, ang)
        assert False
    except TypeError:
        assert True


def input_rpy(func):
    A = np.random.randn(3, 1)
    v = np.array([0.1, 0.2, 0.3])
    s = 5.0
    try: # wrong r dimensions
        func(A, v, v)
        assert False
    except TypeError:
        assert True
    try: # wrong p dimensions
        func(v, np.zeros(3, 3), v)
        assert False
    except TypeError:
        assert True
    try: # wrong y dimensions
        func(v, v, A)
        assert False
    except TypeError:
        assert True
    try: # length mismatch
        func(v, v, np.array([1, 1, 1, 1]))
        assert False
    except ValueError:
        assert True
    try: # type mismatch
        func(2.0, v, 3.0)
        assert False
    except TypeError:
        assert True


def input_dcm(func):
    # Check is_square.
    A = np.array([1, 2, 3])
    B = np.array([
        [1, 3, 6],
        [7, 5, 2]])
    C = np.array([
        [1, 3, 6],
        [7, 5, 2],
        [9, 11, 13]])
    assert r3f.is_square(A) is False
    assert r3f.is_square(B) is False
    assert r3f.is_square(C) is True
    assert r3f.is_square(C, 2) is False
    D = np.array([
        [[1, 3, 6],
        [7, 5, 2],
        [9, 11, 13]],
        [[13, 1, 11],
        [3, 9, 6],
        [2, 7, 5]]])
    assert r3f.is_square(D) is True

    # Check is_ortho.
    A = np.eye(3)
    B = np.eye(3)
    B[2, 2] += 1e-7
    C = np.eye(3)
    C[2, 2] += 1e-8
    assert r3f.is_ortho(A) is True
    assert r3f.is_ortho(B) is False
    assert r3f.is_ortho(C) is True
    try:
        D = np.array([2, 3, 5])
        r3f.is_ortho(D)
        assert False
    except:
        assert True
    E = np.array([
        [[1, 3, 6],
        [7, 5, 2],
        [9, 11, 13]],
        [[13, 1, 11],
        [3, 9, 6],
        [2, 7, 5]]])
    assert r3f.is_ortho(E) is False
    F = np.array([
        [[1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]],
        [[0, 0, -1],
        [0, 1, 0],
        [1, 0, 0]]])
    assert r3f.is_ortho(F) is True


def input_quat(func):
    try: # wrong dimensions
        func(np.array([[[0]]]))
        assert False
    except TypeError:
        assert True
    try: # wrong length
        func(np.array([1, 2, 3]))
        assert False
    except ValueError:
        assert True

# -----------------------------------
# Attitude-representation Conversions
# -----------------------------------

def test_axis_angle_vector():
    # Test inputs.
    input_axang(r3f.axis_angle_to_vector)
    input_vector(r3f.vector_to_axis_angle)

    # rotation about positive vector
    ax = np.array([1, 1, 1])
    ang = 2
    vec = r3f.axis_angle_to_vector(ax, ang)
    assert vec[0] == 2
    assert vec[1] == 2
    assert vec[2] == 2

    # multiple rotations
    ax = np.array([
        [1, 0, 0, 1],
        [0, 1, 0, 1],
        [0, 0, 1, 1]])
    ang = np.array([2, 2, 2, 2])
    vec = r3f.axis_angle_to_vector(ax, ang)
    print(vec)
    assert (vec == np.array([
        [2, 0, 0, 2],
        [0, 2, 0, 2],
        [0, 0, 2, 2]])).all()

    # single rotation
    c = np.array([1, 2, 4])
    ax, ang = r3f.vector_to_axis_angle(c)
    AX = np.array([0.21821789023599238127, 0.43643578047198476253,
            0.87287156094396952506])
    assert np.allclose(ax, AX)
    assert np.allclose(ang, 4.58257569495584000659)

    # multiple rotations
    d = np.array([
        [1, 2],
        [1, 2],
        [1, 2]])
    ax, ang = r3f.vector_to_axis_angle(d)
    rt3 = np.sqrt(3)
    rt12 = np.sqrt(12)
    assert np.allclose(ang, np.array([rt3, rt12]))
    assert np.allclose(ax[:, 0], 1/rt3)
    assert np.allclose(ax[:, 1], 2/rt12)
    d1 = r3f.axis_angle_to_vector(ax, ang)
    assert np.allclose(d, d1)


def test_rpy_axis_angle():
    # Test inputs.
    input_rpy(r3f.rpy_to_axis_angle)
    input_axang(r3f.axis_angle_to_rpy)

    # Test individual axes.
    ax, ang = r3f.rpy_to_axis_angle(0, 0, np.pi/4)
    assert np.allclose(ax, np.array([0, 0, 1]))
    assert np.allclose(ang, np.pi/4)
    ax, ang = r3f.rpy_to_axis_angle(0, np.pi/4, 0)
    assert np.allclose(ax, np.array([0, 1, 0]))
    assert np.allclose(ang, np.pi/4)
    ax, ang = r3f.rpy_to_axis_angle(np.pi/4, 0, 0)
    assert np.allclose(ax, np.array([1, 0, 0]))
    assert np.allclose(ang, np.pi/4)

    # Test vectorized reciprocity.
    N = 3
    R = np.random.uniform(-np.pi, np.pi, N)
    P = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, N)
    Y = np.random.uniform(-np.pi, np.pi, N)
    ax, ang = r3f.rpy_to_axis_angle(R, P, Y)
    r, p, y = r3f.axis_angle_to_rpy(ax, ang)
    assert np.allclose(r, R)
    assert np.allclose(p, P)
    assert np.allclose(y, Y)


def test_dcm_axis_angle():
    # Test inputs.
    input_dcm(r3f.dcm_to_axis_angle)
    input_axang(r3f.axis_angle_to_dcm)

    # Define common angle and cosine and sine.
    ang = np.pi/4
    co = np.cos(ang)
    si = np.sin(ang)

    # Test individual axes.
    C = np.array([[co, si, 0], [-si, co, 0], [0, 0, 1]])
    C_p = r3f.axis_angle_to_dcm(np.array([0, 0, 1]), ang)
    assert np.allclose(C, C_p)
    ax1, ang1 = r3f.dcm_to_axis_angle(C_p)
    assert np.allclose(np.array([0, 0, 1]), ax1)
    assert np.allclose(ang, ang1)
    C = np.array([[co, 0, -si], [0, 1, 0], [si, 0, co]])
    C_p = r3f.axis_angle_to_dcm(np.array([0, 1, 0]), ang)
    assert np.allclose(C, C_p)
    ax1, ang1 = r3f.dcm_to_axis_angle(C_p)
    assert np.allclose(np.array([0, 1, 0]), ax1)
    assert np.allclose(ang, ang1)
    C = np.array([[1, 0, 0], [0, co, si], [0, -si, co]])
    C_p = r3f.axis_angle_to_dcm(np.array([1, 0, 0]), ang)
    assert np.allclose(C, C_p)
    ax1, ang1 = r3f.dcm_to_axis_angle(C_p)
    assert np.allclose(np.array([1, 0, 0]), ax1)
    assert np.allclose(ang, ang1)

    # Test vectorized reciprocity (requires positive axes).
    N = 5
    ax = np.abs(np.random.randn(3, N))
    nm = np.linalg.norm(ax, axis=0)
    ax /= nm
    ang = np.random.randn(N)
    C = r3f.axis_angle_to_dcm(ax, ang)
    ax1, ang1 = r3f.dcm_to_axis_angle(C)
    assert np.allclose(ax, ax1)
    assert np.allclose(ang, ang1)


def test_quat_axis_angle():
    # Test inputs.
    input_quat(r3f.quat_to_axis_angle)
    input_axang(r3f.axis_angle_to_quat)

    # axis angle to quat
    a = np.array([1, 1, 1])/np.sqrt(3) # normalized
    q1 = r3f.axis_angle_to_quat(a, np.pi)
    assert np.allclose(q1, np.array([0, 1, 1, 1])/np.sqrt(3))
    b = np.array([2, 2, 2])/np.sqrt(12) # normalized
    q2 = r3f.axis_angle_to_quat(b, np.pi)
    assert np.allclose(q2, np.array([0, 2, 2, 2])/np.sqrt(12))

    # backwards (requires normalized start)
    ax, ang = r3f.quat_to_axis_angle(q1)
    assert np.allclose(a, ax)
    assert np.allclose(np.pi, ang)

    # Test vectorized reciprocity.
    A = np.column_stack((a, b))
    Q = np.column_stack((q1, q2))
    PI = np.array([np.pi, np.pi])
    assert np.allclose(r3f.axis_angle_to_quat(A, PI), Q)


def test_dcm_rpy():
    # Test inputs.
    input_dcm(r3f.dcm_to_rpy)
    input_rpy(r3f.rpy_to_dcm)

    # Build a random DCM.
    R = np.random.uniform(-np.pi, np.pi)
    P = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL)
    Y = np.random.uniform(-np.pi, np.pi)

    # Get rotation matrix.
    C_1g = np.array([
        [np.cos(Y), np.sin(Y), 0],
        [-np.sin(Y), np.cos(Y), 0],
        [0, 0, 1]])
    C_21 = np.array([
        [np.cos(P), 0, -np.sin(P)],
        [0, 1, 0],
        [np.sin(P), 0, np.cos(P)]])
    C_b2 = np.array([
        [1, 0, 0],
        [0, np.cos(R), np.sin(R)],
        [0, -np.sin(R), np.cos(R)]])
    C_bg = C_b2 @ C_21 @ C_1g

    # Check DCM to RPY.
    r, p, y = r3f.dcm_to_rpy(C_bg)
    assert np.allclose(r, R)
    assert np.allclose(p, P)
    assert np.allclose(y, Y)

    # Test vectorized reciprocity.
    N = 5
    R = np.random.uniform(-np.pi, np.pi, N)
    P = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, N)
    Y = np.random.uniform(-np.pi, np.pi, N)
    C = r3f.rpy_to_dcm(R, P, Y)
    r, p, y = r3f.dcm_to_rpy(C)
    assert np.allclose(r, R)
    assert np.allclose(p, P)
    assert np.allclose(y, Y)


def test_quat_rpy():
    # Test inputs.
    input_quat(r3f.quat_to_rpy)
    input_rpy(r3f.rpy_to_quat)

    # This set of tests relies on previous tests.

    # Test forward path.
    N = 5
    R = np.random.uniform(-np.pi, np.pi, N)
    P = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, N)
    Y = np.random.uniform(-np.pi, np.pi, N)
    ax, ang = r3f.rpy_to_axis_angle(R, P, Y)
    q1 = r3f.axis_angle_to_quat(ax, ang)
    q2 = r3f.rpy_to_quat(R, P, Y)
    assert np.allclose(q1, q2)

    # Test backward path.
    r, p, y = r3f.quat_to_rpy(q2)
    assert np.allclose(r, R)
    assert np.allclose(p, P)
    assert np.allclose(y, Y)


def test_quat_dcm():
    # Test inputs.
    input_quat(r3f.quat_to_dcm)
    input_dcm(r3f.dcm_to_quat)

    # This set of tests relies on previous tests.
    N = 5
    R = np.random.uniform(-np.pi, np.pi, N)
    P = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, N)
    Y = np.random.uniform(-np.pi, np.pi, N)
    q1 = r3f.rpy_to_quat(R, P, Y)
    C1 = r3f.rpy_to_dcm(R, P, Y)
    C2 = r3f.quat_to_dcm(q1)
    assert np.allclose(C1, C2)

    # Test reciprocity.
    q2 = r3f.dcm_to_quat(C2)
    assert np.allclose(q1, q2)


def test_rot():
    irt2 = 1/np.sqrt(2)

    C = np.array([
        [irt2, irt2, 0],
        [-irt2, irt2, 0],
        [0, 0, 1]])
    assert np.allclose(r3f.rot(45, 2, True), C)

    B = np.array([
        [irt2, 0, -irt2],
        [0, 1, 0],
        [irt2, 0, irt2]])
    assert np.allclose(r3f.rot(45, 1, True), B)

    A = np.array([
        [1, 0, 0],
        [0, irt2, irt2],
        [0, -irt2, irt2]])
    assert np.allclose(r3f.rot(45, 0, True), A)

    R = r3f.rot([45, 45, 45], [2, 1, 0], True)
    assert np.allclose(R, A @ B @ C)

# ---------------------------
# Reference-frame Conversions
# ---------------------------

def test_ecef_geodetic():
    # Test single point.
    xe, ye, ze = r3f.geodetic_to_ecef(0.0, 0.0, 0.0)
    assert np.allclose([xe, ye, ze], [r3f.A_E, 0, 0])
    lat, lon, hae = r3f.ecef_to_geodetic(xe, ye, ze)
    assert np.allclose([lat, lon, hae], [0.0, 0.0, 0.0])

    # Build original data.
    N = 10
    lat = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, size=N)
    lon = np.random.uniform(-np.pi, np.pi, size=N)
    hae = np.random.uniform(-10e3, 100e3, size=N)

    # Test vectorized reciprocity.
    xe, ye, ze = r3f.geodetic_to_ecef(lat, lon, hae)
    Lat, Lon, Hae = r3f.ecef_to_geodetic(xe, ye, ze)
    assert np.allclose([lat, lon, hae], [Lat, Lon, Hae])


def test_ecef_tangent():
    # Test single point.
    xe = r3f.A_E
    ye = 0.0
    ze = r3f.B_E
    xe0 = r3f.A_E
    ye0 = 0.0
    ze0 = 0.0
    xt, yt, zt = r3f.ecef_to_tangent(xe, ye, ze, xe0, ye0, ze0)
    XT = r3f.B_E
    YT = 0.0
    ZT = 0.0
    assert np.allclose([xt, yt, zt], [XT, YT, ZT])
    XE, YE, ZE = r3f.tangent_to_ecef(XT, YT, ZT, xe0, ye0, ze0)
    assert np.allclose([xe, ye, ze], [XE, YE, ZE])

    # Build original data.
    N = 10
    lat = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, size=N)
    lon = np.random.uniform(-np.pi, np.pi, size=N)
    hae = np.random.uniform(-10e3, 100e3, size=N)
    xe, ye, ze = r3f.geodetic_to_ecef(lat, lon, hae)

    # Test vectorized reciprocity.
    xt, yt, zt = r3f.ecef_to_tangent(xe, ye, ze)
    XE, YE, ZE = r3f.tangent_to_ecef(xt, yt, zt, xe[0], ye[0], ze[0])
    assert np.allclose([xe, ye, ze], [XE, YE, ZE])


def test_geodetic_curlin():
    # Test single point.
    xc, yc, zc = r3f.geodetic_to_curlin(np.pi/4, 0, 1000, 0, 0, 0)
    assert xc > 0
    assert yc == 0
    assert zc == -1000
    lat, lon, hae = r3f.curlin_to_geodetic(xc, yc, zc, 0, 0, 0)
    assert np.allclose([np.pi/4, 0.0, 1e3], [lat, lon, hae])

    # Build original data.
    N = 10
    lat = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, size=N)
    lon = np.random.uniform(-np.pi, np.pi, size=N)
    hae = np.random.uniform(-10e3, 100e3, size=N)
    xc, yc, zc = r3f.geodetic_to_curlin(lat, lon, hae)

    # Test vectorized reciprocity.
    Lat, Lon, Hae = r3f.curlin_to_geodetic(xc, yc, zc, lat[0], lon[0], hae[0])
    assert np.allclose([lat, lon, hae], [Lat, Lon, Hae])
