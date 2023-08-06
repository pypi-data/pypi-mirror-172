import numpy as np
import scipy.integrate as integrate
import optuna
from gradient_free_optimizers import HillClimbingOptimizer
import nevergrad as ng
from hyperopt import fmin, hp, tpe
from tqdm import tqdm


# Maybe at some point add option for sklearns ridge regressor:
# from sklearn.linear_model import Ridge


def sequencing_threshold_ridge(lib, data, lamb, tol=1e-4, max_it=10, norm=2):
    """
    This reproduces the sequencing threshold ridge regression as it is implemented in PDE-FIND.

    Parameters
    ----------
    lib : np.array
        Time series of library terms as produced by a simulator instance via method create_library_time_series or of
        shape (# Variables, # Time Steps, # Library Terms, Dim1, Dim2(if applicable))
    data : np.array
        Time series to be fitted to (in shape (# Variable, # Time steps, Dim1, Dim2(if applicabe)))
    lamb : float
        Sparsity knob to promote sparsity in regularisation
    tol : float
        (Optional, default: 1e-4) Threshold below which values are cut in sequence of regression
    max_it : int
        (Optional, default: 10) Maximum number of iterations in sequence of regressions
    norm : int
        (Optional, default: 2) Give the norm with which to normalize data

    Returns
    -------
    np.array of weights for linear combination of library terms to best achieve data series

    """
    # Initialize weights and read the number of variables and the number of library terms
    w = []
    n_var = lib.shape[0]
    n_terms = lib.shape[1]

    # We try to find a set of weights for every variables right hand side
    for var in range(n_var):
        # Read and reshape the library terms for the current variable, here we flatten all except the first dimension
        x = np.reshape(lib[var], (lib[var].shape[0], np.prod(lib[var].shape[1:])))
        # Flatten the corresponding data time series
        y = data[var].flatten()
        # When normalization is set, save the scaling factor and normalize the library according to the parameter norm
        l_norm = None
        tol_loc = tol
        if norm != 0:
            l_norm = 1.0 / (np.linalg.norm(x, norm))
            x = l_norm * x
            tol_loc = tol_loc / l_norm
        if lamb != 0:
            # If a sparsity knob is given get the standard ridge estimate
            w_loc = np.linalg.lstsq(x.dot(x.T) + lamb * np.eye(n_terms), x.dot(y), rcond=None)[0]
        else:
            # else perform ordinary least squares fit
            w_loc = np.linalg.lstsq(x.T, y, rcond=None)[0]

        # Set the number of relevant terms to the number of all terms
        n_relevant = n_terms
        for i in range(max_it):
            # We find all the indices which hold values below our threshold and the remaining indices
            off_indices = np.where(np.abs(w_loc) < tol_loc)[0]
            new_on_indices = np.delete(np.arange(n_terms), off_indices)

            if n_relevant == len(new_on_indices):
                # Stop if the number of relevant terms does not change
                break
            else:
                # Update the number of relevant terms
                n_relevant = len(new_on_indices)

            on_indices = new_on_indices

            if len(on_indices) == 0:
                # If all indices have been tossed stop (if this happend during the first iteration return the value)
                if i == 0:
                    # w.append(w_loc)
                    break
                else:
                    break

            # Cut off all values to the corresponding indices
            w_loc[off_indices] = 0
            # Get knew ridge or least square estimate
            if lamb != 0:
                w_loc[on_indices] = np.linalg.lstsq(x[on_indices].dot(x[on_indices].T) +
                                                    lamb * np.eye(len(on_indices)), x[on_indices].dot(y), rcond=None)[0]
            else:
                w_loc[on_indices] = np.linalg.lstsq(x[on_indices].T, y, rcond=None)[0]

        # Normalize the weights
        if norm != 0:
            w_loc[np.where(np.abs(w_loc) < tol_loc)[0]] = 0
            w.append(np.multiply(l_norm, w_loc))
        else:
            w_loc[np.where(np.abs(w_loc) < tol_loc)[0]] = 0
            w.append(w_loc)

    return np.array(w)


def train_ridge(lib, data, lamb, thres, l0=None, split=0.7, seed=1234, max_it_train=10, max_it=10, norm=2):
    np.random.seed(seed)
    n_timesteps = lib.shape[2]
    x = np.reshape(lib, (lib.shape[0], lib.shape[1], np.prod(lib.shape[2:])))
    y = np.reshape(data, (data.shape[0], np.prod(data.shape[1:])))

    train_indices = np.random.choice(x.shape[-1], int(x.shape[-1] * split), replace=False)
    test_indices = np.delete(np.arange(x.shape[-1]), train_indices)

    x_train = x[:, :, train_indices]
    y_train = y[:, train_indices]

    x_test = x[:, :, test_indices]
    y_test = y[:, test_indices]

    d_tol = float(thres)
    tol = thres
    tol_best = tol

    if l0 is None:
        l0 = 0.001 * np.linalg.norm(np.linalg.cond(x), 2)

    def error(w_test):
        errors = [np.linalg.norm(y_test[i] - x_test[i].T.dot(w_test[i]), 2)
                  for i in range(x_test.shape[0])]
        error_test = np.sum(errors) + l0 * np.count_nonzero(w_test)
        return error_test

    w_best = np.array([np.linalg.lstsq(x_test[i].T, y_test[i], rcond=None)[0]
                       for i in range(x_test.shape[0])])
    error_best = error(w_best)

    pbar = tqdm(range(max_it_train))
    pbar.set_description(f"Training sequencing threshold ridge regression with "
                         f"{split * 100:.0f} % split")
    for i in pbar:
        w = sequencing_threshold_ridge(x_train, y_train, lamb, max_it=max_it, tol=tol, norm=norm)
        err = error(w)

        if err <= error_best:
            error_best = err
            tol_best = tol
            w_best = w
            tol = tol + d_tol
        else:
            tol = max([0, tol - 2 * d_tol])
            d_tol = 2 * d_tol / (max_it_train - i)
            tol = tol + d_tol
        pbar.set_postfix({"Threshold": tol_best, "Error": error_best})

    return np.array(w_best), error_best


def train_ridge_wip(lib, data, data_dot, time, lamb, thres, l0=None, seed=1234, max_it_train=10, max_it=10, norm=2,
                    error="BIC"):
    np.random.seed(seed)
    n_timesteps = lib.shape[2]
    # reshaping is done inconsistently
    # x = np.reshape(lib, (lib.shape[0], lib.shape[1], np.prod(lib.shape[2:])))
    # y = np.reshape(data_dot, (data_dot.shape[0], np.prod(data_dot.shape[1:])))
    x = lib
    y = data_dot

    d_tol = float(thres)
    tol = thres
    tol_best = tol

    if l0 is None:
        l0 = 0.001 * np.linalg.norm(np.linalg.cond(x.reshape((x.shape[0], x.shape[1], np.prod(x.shape[2:])))), 2)

    def error_der(w_test):
        errors = [np.linalg.norm(data_dot[i] - x[i].T.dot(w_test[i]), 2)
                  for i in range(x.shape[0])]
        error_test = np.sum(errors) + l0 * np.count_nonzero(w_test)
        return error_test

    def error_sp(w_test):
        errors = [np.linalg.norm(data[i, 1:] - integrate.cumtrapz(x[i].T.dot(w_test[i]), time).T)
                  for i in range(x.shape[0])]

        error_test = np.sum(errors) + l0 * np.count_nonzero(w_test)
        return error_test

    def error_bic(w_test):
        errors = np.array([np.linalg.norm(data[i, 1:] - integrate.cumtrapz(x[i].T.dot(w_test[i]), time).T)
                           for i in range(x.shape[0])])
        errors = errors.flatten() ** 2
        logL = -len(time) * np.log(errors.sum() / len(time)) / 2
        p = np.count_nonzero(w_test)
        bic = -2 * logL + p * np.log(len(time))
        return bic

    if error == "BIC":
        error_func = error_bic
    elif error == "integrate":
        error_func = error_sp
    elif error == "SINDy":
        error_func = error_der
    else:
        raise NotImplementedError("Unrecognized Error function")

    w_best = np.array([np.linalg.lstsq(x[i].reshape(x.shape[1], -1).T, y[i].flatten(), rcond=None)[0]
                       for i in range(x.shape[0])])
    error_best = error_func(w_best)

    pbar = tqdm(range(max_it_train))
    pbar.set_description(f"Training sequencing threshold ridge regression with " + error + "  error")
    for i in pbar:
        w = sequencing_threshold_ridge(x, y, lamb, max_it=max_it, tol=tol, norm=norm)
        err = error_func(w)

        if err <= error_best:
            error_best = err
            tol_best = tol
            w_best = w
            tol = tol + d_tol
        else:
            tol = max([0, tol - 2 * d_tol])
            d_tol = 2 * d_tol / (max_it_train - i)
            tol = tol + d_tol
        pbar.set_postfix({"Threshold": tol_best, "Error": error_best})

    return np.array(w_best), error_best


def optimize(lib, data, data_dot, time):
    def training_loss_bic(weights):
        errors = np.array([np.linalg.norm(data[i, 1:] - integrate.cumtrapz(lib[i].T.dot(weights[i]), time).T)
                           for i in range(lib.shape[0])])
        errors = errors.flatten() ** 2
        logL = -len(time) * np.log(errors.sum() / len(time)) / 2
        p = np.count_nonzero(weights)
        bic = -2 * logL + p * np.log(len(time))
        return bic

    def BIC(lamb):
        weights = sequencing_threshold_ridge(lib, data_dot, lamb)
        return training_loss_bic(weights)

    opt = fmin(BIC, space=hp.loguniform("l", -20, 0), algo=tpe.suggest, max_evals=20)
    print(f"Optimal lambda found: {opt['l']}")
    return sequencing_threshold_ridge(opt["l"])


def optimize_ridge_optuna(lib, data, split=0.7, seed=1234, trials=20, tol_range=[1e-4, 2], lamb_range=[0, 2]):
    np.random.seed(seed)
    # l0 = 0.001 * np.linalg.norm(np.linalg.cond(lib), 2)
    x = np.reshape(lib, (lib.shape[0], lib.shape[1], np.prod(lib.shape[2:])))
    y = np.reshape(data, (data.shape[0], np.prod(data.shape[1:])))

    train_indices = np.random.choice(x.shape[-1], int(x.shape[-1] * split), replace=False)
    test_indices = np.delete(np.arange(x.shape[-1]), train_indices)

    x_train = x[:, :, train_indices]
    y_train = y[:, train_indices]

    x_test = x[:, :, test_indices]
    y_test = y[:, test_indices]

    l0 = 0.001 * np.linalg.norm(np.linalg.cond(x), 2)

    def error(w_test):
        errors = [np.linalg.norm(y_test[i] - x_test[i].T.dot(w_test[i]), 2)
                  for i in range(x_test.shape[0])]
        error_test = np.sum(errors) + l0 * np.count_nonzero(w_test)
        return error_test

    def objective(trial):
        tol = trial.suggest_float("tol", tol_range[0], tol_range[1])
        # tol = 1.0
        lamb = trial.suggest_float("lamb", lamb_range[0], lamb_range[1])
        # lamb = 0.01
        w = sequencing_threshold_ridge(x_train, y_train, lamb, tol=tol)
        # errors = [np.linalg.norm(data[i].flatten() - lib[i].T.dot(w[i]).flatten(), 2)
        #          for i in range(lib.shape[0])]
        # error_test = np.sum(errors) + l0 * np.count_nonzero(w)# + 1 / np.sum([np.linalg.norm(wi, 2) for wi in w])
        error_test = error(w)
        return error_test

    study = optuna.create_study()
    study.optimize(objective, n_trials=trials)
    params = study.best_params
    lam_best = params["lamb"]
    # lam_best = 0.01
    tol_best = params["tol"]
    # tol_best = 1.0

    return sequencing_threshold_ridge(lib, data, lam_best, tol=tol_best)


def optimize_ridge_gfo(lib, data, split=0.7, seed=1234, trials=20, tol_range=[1e-4, 2], lamb_range=[0, 2]):
    np.random.seed(seed)
    # l0 = 0.001 * np.linalg.norm(np.linalg.cond(lib), 2)
    x = np.reshape(lib, (lib.shape[0], lib.shape[1], np.prod(lib.shape[2:])))
    y = np.reshape(data, (data.shape[0], np.prod(data.shape[1:])))

    train_indices = np.random.choice(x.shape[-1], int(x.shape[-1] * split), replace=False)
    test_indices = np.delete(np.arange(x.shape[-1]), train_indices)

    x_train = x[:, :, train_indices]
    y_train = y[:, train_indices]

    x_test = x[:, :, test_indices]
    y_test = y[:, test_indices]

    l0 = 0.001 * np.linalg.norm(np.linalg.cond(x), 2)

    def error(w_test):
        errors = [np.linalg.norm(y_test[i] - x_test[i].T.dot(w_test[i]), 2)
                  for i in range(x_test.shape[0])]
        error_test = np.sum(errors) + l0 * np.count_nonzero(w_test)
        return error_test

    def objective(para):
        tol = para["tol"]
        # tol = 1.0
        lamb = para["lamb"]
        # lamb = 0.01
        w = sequencing_threshold_ridge(x_train, y_train, lamb, tol=tol)
        # errors = [np.linalg.norm(data[i].flatten() - lib[i].T.dot(w[i]).flatten(), 2)
        #          for i in range(lib.shape[0])]
        # error_test = np.sum(errors) + l0 * np.count_nonzero(w)# + 1 / np.sum([np.linalg.norm(wi, 2) for wi in w])
        error_test = error(w)
        return - error_test

    search_space = {"tol": tol_range, "lamb": lamb_range}
    opt = HillClimbingOptimizer(search_space)
    opt.search(objective, n_iter=trials)

    lam_best, tol_best = opt.best_value

    return sequencing_threshold_ridge(lib, data, lam_best, tol=tol_best)


def optimize_ridge_optuna_wip(model, split=0.7, seed=1234, trials=20, tol_range=[1e-4, 2], lamb_range=[0, 2]):
    lib = model.simulator.library_over_time
    data = model.simulator.sol_dot
    time = model.simulator.time
    Nt = len(time)

    np.random.seed(seed)
    # l0 = 0.001 * np.linalg.norm(np.linalg.cond(lib), 2)
    x = np.reshape(lib, (lib.shape[0], lib.shape[1], np.prod(lib.shape[2:])))
    y = np.reshape(data, (data.shape[0], np.prod(data.shape[1:])))

    train_indices = np.random.choice(x.shape[-1], int(x.shape[-1] * split), replace=False)
    test_indices = np.delete(np.arange(x.shape[-1]), train_indices)

    x_train = x[:, :, train_indices]
    y_train = y[:, train_indices]

    x_test = x[:, :, test_indices]
    y_test = y[:, test_indices]

    l0 = 0.001 * np.linalg.norm(np.linalg.cond(x), 2)

    def error(w_test):
        # errors = [np.linalg.norm(y_test[i] - x_test[i].T.dot(w_test[i]), 2)
        #           for i in range(x_test.shape[0])]

        model.simulator.sigma = w_test
        y_estimate = model.simulator.simulate([time[0], time[-1]], t_eval=time)
        diff = ((model.sol - y_estimate).flatten()) ** 2
        logL = -Nt * np.log(diff.sum() / Nt) / 2

        s = w_test.flatten()
        s[np.abs(s != 0)] /= np.abs(s[s != 0])
        p = np.abs(s).sum()

        bic = -2 * logL + p * np.log(Nt)

        return bic

    def objective(trial):
        tol = trial.suggest_float("tol", tol_range[0], tol_range[1])
        # tol = 1.0
        lamb = trial.suggest_float("lamb", lamb_range[0], lamb_range[1])
        # lamb = 0.01
        w = sequencing_threshold_ridge(x_train, y_train, lamb, tol=tol)
        # errors = [np.linalg.norm(data[i].flatten() - lib[i].T.dot(w[i]).flatten(), 2)
        #          for i in range(lib.shape[0])]
        # error_test = np.sum(errors) + l0 * np.count_nonzero(w)# + 1 / np.sum([np.linalg.norm(wi, 2) for wi in w])
        error_test = error(w)
        return error_test

    study = optuna.create_study()
    study.optimize(objective, n_trials=trials)
    params = study.best_params
    lam_best = params["lamb"]
    # lam_best = 0.01
    tol_best = params["tol"]
    # tol_best = 1.0

    return sequencing_threshold_ridge(lib, data, lam_best, tol=tol_best)


def optimize_wip(model, w_init, trials=20, n_time=5):
    time = model.simulator.time[:n_time]
    Nt = len(time)

    def error(w_test):
        # errors = [np.linalg.norm(y_test[i] - x_test[i].T.dot(w_test[i]), 2)
        #           for i in range(x_test.shape[0])]

        model.simulator.sigma = w_test
        y_estimate = model.simulator.simulate([time[0], time[-1]], t_eval=time)
        try:
            diff = ((model.sol - y_estimate).flatten()) ** 2
        except ValueError:
            diff = np.array([1e10])

        logL = -Nt * np.log(diff.sum() / Nt) / 2

        s = w_test.flatten()
        s[np.abs(s != 0)] /= np.abs(s[s != 0])
        p = np.abs(s).sum()

        bic = -2 * logL + p * np.log(Nt)

        return bic

    instru = ng.p.Instrumentation(ng.p.Array(init=w_init))
    optimizer = ng.optimizers.NGOpt(parametrization=instru, budget=trials)
    recommendation = optimizer.minimize(error)

    return recommendation.value[0][0]
