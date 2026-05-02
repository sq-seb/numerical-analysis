import numpy as np
from .utils.utils import plot_interpolation


# -------------------------
# BUILD QUADRATIC SPLINE
# -------------------------
def _build_quadratic_spline(x_nodes, y_nodes):
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)

    n = len(x_nodes)

    a = np.zeros(n - 1)
    b = np.zeros(n - 1)
    c = np.zeros(n - 1)

    # Natural-like condition (your version)
    a[0] = 0.0

    h0 = x_nodes[1] - x_nodes[0]
    b[0] = (y_nodes[1] - y_nodes[0]) / h0
    c[0] = y_nodes[0]

    for j in range(1, n - 1):
        h_prev = x_nodes[j] - x_nodes[j - 1]
        h_next = x_nodes[j + 1] - x_nodes[j]

        # derivative continuity
        b[j] = 2 * a[j - 1] * h_prev + b[j - 1]

        # interpolation at node
        c[j] = y_nodes[j]

        # solve for a_j
        a[j] = (y_nodes[j + 1] - y_nodes[j] - b[j] * h_next) / (h_next ** 2)

    return a, b, c


# -------------------------
# EVALUATION (LOCAL FORM)
# -------------------------
def quadratic_spline_eval(x_nodes, y_nodes, x):
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)
    x = np.array(x, dtype=float)

    idx = np.argsort(x_nodes)
    x_nodes = x_nodes[idx]
    y_nodes = y_nodes[idx]

    a, b, c = _build_quadratic_spline(x_nodes, y_nodes)

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
        result[k] = a[i] * dx**2 + b[i] * dx + c[i]

    return result


# -------------------------
# STRING REPRESENTATION (FIXED: GLOBAL FORM)
# -------------------------
def quadratic_spline_string(x_nodes, y_nodes):
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)

    idx = np.argsort(x_nodes)
    x_nodes = x_nodes[idx]
    y_nodes = y_nodes[idx]

    a, b, c = _build_quadratic_spline(x_nodes, y_nodes)

    segments = []

    for i in range(len(x_nodes) - 1):
        xi = x_nodes[i]

        # convert from (x - xi) form to global Ax^2 + Bx + C
        A = a[i]
        B = -2 * a[i] * xi + b[i]
        C = a[i] * xi**2 - b[i] * xi + c[i]

        segments.append(
            f"({A:.15f})x^2 + ({B:.15f})x + ({C:.15f}) "
            f"for x in [{x_nodes[i]:.15f}, {x_nodes[i+1]:.15f}]"
        )

    return " ; ".join(segments) if segments else "0"


# -------------------------
# MAIN FUNCTION
# -------------------------
def quadratic_spline(validation_percent, pairs):
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
        y_pred_val = quadratic_spline_eval(x_train, y_train, x_val)
        error_inf = float(np.max(np.abs(y_val - y_pred_val)))
    else:
        error_inf = 0.0

    x_curve = np.linspace(domain[0], domain[1], 500)
    y_curve = quadratic_spline_eval(x_train, y_train, x_curve)

    spline_str = quadratic_spline_string(x_train, y_train)

    img_base64 = plot_interpolation(
        x_train, y_train,
        x_val, y_val,
        x_curve, y_curve,
        title="Natural Quadratic Spline Interpolation"
    )

    return {
        "spline": spline_str,
        "domain": domain,
        "error_inf": error_inf,
        "image": img_base64
    }