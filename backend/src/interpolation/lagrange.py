import numpy as np
from .utils.utils import plot_interpolation


# -------------------------
# LAGRANGE EVALUATION
# -------------------------
def lagrange_eval(x_nodes, y_nodes, x):
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)
    x = np.array(x, dtype=float)

    n = len(x_nodes)
    result = np.zeros_like(x, dtype=float)

    for k in range(len(x)):
        total = 0.0

        for i in range(n):
            term = y_nodes[i]

            for j in range(n):
                if i != j:
                    term *= (x[k] - x_nodes[j]) / (x_nodes[i] - x_nodes[j])

            total += term

        result[k] = total

    return result


# -------------------------
# LAGRANGE POLYNOMIAL STRING
# -------------------------
def lagrange_poly_string(x_nodes, y_nodes):
    terms = []

    n = len(x_nodes)

    for i in range(n):
        xi, yi = float(x_nodes[i]), float(y_nodes[i])

        if abs(yi) < 1e-15:
            continue

        sign = "-" if yi < 0 else "+"
        yi_abs = abs(yi)

        term = f"{yi_abs:.15f}"

        for j in range(n):
            if i == j:
                continue
            xj = float(x_nodes[j])

            if xj < 0:
                term += f"(x + {abs(xj):.6f})"
            else:
                term += f"(x - {xj:.6f})"

            denom = (xi - xj)
            term += f"/({denom:.6f})"

        terms.append((sign, term))

    if not terms:
        return "0"

    first_sign, first_term = terms[0]
    polynomial = first_term if first_sign == "+" else f"-{first_term}"

    for sign, term in terms[1:]:
        polynomial += f" {sign} {term}"

    return polynomial


# -------------------------
# LAGRANGE MAIN
# -------------------------
def lagrange(validation_percent, pairs):
    x = np.array([p["x"] for p in pairs], dtype=float)
    y = np.array([p["y"] for p in pairs], dtype=float)

    # SPLIT
    n = len(x)
    val_size = int(np.floor(n * validation_percent))
    split_idx = n - val_size

    x_train, y_train = x[:split_idx], y[:split_idx]
    x_val, y_val = x[split_idx:], y[split_idx:]

    # DOMAIN
    domain = [float(np.min(x)), float(np.max(x))]

    # VALIDATION ERROR
    if len(x_val) > 0:
        y_pred_val = lagrange_eval(x_train, y_train, x_val)
        error_inf = float(np.max(np.abs(y_val - y_pred_val)))
    else:
        error_inf = 0.0

    # CURVE
    x_curve = np.linspace(domain[0], domain[1], 500)
    y_curve = lagrange_eval(x_train, y_train, x_curve)

    # POLYNOMIAL STRING
    polynomial = lagrange_poly_string(x_train, y_train)

    # PLOT
    img_base64 = plot_interpolation(
        x_train, y_train,
        x_val, y_val,
        x_curve, y_curve,
        title="Lagrange Interpolation"
    )

    return {
        "polynomial": f"P(x) = {polynomial}",
        "domain": domain,
        "error_inf": error_inf,
        "image": img_base64
    }