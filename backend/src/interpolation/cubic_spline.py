import numpy as np
from .utils.utils import plot_interpolation


# -------------------------
# BUILD CUBIC SPLINE (NATURAL)
# -------------------------
def _build_cubic_spline(x_nodes, y_nodes):
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)

    n = len(x_nodes)
    h = np.diff(x_nodes)

    A = np.zeros((n, n))
    rhs = np.zeros(n)

    # Natural boundary conditions
    A[0, 0] = 1
    A[-1, -1] = 1
    rhs[0] = 0
    rhs[-1] = 0

    # Interior equations
    for i in range(1, n - 1):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]

        rhs[i] = 6 * (
            (y_nodes[i + 1] - y_nodes[i]) / h[i]
            - (y_nodes[i] - y_nodes[i - 1]) / h[i - 1]
        )

    M = np.linalg.solve(A, rhs)

    a = np.zeros(n - 1)
    b = np.zeros(n - 1)
    c = np.zeros(n - 1)
    d = np.zeros(n - 1)

    for i in range(n - 1):
        hi = h[i]

        a[i] = (M[i + 1] - M[i]) / (6 * hi)
        b[i] = M[i] / 2
        c[i] = (y_nodes[i + 1] - y_nodes[i]) / hi - (2 * hi * M[i] + hi * M[i + 1]) / 6
        d[i] = y_nodes[i]

    return a, b, c, d


# -------------------------
# EVALUATION (UNCHANGED)
# -------------------------
def cubic_spline_eval(x_nodes, y_nodes, x):
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)
    x = np.array(x, dtype=float)

    idx = np.argsort(x_nodes)
    x_nodes = x_nodes[idx]
    y_nodes = y_nodes[idx]

    a, b, c, d = _build_cubic_spline(x_nodes, y_nodes)

    result = np.zeros_like(x, dtype=float)

    for k in range(len(x)):
        if x[k] <= x_nodes[0]:
            result[k] = y_nodes[0]
            continue
        if x[k] >= x_nodes[-1]:
            result[k] = y_nodes[-1]
            continue

        i = np.searchsorted(x_nodes, x[k]) - 1
        dx = x[k] - x_nodes[i]

        result[k] = a[i] * dx**3 + b[i] * dx**2 + c[i] * dx + d[i]

    return result


# -------------------------
# 🔥 KEY FIX: EXPAND LOCAL → GLOBAL POLYNOMIAL
# -------------------------
def _expand_cubic(a, b, c, d, x0):
    A = a
    B = -3 * a * x0 + b
    C = 3 * a * x0**2 - 2 * b * x0 + c
    D = -a * x0**3 + b * x0**2 - c * x0 + d
    return A, B, C, D


# -------------------------
# STRING REPRESENTATION (FIXED)
# -------------------------
def cubic_spline_string(x_nodes, y_nodes):
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)

    idx = np.argsort(x_nodes)
    x_nodes = x_nodes[idx]
    y_nodes = y_nodes[idx]

    a, b, c, d = _build_cubic_spline(x_nodes, y_nodes)

    segments = []

    for i in range(len(x_nodes) - 1):
        A, B, C, D = _expand_cubic(a[i], b[i], c[i], d[i], x_nodes[i])

        segments.append(
            f"({A:.15f})x^3 + ({B:.15f})x^2 + ({C:.15f})x + ({D:.15f}) "
            f"for x in [{x_nodes[i]:.15f}, {x_nodes[i+1]:.15f}]"
        )

    return " ; ".join(segments) if segments else "0"


# -------------------------
# MAIN FUNCTION
# -------------------------
def cubic_spline(validation_percent, pairs):
    x = np.array([p["x"] for p in pairs], dtype=float)
    y = np.array([p["y"] for p in pairs], dtype=float)

    n = len(x)
    val_size = int(np.floor(n * validation_percent))
    split_idx = n - val_size

    x_train, y_train = x[:split_idx], y[:split_idx]
    x_val, y_val = x[split_idx:], y[split_idx:]

    domain = [
        float(f"{np.min(x):.15f}"),
        float(f"{np.max(x):.15f}")
    ]

    if len(x_val) > 0:
        y_pred_val = cubic_spline_eval(x_train, y_train, x_val)
        error_inf = float(np.max(np.abs(y_val - y_pred_val)))
    else:
        error_inf = 0.0

    x_curve = np.linspace(domain[0], domain[1], 500)
    y_curve = cubic_spline_eval(x_train, y_train, x_curve)

    spline_str = cubic_spline_string(x_train, y_train)

    img_base64 = plot_interpolation(
        x_train, y_train,
        x_val, y_val,
        x_curve, y_curve,
        title="Natural Cubic Spline Interpolation"
    )

    return {
        "spline": spline_str,
        "domain": domain,
        "error_inf": error_inf,
        "image": img_base64
    }