import numpy as np
from findiff import FinDiff


def get_differential_operator(array, order):
    return FinDiff(order, array)


class DifferentialOperator:
    """
    Class that handles numerical differentiation under certain boundary conditions.
    """

    def __init__(self, space_dict, boundary="periodic", method="pseudo_spectral"):

        n = space_dict["n"]  # get number of spatial points in each dimension
        self.p = 5  # set size of padding for finite difference method

        if "y" in space_dict.keys():
            self.dimensions = 2
            self.x = space_dict["x"]
            self.y = space_dict["y"]

            if method == "finite_difference":
                # for boundary conditions in finite differences
                x_pad = np.linspace(self.x[0] - self.p * (self.x[1] - self.x[0]),
                                    self.x[-1] + self.p * (self.x[1] - self.x[0]),
                                    num=n + 2 * self.p)

                y_pad = np.linspace(self.y[0] - self.p * (self.y[1] - self.y[0]),
                                    self.y[-1] + self.p * (self.y[1] - self.y[0]),
                                    num=n + 2 * self.p)

                # this is to accommodate for one and two dimension in the differentiation method and feels discouraged
                def unpad(u):
                    return u[self.p:-self.p, self.p:-self.p]

                self.d_dx = lambda u, o: self.finite_difference(u, 0, x_pad, order=o, boundary=boundary, unpad=unpad)
                self.d_dy = lambda u, o: self.finite_difference(u, 1, y_pad, order=o, boundary=boundary, unpad=unpad)
                self.dd_dxdy = lambda u, o: self.finite_difference(u, [0, 1], [x_pad, y_pad], order=o,
                                                                   boundary=boundary, unpad=unpad)

            elif method == "pseudo_spectral":

                # for pseudo-spectral method
                kx, ky = np.meshgrid(np.fft.fftfreq(n, space_dict["Lx"] / (n * 2 * np.pi)),
                                     np.fft.fftfreq(n, space_dict["Ly"] / (n * 2 * np.pi)))

                self.d_dx = lambda u, o: self.pseudo_spectral(u, kx, order=o, fft=np.fft.fft2, ifft=np.fft.ifft2)
                self.d_dy = lambda u, o: self.pseudo_spectral(u, ky, order=o, fft=np.fft.fft2, ifft=np.fft.ifft2)
                self.dd_dxdy = lambda u, o: self.d_dx(self.d_dy(u, o[1]), o[0])

            self.div = lambda u, o: self.d_dx(u, o) + self.d_dy(u, o)

        else:
            self.dimensions = 1
            self.x = space_dict["x"]

            if method == "finite_difference":
                # for boundary conditions in finite differences
                x_pad = np.linspace(self.x[0] - self.p * (self.x[1] - self.x[0]),
                                    self.x[-1] + self.p * (self.x[1] - self.x[0]),
                                    num=n + 2 * self.p)

                def unpad(u):
                    return u[self.p:-self.p]

                self.d_dx = lambda u, o: self.finite_difference(u, 0, x_pad, order=o, boundary=boundary, unpad=unpad)
                self.d_dy = None
                self.dd_dxdy = None

            elif method == "pseudo_spectral":
                kx = np.fft.fftfreq(n, space_dict["Lx"] / (n * 2 * np.pi))
                self.d_dx = lambda u, o: self.pseudo_spectral(u, kx, order=o, fft=np.fft.fft, ifft=np.fft.ifft)
                self.d_dy = None
                self.dd_dxdy = None
            self.div = self.d_dx

    def finite_difference(self, u, var, pad, order=1, boundary="periodic", unpad=None):
        if boundary == "periodic":
            bound = "wrap"
        elif boundary == "neumann":
            bound = "edge"
        else:
            raise NotImplementedError("Boundary condition not implemented.")

        u_padded = np.pad(u, [(self.p, self.p) for i in range(len(u.shape))], bound)
        if not(isinstance(var, int)):
            try:
                dn_dxn = FinDiff((var[0], pad[0], order[0]), (var[1], pad[1], order[1]))
            except TypeError:
                raise TypeError("Multivariate derivative requires lists or arrays for all (numeric) inputs")
        else:
            dn_dxn = FinDiff(var, pad, order)

        gradient = dn_dxn(u_padded)
        return unpad(gradient)

    def pseudo_spectral(self, u, k, order=1, fft=np.fft.fft2, ifft=np.fft.ifft2):
        return ifft((1j * k) ** order * fft(u))
