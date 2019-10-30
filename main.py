"""
main.py
"""
from animation import Animation
import tkinter as tk
import numpy as np
from matplotlib.backends import backend_tkagg
from functions import Functionx
import matplotlib.pyplot as plt


class Main(Animation):
    """
    The main part of the program.
    """
    def __init__(self) -> None:
        """
        The constructor.
        """

        # Make all of the matplotlib objects
        Animation.__init__(self)
        self.ax = self.figure.subplots(nrows=2, ncols=1)
        self.figure.subplots_adjust(wspace=0.75, hspace=0.75)
        # self.figure.tight_layout()
        self.f = Functionx("(a/(sqrt(2*pi*sigma**2)))*"
                           "exp(-(1/2)*((x - mu)/sigma)**2)")
        self.x = np.linspace(-np.pi, np.pi, 512)
        line, = self.ax[0].plot(self.x, self.f(self.x, 1, 1, 1))
        f = np.fft.fftshift(np.fft.fft(self.f(self.x, 1, 1, 1)))/len(self.x)
        dx = self.x[1] - self.x[0]
        freq = 2*np.pi*np.fft.fftshift(np.fft.fftfreq(len(self.x), d=dx))
        line2, = self.ax[1].plot(freq, np.real(f),
                                 label="Real part", linewidth=0.5)
        line3, = self.ax[1].plot(freq, np.imag(f),
                                 label="Imaginary part", linewidth=0.5)
        line4, = self.ax[1].plot(freq, np.abs(f), color="black",
                                 label="Absolute Value", linewidth=1.0)
        self.ax[1].legend(prop={'size': 6})
        self.ax[1].set_xlim(np.min(freq), np.max(freq))
        self.ax[1].set_xlabel("Angular Frequency")
        self.ax[1].set_ylabel("Amplitude")
        self.ax[1].set_ylim(-0.25, 0.25)
        self.ax[1].set_title("Fourier Transform of f(x)")
        self.ax[1].grid()
        self.ax[0].set_xlim(self.x[0], self.x[-1])
        self.ax[0].set_xlabel("x")
        self.ax[0].set_ylabel("y")
        self.ax[0].set_ylim(-2, 2)
        self.ax[0].set_title("Function f(x)")
        self.ax[0].grid()
        self.line = line
        self.line2 = line2
        self.line3 = line3
        self.line4 = line4
        self.fourier_amps = f
        self.freq = freq
        xbounds = self.ax[0].get_xlim()
        ybounds = self.ax[0].get_ylim()
        s = (-xbounds[0] + xbounds[1])/50 + xbounds[0]
        y = (ybounds[1] - ybounds[0])*0.8 + ybounds[0]
        # y = 100
        self.text = self.ax[0].text(s, y, r"f(x) = $%s$" % (self.f.latex_repr))
        self.text.set_bbox({"facecolor": "white", "alpha": 1.0})
        self.autoaddartists = True

        # Tkinter main window
        self.window = tk.Tk()

        # Thanks to stackoverflow user rudivonstaden for
        # giving a way to get the colour of the tkinter widgets:
        # https://stackoverflow.com/questions/11340765/
        # default-window-colour-tkinter-and-hex-colour-codes
        #
        #     https://stackoverflow.com/q/11340765
        #     [Question by user user2063:
        #      https://stackoverflow.com/users/982297/user2063]
        #
        #     https://stackoverflow.com/a/11342481
        #     [Answer by user rudivonstaden:
        #      https://stackoverflow.com/users/1453643/rudivonstaden]
        #
        colour = self.window.cget('bg')
        if colour == 'SystemButtonFace':
            colour = "#F0F0F0"

        # Thanks to stackoverflow user user1764386 for
        # giving a way to change the background colour of a plot.
        #
        #    https://stackoverflow.com/q/14088687
        #    [Question by user user1764386:
        #     https://stackoverflow.com/users/1764386/user1764386]
        #
        self.figure.patch.set_facecolor(colour)

        self.window.title("Plot")
        self.window.configure()

        # Canvas
        self.canvas = \
            backend_tkagg.FigureCanvasTkAgg(
                self.figure,
                master=self.window
            )
        self.canvas.get_tk_widget().grid(
            row=0,
            column=0,
            rowspan=19,
            columnspan=2
            )

        # All the other widgets
        self.enterfunctionlabel = tk.Label(self.window,
                                           text="Enter function f(x)")
        self.enterfunctionlabel.grid(
                row=0,
                column=3,
                columnspan=2,
                sticky=tk.W + tk.E + tk.S,
                padx=(10, 10)
                )
        self.enter_function = tk.Entry(self.window)
        self.enter_function.bind("<Return>", self.update_function_by_entry)
        self.enter_function.grid(
            row=1,
            column=3,
            columnspan=2,
            sticky=tk.W + tk.E + tk.N + tk.S,
            padx=(10, 10)
            )
        self.enter_function_button = tk.Button(self.window,
                                               text="OK",
                                               command=
                                               self.update_function_by_entry)
        self.enter_function_button.grid(
            row=2,
            column=3,
            columnspan=2,
            sticky=tk.W + tk.E + tk.N,
            padx=(10, 10)
            )
        self.function_menu_dict = {
            "Normal Distribution": "a*exp(-(x-mu)**2/(2*sigma**2 ))"
            "/sqrt(2*pi*sigma**2)",
            "Sinusoidal Function 1": "a*sin(20*k*(x - phi))",
            "Sinusoidal Function 2": "a*sin(50*k*(x - phi))",
            "Sinc Function": "a*sinc(20*k*(x - phi))",
            "Rectangle Function": "a*rect(k*(x - b))",
            "Wavepacket": "a*sin(50*k*(x - phi))*exp(-(x-b)**2/"
            "(2*sigma**2 ))/sqrt(2*pi*sigma**2)"
            }
        self.function_menu_string = tk.StringVar(self.window)
        self.function_menu_string.set("Preset function f(x)")
        self.function_menu = tk.OptionMenu(
            self.window,
            self.function_menu_string,
            *tuple(key for key in self.function_menu_dict),
            # text="Choose a preset potential"
            command=self.update_function_by_preset
            )
        self.function_menu.grid(
            row=3,
            column=3,
            columnspan=2,
            sticky=tk.W + tk.E + tk.S,
            padx=(10, 10)
            )
        self.sliderslist = []
        self.set_sliders()

    def lim_update(self) -> None:
        """
        Update the ylimits.
        """
        ymin = np.amin(np.real(self.fourier_amps))
        ymax = np.amax(np.real(self.fourier_amps))
        plt.draw()
        self.ax[1].set_ylim(ymin, ymax)

    def _update_function(self, str_args: str) -> None:
        """
        Helper function for update_function_by_entry and
        update_function_by_preset.
        """
        self.f = Functionx(str_args)
        ones = ([1 for i in range(len(self.f.symbols) - 1)])
        self.line.set_ydata(self.f(self.x, *ones))
        self.fourier_amps = np.fft.fftshift(
                np.fft.fft(self.f(self.x, *ones)))/len(self.x)
        self.line2.set_ydata(np.real(self.fourier_amps))
        self.line3.set_ydata(np.imag(self.fourier_amps))
        self.line4.set_ydata(np.abs(self.fourier_amps))
        self.text.set_text("f(x) = $%s$" % (self.f.latex_repr))
        self.set_sliders()
        # self.lim_update()

    def update_function_by_entry(self, *event: tk.Event) -> None:
        """
        Update the function.
        """
        str_args = self.enter_function.get()
        self.function_menu_string.set("Preset function f(x)")
        self._update_function(str_args)

    def update_function_by_preset(self, str_args: tk.StringVar) -> None:
        """
        Update a function by preset.
        """
        self._update_function(str(self.function_menu_dict[str_args]))

    def slider_update(self, *event: tk.Event) -> None:
        """
        Update the functions given input from the slider.
        """
        tmplist = []
        for i in range(len(self.sliderslist)):
            tmplist.append(self.sliderslist[i].get())
        self.line.set_ydata(self.f(self.x, *tmplist))
        self.fourier_amps = np.fft.fftshift(
                np.fft.fft(self.f(self.x, *tmplist)))/len(self.x)
        self.line2.set_ydata(np.real(self.fourier_amps))
        self.line3.set_ydata(np.imag(self.fourier_amps))
        self.line4.set_ydata(np.abs(self.fourier_amps))

    def set_sliders(self) -> None:
        """
        Create and set sliders.
        """
        rnge = 2.0
        for slider in self.sliderslist:
            slider.destroy()
        self.sliderslist = []
        for i, symbol in enumerate(self.f.parameters):
            self.sliderslist.append(tk.Scale(self.window,
                                             label="change "
                                             + str(symbol) + ":",
                                             from_=-rnge, to=rnge,
                                             resolution=0.01,
                                             orient=tk.HORIZONTAL,
                                             length=200,
                                             command=self.slider_update))
            self.sliderslist[i].grid(row=i + 4, column=3,
                                     padx=(10, 10), pady=(0, 0))
            self.sliderslist[i].set(1.0)

    def update(self, delta_t: float) -> None:
        pass


if __name__ == "__main__":
    run = Main()
    run.animation_loop()
    tk.mainloop()
