import numpy as np
from .utils.utils import plot_interpolation


def vandermonde(validation_percent, pairs):
    x = np.array([p["x"] for p in pairs], dtype=float)
    y = np.array([p["y"] for p in pairs], dtype=float)

    # SPLIT
    n = len(x)
    val_size = int(np.floor(n * validation_percent))
    split_idx = n - val_size

    x_train, y_train = x[:split_idx], y[:split_idx]
    x_val, y_val = x[split_idx:], y[split_idx:]

    # VANDERMONDE
    V = np.vander(x_train, increasing=False)
    coeffs = np.linalg.solve(V, y_train)

    # POLYNOMIAL STRING
    terms = []
    ncoef = len(coeffs)

    for i, a in enumerate(coeffs):
        power = ncoef - i - 1
        if abs(a) < 1e-15:
            continue

        coef = f"{a:.15f}"

        if power == 0:
            term = f"{coef}"
        elif power == 1:
            term = f"{coef}x"
        else:
            term = f"{coef}x^{power}"

        terms.append(term)

    polynomial = " + ".join(terms).replace("+ -", "- ")

    # DOMAIN
    domain = [float(np.min(x)), float(np.max(x))]

    # VALIDATION ERROR
    if len(x_val) > 0:
        y_pred_val = np.polyval(coeffs, x_val)
        error_inf = float(np.max(np.abs(y_val - y_pred_val)))
    else:
        error_inf = 0.0

    # CURVE
    x_curve = np.linspace(domain[0], domain[1], 500)
    y_curve = np.polyval(coeffs, x_curve)

    # PLOT
    img_base64 = plot_interpolation(
        x_train, y_train,
        x_val, y_val,
        x_curve, y_curve,
        title="Vandermonde Interpolation"
    )

    return {
        "polynomial": f"P(x) = {polynomial}",
        "domain": domain,
        "error_inf": error_inf,
        "image": img_base64
    }