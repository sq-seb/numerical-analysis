import numpy as np
from .utils.utils import plot_interpolation


# -------------------------
# DIVIDED DIFFERENCES
# -------------------------
def divided_differences(x, y):
    n = len(x)
    coef = np.copy(y).astype(float)

    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (x[i] - x[i - j])

    return coef


# -------------------------
# NEWTON EVALUATION
# -------------------------
def newton_eval(x_nodes, coef, x):
    x = np.array(x, dtype=float)
    result = np.zeros_like(x, dtype=float)

    for i in range(len(x)):
        value = coef[-1]
        for j in range(len(coef) - 2, -1, -1):
            value = value * (x[i] - x_nodes[j]) + coef[j]
        result[i] = value

    return result


# -------------------------
# FORMAT (FIX x - -a → x + a)
# -------------------------
def format_node(x):
    # clean float formatting
    if abs(x) < 1e-12:
        x = 0.0

    if x < 0:
        return f"(x + {abs(x):.6f})"
    else:
        return f"(x - {x:.6f})"


# -------------------------
# NEWTON MAIN
# -------------------------
def newton(validation_percent, pairs):
    x = np.array([p["x"] for p in pairs], dtype=float)
    y = np.array([p["y"] for p in pairs], dtype=float)

    # SPLIT
    n = len(x)
    val_size = int(np.floor(n * validation_percent))
    split_idx = n - val_size

    x_train, y_train = x[:split_idx], y[:split_idx]
    x_val, y_val = x[split_idx:], y[split_idx:]

    # SORT
    idx = np.argsort(x_train)
    x_train, y_train = x_train[idx], y_train[idx]

    # COEFFICIENTS
    coef = divided_differences(x_train, y_train)

    # DOMAIN
    domain = [float(np.min(x)), float(np.max(x))]

    # VALIDATION ERROR
    if len(x_val) > 0:
        y_pred_val = newton_eval(x_train, coef, x_val)
        error_inf = float(np.max(np.abs(y_val - y_pred_val)))
    else:
        error_inf = 0.0

    # CURVE
    x_curve = np.linspace(domain[0], domain[1], 500)
    y_curve = newton_eval(x_train, coef, x_curve)

    # -------------------------
    # POLYNOMIAL STRING (FIXED)
    # -------------------------
    terms = []

    for i in range(len(coef)):
        c = float(coef[i])

        if abs(c) < 1e-15:
            continue

        sign = "-" if c < 0 else "+"
        c_abs = abs(c)

        term = f"{c_abs:.15f}"

        for j in range(i):
            term += format_node(x_train[j])

        terms.append((sign, term))

    if not terms:
        polynomial = "0"
    else:
        first_sign, first_term = terms[0]
        polynomial = first_term if first_sign == "+" else f"-{first_term}"

        for sign, term in terms[1:]:
            polynomial += f" {sign} {term}"

    # -------------------------
    # PLOT
    # -------------------------
    img_base64 = plot_interpolation(
        x_train, y_train,
        x_val, y_val,
        x_curve, y_curve,
        title="Newton Interpolation"
    )

    return {
        "polynomial": f"P(x) = {polynomial}",
        "domain": domain,
        "error_inf": error_inf,
        "image": img_base64
    }