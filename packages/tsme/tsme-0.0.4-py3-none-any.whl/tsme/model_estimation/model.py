import numpy as np
from numpy import math
from tsme.time_simulation import AbstractTimeSimulator
from .optimization import train_ridge_wip
from itertools import combinations_with_replacement as combinations_wr
from tabulate import tabulate


def _make_combination_string(order, n_variables):
    """
    This helper method gives a string containing all combinations of multiplying n_variables with one another and
    also the single elements.
    Example output for order=2 and n_variables=3:
    `np.array([np.ones(u[0].shape), u[0], u[1], u[2], u[0]*u[0], u[0]*x[1], u[0]*u[2], u[1]*u[1], u[1]*u[2], u[2]*u[2]])`

    Parameters
    ----------
    order : int
        Order up to which permutations should be included
    n_variables :
        Number of variables to combine

    Returns
    -------
    x_string : string
        String containing a 'one' element, the elements of an array u and products of all combinations of elements of u.

    """
    xstr = [f"u[{i}]" for i in range(n_variables)]
    x_string = "np.array([np.ones(u[0].shape)"
    for o in range(order + 1):
        comb = combinations_wr(xstr, o)
        for c in list(comb):
            if c == ():
                continue
            x_string += ", "
            for i, t in enumerate(c):
                if i == 0:
                    x_string += t
                else:
                    x_string += "*" + t
    x_string += "])"
    return x_string


class Model:
    def __init__(self, sol, time, phys_domain=None, bc="periodic", diff="finite_difference"):
        """
        This class is used to wrap the time simulation capabilities of the time_simulation submodule.
        It supplies a method to create a library of possible right-hand-side terms and creates an instance of a Time-
        simulator object used to perfom time simulations provided a vector `sigma` giving factors for linearly combining
        library terms for each variable. The overall geometry of the problem is extracted from the initial conditions
        provided during initialization.

        Parameters
        ----------
        sol : numpy.array
            Time series data
        time : numpy.array
            Array of points in time for each data point in time series data
        phys_domain : tuple
            (Optional, default=None) Physical domain size in shape e. g. ((Lx_min, Lx_max), (Ly_min, Ly_max))
            If None will set the domain size equal to the number of spatial discretization steps (if applicable)
        bc : string
            (optional, default="periodic") Sets boundary conditions (mainly for finite difference method). Options are
            "periodic" and "neumann"
        diff : string
            (optional, default="finite_difference") Sets differentiation method for spatial derivative. Options are
            "finite_difference" and "pseudo_spectral"
        """

        ic = sol[:, 0]
        self.initial_state = ic

        self.simulator = None
        self.sol = sol
        self.time = time

        self.n_variables = ic.shape[0]
        self.N = ic.shape[-1]
        self.dimension = len(ic[0].shape)
        # In case of ODE system
        if len(ic.shape) == 1:
            self.dimension = 0
            self.N = 0
        if phys_domain is None and self.dimension != 0:
            self.domain = [(0, self.N) for i in range(self.dimension)]
        else:
            # assert self.dimension is not 0, "Cannot specify physical domain for ODE system."
            self.domain = phys_domain
        self.boundary_condition = bc
        self.differentiation_method = diff

        self.ode_order = None  # Maximum number of factors in products of permutations
        self.indices_ode_to_pde = None  # Maximum order of spatial derivative
        self.pde_order = None  # Maximum order of factors in products for spatial derivatives
        self.ode_count = 0
        self.pde_count = 0
        self.custom_count = 0
        self.ode_string = None
        self.pde_string = None
        self.custom_string = None
        self._ode_comp_string = None
        self._pde_comp_string = None
        self._custom_comp_string = None
        self.sigma = None
        self.lib_strings = None

        self.sol_dot = None
        self.lot = None

    def init_library(self, ode_order=2, pde_order=2, indices=None, custom_terms=np.array([]), kind="split"):
        """
        Method that initializes all library strings up to specified order. These string will be pre-compiled and later
        evaluated in the right hand side method. They include products of all provided variabled up to order ode_order
        and their spatial derivatives up to order pde_order. Indices is used to filter only selected library terms for
        spatial differentiation.

        Parameters
        ----------
        ode_order : int
            (Optional, default=2) Order up to which products of variables (including with themselves) are included in the library
        pde_order : int
            (Optional, default=2) Order up to which spatial derivatives are to be computed
        indices : np.array
            (optional, default=None) Array of indices of library elements to be included for spatial derivation (as a
            subset of terms created undeer ode_order)
        custom_terms : np.array
            (optional, default=np.array([])) User defined string to append to library and evaluate in RHS
        kind : str
            (optional, default="split") Whether to split derivatives into each spatial direction and their combinations
            (exhaustive) or "pair" them each (non-exhaustive).

        Notes
        -----
        Library creation should focus on the array-valued attribute "lib_string" and later evaluation should use that
        array for easier manipulation of library terms. Then one wouldn't need all this bogus differentiation between
        ode, pde or custom strings. Also using strings may generally be prohibitive.

        """
        if self.dimension == 0:
            pde_order = 0

        self.ode_order = ode_order  # Maximum number of factors in products of permutations
        self.pde_order = pde_order  # Maximum order of spatial derivative
        self.ode_count = self._give_count(self.ode_order)
        if indices is None:
            self.indices_ode_to_pde = np.arange(1, self.ode_count)
        else:
            self.indices_ode_to_pde = indices
        self.pde_count = self.pde_order * self.dimension * len(self.indices_ode_to_pde)

        self.ode_string = _make_combination_string(self.ode_order, self.n_variables)
        self._ode_comp_string = compile(self.ode_string, '<string>', 'eval')

        ode_strings = self.ode_string.split(", ")
        ode_strings[-1] = ode_strings[-1][:-2]

        def make_split_pde_terms():
            x_string = "np.array(["
            for order in np.arange(1, pde_order + 1):
                for index in self.indices_ode_to_pde:
                    if self.dimension == 0:
                        x_string += "  "
                        break
                    # x_string += pre + f"self.diff.d_dx(ode_lib[{index}],{order})"
                    x_string += f"self.diff.d_dx({ode_strings[index]},{order}), "
                    if self.dimension == 2:
                        # x_string += f", self.diff.d_dy(ode_lib[{index}],{order})"
                        x_string += f"self.diff.d_dy({ode_strings[index]},{order}), "
                        combs = [c for c in combinations_wr(range(1, order + 1), 2) if sum(c) == order]
                        for comb in combs:
                            x_string += f"self.diff.dd_dxdy({ode_strings[index]},[{comb[0]},{comb[1]}]), "
                            self.pde_count += 1
                            if comb[0] != comb[1]:
                                x_string += f"self.diff.dd_dxdy({ode_strings[index]},[{comb[1]},{comb[0]}]), "
                                self.pde_count += 1
            x_string = x_string[:-2] + (pde_order == 0) * "([" + "])"
            return x_string

        def make_coupled_pde_terms():
            x_string = "np.array(["
            for order in np.arange(1, pde_order + 1):
                for index in self.indices_ode_to_pde:
                    if self.dimension == 0:
                        x_string += "  "
                        break
                    x_string += f"self.diff.div({ode_strings[index]},{order}), "
            x_string = x_string[:-2] + (pde_order == 0) * "([" + "])"
            return x_string

        if kind == "split":
            x = make_split_pde_terms()
        else:
            x = make_coupled_pde_terms()
        self.pde_string = x
        self._pde_comp_string = compile(self.pde_string, '<string>', 'eval')
        self.sigma = np.zeros((self.n_variables, (self.ode_count + self.pde_count)))

        self.lib_strings = np.concatenate((self.ode_string[10:-2].split(", "), self.pde_string[10:-2].split(", ")))
        self.add_library_terms(custom_terms)

    def add_library_terms(self, list_of_strings):
        """
        Method that adds custom python expressions as strings and adds them to the library of RHS terms.

        Parameters
        ----------
        list_of_strings : numpy.array
            Array of strings to be added, can be empty.

        """
        assert self.lib_strings is not None
        self.custom_count = len(list_of_strings)
        self.lib_strings = np.concatenate((self.lib_strings, list_of_strings))

        if len(list_of_strings) == 0:
            if self.dimension == 0:
                x_string = f"np.array([]).reshape(0, )"
            elif self.dimension == 1:
                x_string = f"np.array([]).reshape(0, {self.N})"
            elif self.dimension == 2:
                x_string = f"np.array([]).reshape(0, {self.N}, {self.N})"
        else:
            x_string = "np.array(["
            for string in list_of_strings:
                x_string += string + ", "

            x_string = x_string[:-2] + "])"

        self.custom_string = x_string
        self._custom_comp_string = compile(self.custom_string, '<string>', 'eval')
        self.sigma = np.zeros((self.n_variables, (self.ode_count + self.pde_count + self.custom_count)))

    def drop_library_terms(self, indices):
        """
        Drop terms of library at the indices specified in the argument. See 'print_library' for an output of library
        terms and their indices.

        Parameters
        ----------
        indices : list or array-like
            List of indices to be dropped from library

        Notes
        -----
        This is all way too cumbersome and should be redone (as described in the note of init_library)

        """

        assert self.lib_strings is not None
        n_drops = len(indices)
        indices = np.array(indices)
        n_ode_drops = np.sum(indices < self.ode_count)
        n_pde_drops = np.sum(np.logical_and(indices >= self.ode_count, indices < (self.ode_count + self.pde_count)))
        n_custom_drops = np.sum(np.logical_and(indices >= (self.ode_count + self.pde_count),
                                               indices < (self.ode_count + self.pde_count + self.custom_count)))
        self.ode_count -= n_ode_drops
        self.pde_count -= n_pde_drops
        self.custom_count -= n_custom_drops

        all_library_strings = self.ode_string.split(", ") + self.pde_string.split(", ") + self.custom_string.split(", ")
        new_library_strings = np.delete(np.array(all_library_strings), indices)

        new_ode_strings = new_library_strings[0:self.ode_count]
        new_pde_strings = new_library_strings[self.ode_count:(self.ode_count + self.pde_count)]
        new_custom_strings = new_library_strings[(self.ode_count + self.pde_count):]

        flags = [False, False, False]
        if len(new_ode_strings) == 0:
            new_ode_strings = [" "]
            flags[0] = True
        if len(new_pde_strings) == 0:
            new_pde_strings = [" "]
            flags[1] = True
        if len(new_custom_strings) == 0:
            new_custom_strings = [" "]
            flags[2] = True

        if new_ode_strings[0][0:10] != "np.array([":
            new_ode_strings[0] = "np.array([" + new_ode_strings[0]
        if new_pde_strings[0][0:10] != "np.array([":
            new_pde_strings[0] = "np.array([" + new_pde_strings[0]
        if new_custom_strings[0][0:10] != "np.array([":
            new_custom_strings[0] = "np.array([" + new_custom_strings[0]

        if new_ode_strings[-1][-2:] != "])":
            new_ode_strings[-1] += "])"
            if flags[0]:
                new_ode_strings[-1] += f".reshape(0, {self.N}, {self.N})"
        if new_pde_strings[-1][-2:] != "])":
            new_pde_strings[-1] += "])"
            if flags[1]:
                new_pde_strings[-1] += f".reshape(0, {len(self.x)}, {len(self.y)})"
        if new_custom_strings[-1][-2:] != "])":
            new_custom_strings[-1] += "])"
            if flags[2]:
                new_custom_strings[-1] += f".reshape(0, {self.N}, {self.N})"

        self.ode_string = ", ".join(new_ode_strings)
        self.pde_string = ", ".join(new_pde_strings)
        self.custom_string = ", ".join(new_custom_strings)
        self._ode_comp_string = compile(self.ode_string, '<string>', 'eval')
        self._pde_comp_string = compile(self.pde_string, '<string>', 'eval')
        self._custom_comp_string = compile(self.custom_string, '<string>', 'eval')
        self.sigma = np.zeros((self.n_variables, (self.ode_count + self.pde_count + self.custom_count)))
        self.lib_strings = np.delete(self.lib_strings, indices)

    def _give_count(self, order):
        """
        (Internal) helper function that gives the number of ode-type terms that will automatically be created.

        Parameters
        ----------
        order : int
            Highest order up to which products will be created

        Returns
        -------
        int
            Number of ode-type terms that will be created automatically.

        """
        count = int(sum([math.factorial(self.n_variables + o - 1) / math.factorial(o) /
                         math.factorial(self.n_variables - 1) for o in range(order + 1)]))
        return count

    def init_simulator(self, sig=None, sol=None, time=None):
        """
        Method that initializes a TimeSimulator class and object. This object is a child of 'AbstractTimesimulator' of
        the time_simulation submodule. It is extended with a method that provides a time series of the library terms
        given a time series.

        Parameters
        ----------
        sig : numpy.array
            (Optional, default=None) Vector of factors for linearly combining library terms in right hand side. If none
            the attribute self.sigma is used instead (which is initialized as all zeros).
        sol : numpy.array
            (optional, default=None) Time series data to give to the time series simulator, if None self.sol is used.
        time : numpy.array
            (optional, default=None) Time stepping data corresponding to solution, if None self.time is used.

        """
        if sig is None:
            sigma = self.sigma
        else:
            sigma = sig
        if sol is None:
            sol = self.sol
        if time is None:
            time = self.time

        ode_string = self._ode_comp_string
        pde_string = self._pde_comp_string
        custom_string = self._custom_comp_string
        initial_state = self.initial_state
        domain = self.domain
        boundary_condition = self.boundary_condition
        differentiation_method = self.differentiation_method

        if self.dimension == 1:
            n_shape = (self.N,)
        elif self.dimension == 2:
            n_shape = (self.N, self.N)

        class TimeSimulator(AbstractTimeSimulator):
            def __init__(self):
                super().__init__(initial_state, domain=domain, bc=boundary_condition,
                                 diff=differentiation_method)
                self.sigma = sigma
                self.library_over_time = None
                self.sol_dot = None

            # def rhs(self, t, u):
            #     ode_lib = eval(ode_string)
            #     pde_lib = eval(pde_string)
            #     custom_lib = eval(custom_string)
            #     vec = np.concatenate((ode_lib, pde_lib, custom_lib))
            #     u_next = [np.dot(s, [item.flatten() for item in vec]).reshape(n_shape) for s in self.sigma]
            #
            #     return np.array(u_next)

            def create_library_time_series(self, ts=None):
                if ts is None:
                    assert self.sol is not None, "Must provide time series or perform time simulation."
                    time_series = self.sol
                else:
                    time_series = ts

                # Feels inefficient (and it is)
                library_over_time = []
                for var in range(time_series.shape[0]):
                    var_lib_over_time = []
                    for t in range(time_series.shape[1]):
                        u = time_series[:, t]
                        ode_lib = eval(ode_string)
                        pde_lib = eval(pde_string)
                        custom_lib = eval(custom_string)
                        vec = np.concatenate((ode_lib, pde_lib, custom_lib))
                        var_lib_over_time.append(vec)
                    var_lib_over_time = np.swapaxes(np.array(var_lib_over_time), 0, 1)
                    library_over_time.append(var_lib_over_time)

                self.library_over_time = np.array(library_over_time)
                return self.library_over_time

        def rhs_pde(obj, t, u):
            ode_lib = eval(ode_string)
            pde_lib = eval(pde_string)
            custom_lib = eval(custom_string)
            vec = np.concatenate((ode_lib, pde_lib, custom_lib))
            u_next = [np.dot(s, [item.flatten() for item in vec]).reshape(n_shape) for s in self.sigma]
            return np.array(u_next)

        def rhs_ode(obj, t, u):
            ode_lib = eval(ode_string)
            pde_lib = eval(pde_string)
            custom_lib = eval(custom_string)
            vec = np.concatenate((ode_lib, pde_lib, custom_lib))
            u_next = [np.dot(s, [item for item in vec]) for s in self.sigma]
            return np.array(u_next)

        # This is actually batshit crazy
        sim = TimeSimulator()
        if self.dimension == 0:
            sim.rhs = rhs_ode.__get__(sim)
        else:
            sim.rhs = rhs_pde.__get__(sim)

        self.simulator = sim

        # Usually doesn't do anything
        self.simulator.sol = sol
        self.simulator.time = time

    def print_library(self, sigma=None):
        """
        Print a readable table of library terms, their index and if available their linear factor.

        Parameters
        ----------
        sigma : numpy.array
            (optional, default=None) If not None, replace values of linear combination factors with values stored in
            this array.

        """
        if self.sigma is None:
            print(tabulate(zip(range(len(self.lib_strings)), self.lib_strings), headers=["Index", "Term"]))
        else:
            if sigma is not None:
                sigma_loc = sigma
            else:
                sigma_loc = self.sigma
            headers = ["Index", "Term"]
            for i in range(sigma_loc.shape[0]):
                headers.append(f"Value {i}")  # could do this with list comprehension

            strings = [item[10:] if item[:10] == "self.diff." else item for item in self.lib_strings]
            if strings[0] == "np.ones(u[0].shape)":
                strings[0] = "1.0"

            print(tabulate(zip(range(len(self.lib_strings)), strings, *sigma_loc), headers=headers))

    def optimize_sigma(self, lamb=0.1, thres=0.01, error="BIC", **kwargs):
        """
        Optimize sigma using variation of training for sequencing threshold ridge regression. See Module `opimization`
        for details.

        Parameters
        ----------
        lamb : float
            (Optional, default=0.1) Sparsity knob to promote sparsity in regularisation

        thres : float
            (Optional, default=0.01) Threshold below which values are cut in sequence of regression

        error : string
            (Optional, default="BIC") Keyword argument to pass to optimization routine. Choices are "BIC" for
            bayesian information criterion using integration, "SINDy" for the sum of squared differences in derivative
            and library reconstruction and "integrate" for sum of squared differences in original time series and
            integrated library reconstruction. (Both "SINDy" and "integrate" additionally punish non-sparsity,
            adjustable with the additional keyword argument `l0`.)

        """
        print("Generating test functions (this may take some time)...")
        if self.sol_dot is None:
            self.sol_dot = self.simulator.get_sol_dot()
        if self.lot is None:
            self.lot = self.simulator.create_library_time_series()
        # sol_dot_flat = sol_dot.reshape((sol_dot.shape[0], -1))
        # lot_flat = lot.reshape((lot.shape[0], lot.shape[1], -1))

        sigma_opt, error = train_ridge_wip(self.lot, self.sol, self.sol_dot, self.time, lamb, thres, error=error,
                                           **kwargs)

        self.sigma = sigma_opt
        print("New Sigma set to: \n")

        self.print_library()

    def least_square_sigma(self, lamb=None):
        """
        Method that performs a least-square fit using numpy to fit the library to the derivative of the time series,
        without any regard for sparsity or further optimization (mainly for debugging purposes).

        Parameters
        ----------
        lamb : float or None
            (Optional, default=None) If provided adds the ridge-regression term for promoting sparsity, then `lamb` is
            the sparsity knob otherwise perform ordinary least-square fit

        """
        if self.sol_dot is None:
            self.sol_dot = self.simulator.get_sol_dot()
        if self.lot is None:
            self.lot = self.simulator.create_library_time_series()

        sol_dot_flat = self.sol_dot.reshape((self.sol_dot.shape[0], -1))
        lot_flat = self.lot.reshape((self.lot.shape[0], self.lot.shape[1], -1))
        if lamb is None:
            sigma = [np.linalg.lstsq(lot_flat[i].T, sol_dot_flat[i], rcond=None)[0] for i in range(self.n_variables)]
        else:
            sigma = [np.linalg.lstsq(lot_flat[i].dot(lot_flat[i].T) +
                                     lamb * np.eye(self.lot.shape[1]), lot_flat[i].dot(sol_dot_flat[i]), rcond=None)[0]
                     for i in range(self.n_variables)]
        self.sigma = np.array(sigma)

        self.print_library()
