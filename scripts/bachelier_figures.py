"""
Figures for the post "Bachelier and the Radiation of Probability".

Run:  python scripts/bachelier_figures.py
Writes PNGs to assets/images/bachelier/. Everything is simulated with a fixed
seed, so the figures are reproducible.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

OUT = Path(__file__).resolve().parent.parent / "assets" / "images" / "bachelier"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(1900)  # the year of the thesis

# ---- palette (light surface) -------------------------------------------------
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
SEQ = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]  # sequential blue ramp

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "font.family": "DejaVu Sans",
    "font.size": 11, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.titlesize": 13,
    "axes.titleweight": "bold", "axes.titlecolor": INK, "axes.titlelocation": "left",
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.labelcolor": INK2, "lines.linewidth": 2,
})


def save(fig, name):
    fig.savefig(OUT / name, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT / name)


# ---- 1. random walks fan out inside sigma*sqrt(t) ---------------------------
def fig_random_walks():
    n_paths, n_steps, sigma = 200, 250, 1.0
    t = np.arange(n_steps + 1)
    steps = rng.normal(0, sigma, size=(n_paths, n_steps))
    paths = np.hstack([np.zeros((n_paths, 1)), steps.cumsum(axis=1)])

    fig, ax = plt.subplots(figsize=(9, 5))
    for p in paths:
        ax.plot(t, p, color=MUTED, alpha=0.18, lw=0.8)
    ax.plot(t, paths[7], color=INK, lw=1.4, label="one sample path")
    band = sigma * np.sqrt(t)
    for k, c in [(1, BLUE), (2, ORANGE)]:
        ax.plot(t, k * band, color=c, lw=2)
        ax.plot(t, -k * band, color=c, lw=2)
        ax.text(t[-1] + 3, k * band[-1], f"+{k}σ√t", color=INK2, va="center")
        ax.text(t[-1] + 3, -k * band[-1], f"−{k}σ√t", color=INK2, va="center")

    inside = (np.abs(paths[:, -1]) <= 2 * band[-1]).mean()
    ax.set_title("200 random walks spread out like σ√t")
    ax.set_xlabel("time step t")
    ax.set_ylabel("price change from start")
    ax.set_xlim(0, n_steps + 30)
    ax.text(0.01, 0.02, f"{inside:.0%} of paths end inside ±2σ√t (theory: 95%)",
            transform=ax.transAxes, color=INK2, fontsize=10)
    ax.legend(loc="upper left")
    save(fig, "random-walk-fan.png")


# ---- 2. radiation of probability: Gaussians widen with time -----------------
def fig_radiation():
    x = np.linspace(-12, 12, 600)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for t, c in zip([1, 4, 16, 36], SEQ):
        y = stats.norm.pdf(x, 0, np.sqrt(t))
        ax.plot(x, y, color=c)
        ax.text(0, y.max() + 0.012, f"t = {t}", color=INK2, ha="center", fontsize=10)
    ax.set_ylim(0, 0.45)
    ax.set_title("“Radiation of probability”: N(0, σ²t) at t = 1, 4, 16, 36")
    ax.set_xlabel("price change")
    ax.set_ylabel("probability density")
    save(fig, "radiation-of-probability.png")


# ---- 3. central limit theorem: coin flips become a Gaussian -----------------
def fig_clt():
    n_steps, n_sims = 1000, 50_000
    ends = rng.binomial(n_steps, 0.5, size=n_sims) * 2 - n_steps  # sum of ±1 steps
    fig, ax = plt.subplots(figsize=(9, 4.8))
    bins = np.arange(-130, 132, 4)
    ax.hist(ends, bins=bins, density=True, color=BLUE, edgecolor=SURFACE, lw=1,
            label="simulated endpoints")
    x = np.linspace(-130, 130, 500)
    ax.plot(x, stats.norm.pdf(x, 0, np.sqrt(n_steps)), color=ORANGE,
            label="N(0, 1000)")
    ax.set_title("1,000 coin-flip steps (±1): the endpoint is Gaussian")
    ax.set_xlabel("position after 1,000 steps")
    ax.set_ylabel("density")
    ax.legend(loc="upper right")
    save(fig, "clt-coin-flips.png")


# ---- 4. fat tails: same standard deviation, very different extremes ---------
def fig_fat_tails():
    df = 3
    scale = np.sqrt((df - 2) / df)  # Student-t rescaled to unit variance
    n_steps = 500

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"wspace": 0.28})

    ax = axes[0]
    t = np.arange(n_steps)
    g = rng.normal(0, 1, n_steps)
    f = stats.t.rvs(df, size=n_steps, random_state=rng) * scale
    ax.plot(t, g, color=BLUE, lw=1, label="Gaussian")
    ax.plot(t, f, color=ORANGE, lw=1, alpha=0.9, label="Student-t, 3 d.o.f.")
    ax.axhline(3, color=AXIS, lw=1, ls="--")
    ax.axhline(-3, color=AXIS, lw=1, ls="--")
    ax.text(n_steps, 3.2, "±3σ", color=MUTED, ha="right", fontsize=9)
    ax.set_title("Daily returns, both with σ = 1")
    ax.set_xlabel("day")
    ax.set_ylabel("return (in σ)")
    ax.legend(loc="lower left", fontsize=9)

    ax = axes[1]
    k = np.linspace(1, 8, 200)
    p_norm = 2 * stats.norm.sf(k)
    p_t = 2 * stats.t.sf(k / scale, df)
    ax.semilogy(k, p_norm, color=BLUE, label="Gaussian")
    ax.semilogy(k, p_t, color=ORANGE, label="Student-t, 3 d.o.f.")
    lines = []
    for kk in (4, 6):
        ratio = (2 * stats.t.sf(kk / scale, df)) / (2 * stats.norm.sf(kk))
        lines.append(f"{kk}σ move: ~{float(f'{ratio:.2g}'):,.0f}× likelier")
    ax.text(2.2, 1e-10, "Under fat tails, a\n" + "\n".join(lines),
            color=INK2, fontsize=9, va="center")
    ax.set_ylim(1e-15, 1.5)
    ax.set_title("Probability of a move bigger than kσ")
    ax.set_xlabel("k (size of move in standard deviations)")
    ax.set_ylabel("P(|return| > kσ), log scale")
    ax.legend(loc="lower left", fontsize=9)
    save(fig, "fat-tails.png")


# ---- 5. Bachelier (arithmetic) vs log-normal prices --------------------------
def fig_arith_vs_lognormal():
    s0, vol, T = 100.0, 0.40, 5.0  # 40% annual vol over 5 years, exaggerated on purpose
    sd = s0 * vol * np.sqrt(T)     # Bachelier: absolute vol in price units
    x = np.linspace(-150, 450, 1200)
    arith = stats.norm.pdf(x, s0, sd)
    mu = np.log(s0) - 0.5 * vol**2 * T  # same mean as arithmetic model
    logn = np.where(x > 0, stats.lognorm.pdf(np.clip(x, 1e-9, None), s=vol * np.sqrt(T),
                                             scale=np.exp(mu)), 0)

    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.fill_between(x, arith, where=x < 0, color=BLUE, alpha=0.25, lw=0)
    ax.plot(x, arith, color=BLUE, label="Bachelier: $S_T$ normal")
    ax.plot(x, logn, color=ORANGE, label="Log-normal (geometric Brownian motion)")
    ax.axvline(0, color=INK2, lw=1)
    p_neg = stats.norm.cdf(0, s0, sd)
    ax.text(-140, arith.max() * 0.55, f"{p_neg:.0%} chance of a\nnegative price",
            color=INK2, fontsize=10)
    ax.set_title("Price in 5 years, starting at $100 with 40% volatility")
    ax.set_xlabel("price at T ($)")
    ax.set_ylabel("density")
    ax.legend(loc="upper right")
    save(fig, "arithmetic-vs-lognormal.png")


# ---- 6. timeline --------------------------------------------------------------
def fig_timeline():
    events = [
        (1870, "Born in Le Havre"),
        (1900, "Defends Théorie de la spéculation\n(supervisor: Poincaré)"),
        (1905, "Einstein's Brownian motion paper,\nunaware of Bachelier"),
        (1912, "Calcul des probabilités"),
        (1926, "Blocked at Dijon after\nLévy's critical report"),
        (1931, "Kolmogorov cites him;\nLévy apologises"),
        (1946, "Dies in Saint-Servan-sur-Mer"),
        (1954, "Savage's postcards reach\nSamuelson (mid-1950s)"),
        (1973, "Black–Scholes option\npricing formula"),
        (2000, "Centenary; first Bachelier\nFinance Society congress"),
    ]
    fig, ax = plt.subplots(figsize=(12, 4.2))
    ax.axhline(0, color=AXIS, lw=2)
    heights = [1.0, -1.0, 2.3, -2.6, 1.0, -1.0, 2.3, -2.6, 1.0, -1.0]
    for (yr, label), h in zip(events, heights):
        up = 1 if h > 0 else -1
        ax.plot([yr, yr], [0, h - up * 0.12], color=AXIS, lw=1)
        ax.plot(yr, 0, "o", color=BLUE if yr <= 1946 else ORANGE, ms=8,
                markeredgecolor=SURFACE, markeredgewidth=2, zorder=3)
        ax.text(yr, h, f"{yr}\n{label}" if up > 0 else f"{label}\n{yr}",
                ha="center", va="bottom" if up > 0 else "top", fontsize=8.5, color=INK2)
    ax.set_xlim(1862, 2008)
    ax.set_ylim(-4.0, 3.8)
    ax.axis("off")
    ax.set_title("Bachelier's life (blue) and afterlife (orange)", loc="left")
    save(fig, "timeline.png")


if __name__ == "__main__":
    fig_random_walks()
    fig_radiation()
    fig_clt()
    fig_fat_tails()
    fig_arith_vs_lognormal()
    fig_timeline()
