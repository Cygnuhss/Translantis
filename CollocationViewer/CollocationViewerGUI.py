import os

import matplotlib

matplotlib.use("TkAgg")

from matplotlib import style

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from drawCollocations import drawCollocations

LARGE_FONT = ("Verdana", 12)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

style.use("ggplot")

APPLICATION_TITLE = "Collocation Viewer"

FAVICON_PATH = "../img/favicon.ico" if os.name == "nt" else "@../img/favicon.xbm"
LOGO_PATH = "../img/logo.png"


class CollocationViewerGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #tk.Tk.iconbitmap(self, FAVICON_PATH)
        tk.Tk.wm_title(self, APPLICATION_TITLE)

        container = tk.Frame(self)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk. Menu(container)
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Save", command=lambda: save(self), accelerator="Ctrl+S")
        fileMenu.add_command(label="Save as...", command=lambda: save_as(self), accelerator="Ctrl+Shift+S")
        # fileMenu.add_command(label="Export animation as Bvh", command=lambda: showPopupMessage("Not supported yet", accelerator="Ctrl+E"))
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=quit, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=fileMenu)

        helpMenu = tk.Menu(menubar, tearoff=0)
        helpMenu.add_command(label="Help", command=lambda: showPopupMessage(
            "Use the Generators menu to select a predefined motion generator.\nThe Generate Animation button creates and shows an animation. Use File > Save to store the results as a motion capture file."))
        menubar.add_cascade(label="Help", menu=helpMenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for frameType in (StartPage, PlotPage):
            frame = frameType(container, self)
            self.frames[frameType] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Welcome to Collocation Viewer", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Next", command=lambda: controller.show_frame(PlotPage))
        button1.pack()


class PlotPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Plot Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        #drawCollocations(collocationRelations, wordCounts)


# Source: https://stackoverflow.com/questions/22848080/python-create-save-button-that-saves-an-edited-version-to-the-same-filenot-save
def save(self):
    global currentAnimation
    if currentAnimation:
        skeleton, motionChannels, motion = currentAnimation
        try:
            pass#writeBvh(self.file, skeleton, motionChannels, motion)
        except AttributeError:
            save_as(self)
    else:
        try:
            with open(self.file, "w") as outputFile:
                outputFile.write("")
        except AttributeError:
            save_as(self)


def save_as(self):
    self.file = filedialog.asksaveasfilename(
        defaultextension=".bvh",
        filetypes=[("BVH File", "*.bvh")])
    global currentAnimation
    if currentAnimation:
        skeleton, motionChannels, motion = currentAnimation
        #writeBvh(self.file, skeleton, motionChannels, motion)
    else:
        with open(self.file, "w") as outputFile:
            outputFile.write("")


def showPopupMessage(message):
    popup = tk.Tk()
    popup.iconbitmap(FAVICON_PATH)
    popup.wm_title("!")
    label = ttk.Label(popup, text=message, font=NORMAL_FONT)
    label.pack(side=tk.TOP, fill="x", pady=10)
    button1 = ttk.Button(popup, text="Ok", command=popup.destroy)
    button1.pack()
    popup.mainloop()