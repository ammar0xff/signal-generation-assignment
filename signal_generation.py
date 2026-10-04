"""
GENERATION OF DISCRETE-TIME SIGNALS
====================================

Plots the continuous-time (CT) and discrete-time (DT) forms of five basic
signals:

    i.   Step Function        u(t)   /  u[n]
    ii.  Impulse Function     d(t)   /  d[n]
    iii. Exponential Function e^(at) /  a^n
    iv.  Ramp Function        r(t)   /  r[n]
    v.   Sine Function        sin(wt)/  sin(wn)

Run with:  python signal_generation.py

Produces one PNG per signal (CT and DT side by side) plus a combined
overview figure, all in ./figures/.
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # non-interactive backend (headless / Termux)
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUTDIR, exist_ok=True)

# Continuous-time axis: fine sampling so CT curves look smooth.
T_CT = np.linspace(-5, 5, 2001)

# Discrete-time axis: integer samples only, n = -10 .. 10.
N_DT = np.arange(-10, 11)

# Parameters
A_EXP = 0.5   # exponential growth rate (0 < A < 1 gives decay)
W_SIN = np.pi / 4  # sine angular frequency (rad/sample)


# ----------------------------------------------------------------------------
# Signal definitions
# ----------------------------------------------------------------------------
def step_ct(t):
    """Unit step: u(t) = 1 for t >= 0, else 0."""
    return np.where(t >= 0, 1.0, 0.0)


def step_dt(n):
    """Unit step: u[n] = 1 for n >= 0, else 0."""
    return np.where(n >= 0, 1.0, 0.0)


def impulse_ct(t):
    """Unit impulse: d(t) = 1 at t = 0, else 0.

    Represented as an arrow of unit height at the origin because a Dirac
    delta has infinite height and zero width -- it cannot be drawn as an
    ordinary point.
    """
    return np.where(t == 0, 1.0, 0.0)


def impulse_dt(n):
    """Unit impulse (Kronecker delta): d[n] = 1 at n = 0, else 0."""
    return np.where(n == 0, 1.0, 0.0)


def exponential_ct(t, a=A_EXP):
    """Exponential: e^(a t)."""
    return np.exp(a * t)


def exponential_dt(n, a=A_EXP):
    """Exponential: a^n."""
    return np.power(a, n)


def ramp_ct(t):
    """Ramp: r(t) = t for t >= 0, else 0."""
    return np.where(t >= 0, t, 0.0)


def ramp_dt(n):
    """Ramp: r[n] = n for n >= 0, else 0."""
    return np.where(n >= 0, n.astype(float), 0.0)


def sine_ct(t, w=W_SIN):
    """Sine: sin(w t)."""
    return np.sin(w * t)


def sine_dt(n, w=W_SIN):
    """Sine: sin(w n)."""
    return np.sin(w * n)


# ----------------------------------------------------------------------------
# Plotting helpers
# ----------------------------------------------------------------------------
def style_axes(ax, xlabel, ylabel, title):
    """Apply consistent styling to a subplot."""
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    # Mark the origin so the step/impulse transitions are unambiguous.
    ax.plot(0, 0, "ko", markersize=4, markerfacecolor="white", zorder=5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=11)
    ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.6)


def save(fig, name):
    path = os.path.join(OUTDIR, name)
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", path)


# ----------------------------------------------------------------------------
# i. Step function
# ----------------------------------------------------------------------------
def plot_step():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

    style_axes(ax1, "t", "u(t)", "(i-a) Continuous-Time Step  u(t)")
    ax1.plot(T_CT, step_ct(T_CT), linewidth=2, color="tab:blue")
    ax1.set_ylim(-0.3, 1.4)

    style_axes(ax2, "n", "u[n]", "(i-b) Discrete-Time Step  u[n]")
    ax2.stem(N_DT, step_dt(N_DT), linefmt="C0-", markerfmt="C0o", basefmt=" ")
    ax2.set_ylim(-0.3, 1.4)

    fig.suptitle("Step Function", fontsize=13)
    fig.tight_layout()
    save(fig, "1_step_function.png")


# ----------------------------------------------------------------------------
# ii. Impulse function
# ----------------------------------------------------------------------------
def plot_impulse():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

    style_axes(ax1, "t", "d(t)", "(ii-a) Continuous-Time Impulse  d(t)")
    ax1.plot(T_CT, impulse_ct(T_CT), linewidth=2, color="tab:blue")
    # Draw the delta as an arrow: infinite height, zero width.
    ax1.annotate(
        "",
        xy=(0, 1.0),
        xytext=(0, 0),
        arrowprops=dict(arrowstyle="-|>", color="tab:blue", linewidth=2.2),
    )
    ax1.set_ylim(-0.3, 1.4)

    style_axes(ax2, "n", "d[n]", "(ii-b) Discrete-Time Impulse  d[n]")
    ax2.stem(N_DT, impulse_dt(N_DT), linefmt="C0-", markerfmt="C0o", basefmt=" ")
    ax2.set_ylim(-0.3, 1.4)

    fig.suptitle("Impulse Function", fontsize=13)
    fig.tight_layout()
    save(fig, "2_impulse_function.png")


# ----------------------------------------------------------------------------
# iii. Exponential function
# ----------------------------------------------------------------------------
def plot_exponential():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

    style_axes(ax1, "t", "e^(a t)", f"(iii-a) Continuous-Time Exponential  e^({A_EXP}t)")
    ax1.plot(T_CT, exponential_ct(T_CT), linewidth=2, color="tab:blue")
    ax1.set_ylim(0, max(exponential_ct(T_CT)) * 1.15)

    style_axes(ax2, "n", "a^n", f"(iii-b) Discrete-Time Exponential  {A_EXP}^n")
    ax2.stem(
        N_DT,
        exponential_dt(N_DT),
        linefmt="C0-",
        markerfmt="C0o",
        basefmt=" ",
    )
    ax2.set_ylim(0, max(exponential_dt(N_DT)) * 1.15)

    fig.suptitle("Exponential Function", fontsize=13)
    fig.tight_layout()
    save(fig, "3_exponential_function.png")


# ----------------------------------------------------------------------------
# iv. Ramp function
# ----------------------------------------------------------------------------
def plot_ramp():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

    style_axes(ax1, "t", "r(t)", "(iv-a) Continuous-Time Ramp  r(t)")
    ax1.plot(T_CT, ramp_ct(T_CT), linewidth=2, color="tab:blue")
    ax1.set_ylim(-0.5, 5.5)

    style_axes(ax2, "n", "r[n]", "(iv-b) Discrete-Time Ramp  r[n]")
    ax2.stem(N_DT, ramp_dt(N_DT), linefmt="C0-", markerfmt="C0o", basefmt=" ")
    ax2.set_ylim(-0.5, 11)

    fig.suptitle("Ramp Function", fontsize=13)
    fig.tight_layout()
    save(fig, "4_ramp_function.png")


# ----------------------------------------------------------------------------
# v. Sine function
# ----------------------------------------------------------------------------
def plot_sine():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

    style_axes(ax1, "t", "sin(wt)", f"(v-a) Continuous-Time Sine  sin({W_SIN:.4f}t)")
    ax1.plot(T_CT, sine_ct(T_CT), linewidth=2, color="tab:blue")
    ax1.set_ylim(-1.4, 1.4)

    style_axes(ax2, "n", "sin(wn)", f"(v-b) Discrete-Time Sine  sin({W_SIN:.4f}n)")
    ax2.stem(N_DT, sine_dt(N_DT), linefmt="C0-", markerfmt="C0o", basefmt=" ")
    ax2.set_ylim(-1.4, 1.4)

    fig.suptitle("Sine Function", fontsize=13)
    fig.tight_layout()
    save(fig, "5_sine_function.png")


# ----------------------------------------------------------------------------
# Combined overview: all five signals, CT and DT
# ----------------------------------------------------------------------------
def plot_overview():
    fig, axes = plt.subplots(5, 2, figsize=(12, 18))

    rows = [
        ("Step", step_ct, step_dt, "u(t)", "u[n]"),
        ("Impulse", impulse_ct, impulse_dt, "d(t)", "d[n]"),
        ("Exponential", exponential_ct, exponential_dt, "e^(at)", "a^n"),
        ("Ramp", ramp_ct, ramp_dt, "r(t)", "r[n]"),
        ("Sine", sine_ct, sine_dt, "sin(wt)", "sin(wn)"),
    ]

    for row, (name, f_ct, f_dt, lbl_ct, lbl_dt) in zip(axes, rows):
        style_axes(row[0], "t", lbl_ct, f"{name} (continuous-time)")
        y = f_ct(T_CT)
        row[0].plot(T_CT, y, linewidth=2, color="tab:blue")
        if name == "Impulse":
            row[0].annotate(
                "",
                xy=(0, 1.0),
                xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="tab:blue", linewidth=2.2),
            )

        style_axes(row[1], "n", lbl_dt, f"{name} (discrete-time)")
        row[1].stem(N_DT, f_dt(N_DT), linefmt="C0-", markerfmt="C0o", basefmt=" ")

        for ax in row:
            ax.set_ylim(min(-0.4, np.min(f_ct(T_CT))), np.max(f_ct(T_CT)) * 1.2 + 0.3)

    fig.suptitle(
        "Generation of Discrete-Time Signals -- Continuous vs. Discrete", fontsize=15
    )
    fig.tight_layout(rect=[0, 0, 1, 0.98])
    save(fig, "0_all_signals_overview.png")


# ----------------------------------------------------------------------------
def main():
    print("Generating signal plots ->", OUTDIR)
    plot_overview()
    plot_step()
    plot_impulse()
    plot_exponential()
    plot_ramp()
    plot_sine()
    print("Done.")


if __name__ == "__main__":
    main()