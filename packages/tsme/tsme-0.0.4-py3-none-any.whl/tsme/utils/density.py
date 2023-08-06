import numpy as np
from sklearn.neighbors import KernelDensity
import freud


def density_from_2d_positions_freud(box, position_series, width=128, r_max=7.5, sigma=5.0):
    """
    Function that wraps the freud-analysis Guassian density estimator for a time series of 2d positional data

    Parameters
    ----------
    box : tuple
        Tuple (Lx, Ly) containing the length of x and y direction of the 2d slice (positions should fall in between
        these values)
    position_series : numpy.array-like
        Time series of positional values of individual particles. Shape should be (# time steps, # particles, 3), where
        one postion is comprised of x, y and z coordinates. This case assumes z=0 for all coordinates.
    width : integer, default=128
        Number of bins per side in 2d slice
    r_max : float, default=7.5
        Distance over which particles are blurred
    sigma : float, default=5.0
        Sigma parameter for Gaussian

    Returns
    -------
    numpy.array
        Time series of 2d slices of density approximation (shape: (# time steps, width, width))
    """
    box = freud.box.Box(Lx=box[0], Ly=box[1], Lz=0)

    ds = freud.density.GaussianDensity(width=width, r_max=r_max, sigma=sigma)

    snaps = []
    for i, positions in enumerate(position_series):
        density_a = ds.compute((box, positions))

        snaps.append(density_a.density)
        print(f"Time step: {i} of {len(position_series)}")

    snaps = np.array(snaps)

    return snaps


def density_from_2d_positions_sklearn(box, position_series, bandwidth=2.0, bins=None, kernel="epanechnikov"):
    """
    Method that uses sklearns kernel density estimator to approximate the density of  time series of 2d positinal data

    Parameters
    ----------
    box : tuple
        Tuple (Lx, Ly) containing the length of x and y direction of the 2d slice (positions should fall in between
        these values)
    position_series : numpy.array-like
        Time series of positional values of individual particles. Shape should be (# time steps, # particles, 3), where
        one postion is comprised of x, y and z coordinates. This case assumes z=0 for all coordinates.
    bandwidth : float, default=2.0
        Smoothing parameter that controls the bias-variance trade-off in kernel density estimation
    bins : tuple, default=None
        Tuple (Nx, Ny) with the number of bins in x and y direction. If `None` is set to 128 in each direction.
    kernel : string, default="epanechnikov"
        Sets which sklearn Kernel should be used. Options are: 'gaussian', 'tophat', 'epanechnikov', 'exponential',
        'linear', 'cosine'.


    Returns
    -------
    numpy.array
        Time series of 2d slices of density approximation (shape: (# time steps, box[0], box[1]))
    """
    if bins is None:
        x_bins = 128j
        y_bins = 128j
    else:
        x_bins = bins[0]*1j
        y_bins = bins[1]*1j

    box = np.array([[- box[0] / 2, box[0] / 2],
                    [-box[1] / 2, box[1] / 2]])

    def kde2D(x, y, bw, xbins=x_bins, ybins=y_bins, **kwargs):
        """Build 2D kernel density estimate (KDE)."""

        # create grid of sample locations
        xx, yy = np.mgrid[box[0][0]:box[0][1]:xbins, box[1][0]:box[1][1]:ybins]

        xy_sample = np.vstack([yy.ravel(), xx.ravel()]).T
        xy_train = np.vstack([y, x]).T

        kde_skl = KernelDensity(bandwidth=bw, **kwargs)
        kde_skl.fit(xy_train)

        # score_samples() returns the log-likelihood of the samples
        z = np.exp(kde_skl.score_samples(xy_sample))
        return xx, yy, np.reshape(z, xx.shape)

    snaps = []
    for i, positions in enumerate(position_series):

        _, _, zz = kde2D(positions[:, 0], positions[:, 1], bandwidth, kernel=kernel)
        snaps.append(zz)
        print(f"Time step: {i} of {len(position_series)}")

    snaps = np.array(snaps)

    return snaps
