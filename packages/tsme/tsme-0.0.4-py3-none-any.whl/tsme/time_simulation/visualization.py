import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation, rc

rc("text", usetex=True)


def animate(sol, title="", savepath=None, fig_size=(6, 6), variable=0):
    """
    Method that animates the time evolution of the defined system. Optionally saves an mp4 video file to
    'savepath'.

    Parameters
    ----------
    sol : np.array
        Array of shape either (#Variables, #Timesteps, #Dim1) or (#Variables, #Timesteps, #Dim1, #Dim2)
    title : string
        (Optional, default="") Give a title for the resulting animation
    savepath : string
        (Optional, default=None) Give a savepath for the animation
    fig_size : tuple
        (Optional, default=(6, 6)) Give a figure size for matplotlib
    variable : int
        (Optional, default=0) Gives the index of the variable to show (if there are more than one)

    Returns
    -------
    None

    """
    fig, ax = plt.subplots(figsize=fig_size)
    dimension = len(sol.shape) - 2

    if dimension == 2:
        sol_img = ax.imshow(sol[variable, 0])
    elif dimension == 1:
        sol_img, = ax.plot(sol[variable, 0])
    else:
        raise NotImplementedError("Only 1D and 2D solutions can be animated.")

    # This feels stupid (trying to avoid "if" in animation call)+
    def anime2d(i):
        plt.title(title + f" Timesteps: {i}")

        sol_img.set_data(sol[variable, i])
        return sol_img

    def anime1d(i):
        plt.title(title + f" Timesteps: {i}")

        sol_img.set_ydata(sol[variable, i])
        return sol_img

    # This feels even more stupid
    if dimension == 2:
        anime = anime2d
    elif dimension == 1:
        anime = anime1d

    anima = animation.FuncAnimation(fig, anime, frames=np.arange(0, len(sol[variable, :]), 1), interval=10,
                                    repeat=False)
    if savepath is not None:
        Writer = animation.writers["ffmpeg"]
        writer = Writer(fps=15, bitrate=1800)
        anima.save(savepath, writer=writer)
    else:
        plt.show()
