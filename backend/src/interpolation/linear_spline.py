import numpy as np
from .utils.utils import plot_interpolation


# -------------------------
# LINEAR SPLINE EVALUATION
# -------------------------
def linear_spline_eval(x_nodes, y_nodes, x):
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)
    x = np.array(x, dtype=float)

    # Ensure sorting
    idx = np.argsort(x_nodes)
    x_nodes = x_nodes[idx]
    y_nodes = y_nodes[idx]

    result = np.zeros_like(x, dtype=float)

    for k in range(len(x)):
        # Clamp out-of-bounds
        if x[k] <= x_nodes[0]:
            result[k] = y_nodes[0]
            continue
        if x[k] >= x_nodes[-1]:
            result[k] = y_nodes[-1]
            continue

        # Find segment
        i = np.searchsorted(x_nodes, x[k]) - 1

        x0, x1 = x_nodes[i], x_nodes[i + 1]
        y0, y1 = y_nodes[i], y_nodes[i + 1]

        # Linear interpolation
        t = (x[k] - x0) / (x1 - x0)
        result[k] = (1 - t) * y0 + t * y1

    return result


# -------------------------
# LINEAR SPLINE STRING (15 DECIMALS ONLY)
# -------------------------
def linear_spline_string(x_nodes, y_nodes):
    x_nodes = np.array(x_nodes, dtype=float)
    y_nodes = np.array(y_nodes, dtype=float)

    idx = np.argsort(x_nodes)
    x_nodes = x_nodes[idx]
    y_nodes = y_nodes[idx]

    segments = []
    n = len(x_nodes)

    for i in range(n - 1):
        x0, x1 = x_nodes[i], x_nodes[i + 1]
        y0, y1 = y_nodes[i], y_nodes[i + 1]

        if x1 == x0:
            continue

        m = (y1 - y0) / (x1 - x0)
        b = y0 - m * x0

        segments.append(
            f"({m:.15f})x + ({b:.15f})  for x in [{x0:.15f}, {x1:.15f}]"
        )

    if not segments:
        return "0"

    return " ; ".join(segments)


# -------------------------
# LINEAR SPLINE MAIN
# -------------------------
def linear_spline(validation_percent, pairs):
    x = np.array([p["x"] for p in pairs], dtype=float)
    y = np.array([p["y"] for p in pairs], dtype=float)

    # SPLIT
    n = len(x)
    val_size = int(np.floor(n * validation_percent))
    split_idx = n - val_size

    x_train, y_train = x[:split_idx], y[:split_idx]
    x_val, y_val = x[split_idx:], y[split_idx:]

    # DOMAIN (15 decimals forced via formatting later if needed)
    domain = [
        float(f"{np.min(x):.15f}"),
        float(f"{np.max(x):.15f}")
    ]

    # VALIDATION ERROR (kept numeric but can be formatted if needed)
    if len(x_val) > 0:
        y_pred_val = linear_spline_eval(x_train, y_train, x_val)
        error_inf = float(np.max(np.abs(y_val - y_pred_val)))
    else:
        error_inf = 0.0

    # CURVE
    x_curve = np.linspace(domain[0], domain[1], 500)
    y_curve = linear_spline_eval(x_train, y_train, x_curve)

    # SPLINE STRING (15 DECIMALS)
    spline_str = linear_spline_string(x_train, y_train)

    # PLOT
    img_base64 = plot_interpolation(
        x_train, y_train,
        x_val, y_val,
        x_curve, y_curve,
        title="Natural Linear Spline Interpolation"
    )

    return {
        "spline": spline_str,
        "domain": domain,
        "error_inf": error_inf,
        "image": img_base64
    }