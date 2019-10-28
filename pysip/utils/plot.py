import numpy as np
import matplotlib.pyplot as plt


def percentile_plot(
    x,
    y,
    n=10,
    percentile_min=2.5,
    percentile_max=97.5,
    color='r',
    plot_mean=True,
    plot_median=False,
    line_color='k',
    **kwargs,
):
    """Percentile plot for time series"""

    # calculate the lower and upper percentile groups, skipping 50 percentile
    linspace1 = np.linspace(percentile_min, 50, num=n, endpoint=False)
    linspace2 = np.linspace(50, percentile_max, num=n + 1)[1:]
    perc1 = np.percentile(y, linspace1, axis=0)
    perc2 = np.percentile(y, linspace2, axis=0)

    # transparency
    if 'alpha' in kwargs:
        alpha = kwargs.pop('alpha')
    else:
        alpha = 1 / n

    # fill lower and upper percentile groups
    for p1, p2 in zip(perc1, perc2):
        plt.fill_between(x, p1, p2, alpha=alpha, color=color, edgecolor=None)

    if plot_mean:
        plt.plot(x, np.mean(y, axis=0), color=line_color)

    if plot_median:
        plt.plot(x, np.median(y, axis=0), color=line_color)

    return plt.gca()


def plot_ccf(lags, coeffs, confidence, ax=None):
    """Plot cross-correlation coefficients

    Args:
        lags, coeffs, confidences: outputs of the ccf function
        ax: Matplotlib axe

    Returns:
        Matplotlib axe
    """
    if ax is None:
        _, ax = plt.subplots()

    _, stemlines, baseline = ax.stem(lags, coeffs, '-', markerfmt='None', use_line_collection=True)
    ax.fill_between(lags, -confidence, confidence, facecolor='r', edgecolor='None', alpha=0.2)

    ax.set_xlabel('Lags', fontsize=12)
    ax.set_ylabel('Normalized Correlation Coefficients', fontsize=12)
    plt.setp(baseline, color='b', linewidth=1)
    plt.setp(stemlines, color='b', linewidth=1.5)

    return ax


def plot_cpgram(y, freq, crit, ax=None):
    """Plot cumulative periodogram with confidence intervals

    Args:
        lags, coeffs, confidences: outputs of the ccf function
        ax: Matplotlib axe

    Returns:
        Matplotlib axe
    """
    if ax is None:
        _, ax = plt.subplots()

    ax.plot(freq, np.cumsum(y) / np.sum(y))
    ax.fill_between(
        freq, 2 * freq - crit, 2 * freq + crit, facecolor='r', edgecolor='None', alpha=0.2
    )
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0, 1)
    ax.set_xlabel('Normalized Nyquist Frequency')
    ax.set_ylabel('Cumulated Periodogram')

    return ax
