"""
a collection of frequently used methods
"""

import numpy as np
from matplotlib import ticker as tick
from matplotlib import pyplot as plt


class FileOps:
    """
    a collection of often used file operation methods
    """

    @classmethod
    def import_csv(cls, path) -> np.ndarray:
        """
        a function that imports a numpy array from a .csv file
        :param path: raw string, path to file
        :return arr: data from file in the form of a numpy array
        """

        # Input Validation
        assert isinstance(path, str), f"Error in 'path', {path} is not of type 'str'"

        # Method Logic
        arr = np.loadtxt(open(path, "rb"), delimiter=",")
        return arr

    @classmethod
    def export_csv(cls, path, arr) -> None:
        """
        a function that exports a numpy array to a .csv file as a side effect
        :param path: raw string, desired path to saved file
        :param arr: numpy array to be exported
        :return: None
        """

        # Input validation
        assert isinstance(path, str), f"Error in 'path', {path} is not of type 'str'"
        assert isinstance(arr, np.ndarray), f"Error in arr, {arr} is not of type 'ndarray'"

        # Method Logic
        np.savetxt(open(path, "wb"), arr, delimiter=",")


class PlotTemplates:
    """
    A Collection of often used plotting template methods
    """

    @classmethod
    def build_plot(cls, xstr="", ystr="", xscale="linear", yscale="linear", xlim=(0, 0), ylim=(0, 0)):
        """
        a method that builds figure and axis objects
        :param xstr: text to go on x-axis
        :param ystr: text to go on y-axis
        :param xscale: scale of x-axis
        :param yscale: scale of y-axis
        :param xlim: tuple of x-limits
        :param ylim: tuple of y-limits
        :return: fig, ax: Matplotlib figure and axis objects
        """
        
        # Input Validation
        assert isinstance(xstr, str), f"Error in 'xstr', {xstr} is not of type 'str'"
        assert isinstance(ystr, str), f"Error in 'ystr', {ystr} is not of type 'str'"
        assert isinstance(xscale, str), f"Error in 'xscale', {xscale} is not of type 'str'"
        assert isinstance(yscale, str), f"Error in 'yscale', {yscale} is not of type 'str'"
        assert isinstance(xlim, tuple), f"Error in 'xlim', {xlim} is not of type 'tuple'"
        assert isinstance(ylim, tuple), f"Error in 'ylim', {ylim} is not of type 'tuple'"
        
        # Method Logic
        plt.rcParams["text.usetex"] = True
        fig, ax = plt.subplots(figsize=(4, 3))
        fig.set_dpi(300)
        ax.set_xlabel(xstr)
        ax.set_ylabel(ystr)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_xscale(xscale)
        ax.set_yscale(yscale)
        ax.xaxis.grid(True, which="major")
        ax.yaxis.grid(True, which="major")
        plt.gca().yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
        plt.gca().xaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
        plt.ticklabel_format(style='sci', scilimits=(0, 0))
        plt.minorticks_on()
        tick.AutoMinorLocator(n=5)
        return fig, ax

    @classmethod
    def __default_axis(cls, arr) -> tuple:
        """
        A method that sets the default axis slightly larger than the given data
        :param arr: numpy array that the scale is to be based on
        :return:
        """
        # input validation
        assert isinstance(arr, np.ndarray), f"Error in 'arr', {arr} is not of type 'ndarray'"

        umult = 1.05  # Max Axis Multiplier
        lmult = 0.95  # Min Axis Multiplier
        return tuple([np.min(arr) * lmult, np.max(arr) * umult])
    
    @classmethod
    def line_plot(cls, x, y, xstr="", ystr="", xscale="linear", yscale="linear", xlim=(0,0), ylim=(0,0)) -> None:
        """
        A Function that generates x vs y line plots
        :param x: x data
        :param y: y data
        :param xstr: text to go on x-axis
        :param ystr: text to go on y-axis
        :param xscale: scale of x-axis
        :param yscale: scale of y-axis
        :param xlim: tuple of x-limits
        :param ylim: tuple of y-limits
        :return None
        """

        # Input Validation
        assert isinstance(x, np.ndarray), f"Error in 'x', {x} is not of type 'ndarray'"
        assert isinstance(y, np.ndarray), f"Error in 'y', {y} is not of type 'ndarray'"

        # Method Logic
        if xlim == (0, 0):
            xlim = cls.__default_axis(x)
        if ylim == (0, 0):
            ylim = cls.__default_axis(y)
        fig, ax = cls.build_plot(xstr, ystr, xscale, yscale, xlim, ylim)
        ax.plot(x, y)

    @classmethod
    def bar_plot(cls, x, y, xstr="", ystr="", xscale="linear", yscale="linear", xlim=(0,0), ylim=(0,0)) -> None:
        """
        A Function that generates x vs y bar plots
        :param x: x data
        :param y: y data
        :param xstr: text to go on x-axis
        :param ystr: text to go on y-axis
        :param xscale: scale of x-axis
        :param yscale: scale of y-axis
        :param xlim: tuple of x-limits
        :param ylim: tuple pf y-limits
        :return None
        """

        # Input Validation
        assert isinstance(x,np.ndarray), f"Error in 'x', {x} is not of type 'ndarray'"
        assert isinstance(y,np.ndarray), f"Error in 'y', {y} is not of type 'ndarray'"

        # Method Logic
        if xlim == (0, 0):
            xlim = cls.__default_axis(x)
        if ylim == (0, 0):
            ylim = cls.__default_axis(y)
        fig, ax = cls.build_plot(xstr, ystr, xscale, yscale, xlim, ylim)
        ax.bar(x, y)

        return
    
    @classmethod
    def linear_regression(cls, x, y, xstr="", ystr="", xscale="linear", yscale="linear", xlim=(0,0), ylim=(0,0)) -> list:
        """
        A Function that generates and plots a linear regression of x and y
        :param x: x data
        :param y: y data
        :param xstr: text to go on x-axis
        :param ystr: text to go on y-axis
        :param xscale: scale of x-axis
        :param yscale: scale of y-axis
        :param xlim: tuple of x-limits
        :param ylim: tuple pf y-limits
        :return None
        """
        
        coefs = np.polyfit(x, y, 1)
        xmodel = np.linspace(np.min(x), np.max(y),1000)
        ymodel = xmodel*coefs[0] + coefs[1]

        # Input Validation
        assert isinstance(x,np.ndarray), f"Error in 'x', {x} is not of type 'ndarray'"
        assert isinstance(y,np.ndarray), f"Error in 'y', {y} is not of type 'ndarray'"

        # Method Logic
        if xlim == (0, 0):
            xlim = cls.__default_axis(x)
        if ylim == (0, 0):
            ylim = cls.__default_axis(y)
        
        fig, ax = PlotTemplates.build_plot(xstr, ystr, xscale, yscale, xlim, ylim)
        ax.plot(x, y, "r.")
        ax.plot(xmodel, ymodel, "b")
        
        return [f"y={coefs[0]}x+{coefs[1]}", f"r^2 = {1-(np.sum((y-(coefs[0]*x+coefs[1]))**2))/(np.sum((y-np.mean(y))**2))}"]
