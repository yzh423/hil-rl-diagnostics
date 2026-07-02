from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt


FIG_DIR = Path(__file__).resolve().parent
DPI = 300

matplotlib.rcParams.update({
    "font.size": 10,
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "axes.labelsize": 10,
    "axes.titlesize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8,
    "figure.dpi": DPI,
    "savefig.dpi": DPI,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.04,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "mathtext.fontset": "stix",
})

COLORS = {
    "none": "#4D4D4D",
    "random": "#0072B2",
    "method": "#D55E00",
    "repair": "#009E73",
    "warning": "#CC79A7",
}


def save_fig(fig, stem):
    path = FIG_DIR / f"{stem}.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"saved {path}")
