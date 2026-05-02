import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import io
import base64


def plot_interpolation(
    x_train, y_train,
    x_val, y_val,
    x_curve, y_curve,
    title="Interpolation"
):
    plt.figure()

    # TRAINING
    plt.scatter(x_train, y_train, color="green", label="Training", s=60)

    for xi, yi in zip(x_train, y_train):
        plt.annotate(
            f"({xi:.2f}, {yi:.2f})",
            (xi, yi),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=8,
            color="green"
        )

    # VALIDATION
    if len(x_val) > 0:
        plt.scatter(x_val, y_val, color="orange", label="Validation", s=60)

        for xi, yi in zip(x_val, y_val):
            plt.annotate(
                f"({xi:.2f}, {yi:.2f})",
                (xi, yi),
                textcoords="offset points",
                xytext=(5, 5),
                fontsize=8,
                color="orange"
            )

    # CURVE
    plt.plot(x_curve, y_curve, color="blue", label="Interpolation")

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(title)
    plt.legend()
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    return img_base64