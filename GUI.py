from tkinter import Frame, N, S, E, W, Label, DoubleVar, Entry, Button
from tkthread import tk, TkThread
from tkinter.constants import *
from PIL import Image
from PIL import ImageTk
import tkinter.font as tkFont
import time
import threading
class Gui(tk.Frame):
    def __init__(self, camera):
        master = tk.Tk()
        #tkt = TkThread(master)
        master.wm_title('OPEN CV')
        self.exitFlag = FALSE

        # Initialize values
        self.w1 = 1000
        self.h1 = 600
        self.PanelAscale = 0.9
        tk.Frame.__init__(self, master)
        self.frame = tk.Frame(master)
        self.master = master
        self.Camera = camera
        # Configure
        master.geometry("1000x600")
        self._create_widgets()
        self.bind('<Configure>', self._resize)
        self.winfo_toplevel().minsize(200, 200)
        self.grid_propagate(False)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()
        #self.master.mainloop()

    def on_closing(self):
        try:
            self.master.destroy()
            print("closed")
            self.exitFlag = TRUE
            self.Camera.destoroy()
        except:
            print("Error!!!")

    def loop(self):
        while not self.exitFlag:
            try:
                time.sleep(0.06)
                img = self.Camera.getImg()
                self.updatePanelAImage(img)
                self.master.update()
                print("loop")
            except:
                print("Error!!!")

    def _create_widgets(self):
        try:
            # Configure grid
            self.content = tk.Frame(self)
            self.grid(sticky=N + S + E + W)
            self.master.rowconfigure(0, weight=1)
            self.master.rowconfigure(1, weight=1)
            self.master.columnconfigure(0, weight=1)
            self.master.columnconfigure(1, weight=1)
            # Create controls
            self.fontStyle = tkFont.Font(family="Lucida Grande", size=int(self.h1 / 25))
            Label = tk.Label(self.master, text='°F', font=self.fontStyle).grid(row=0, column=0, sticky=("nw"))
            self.Label = Label
            self.addPanelA()
        except:
            print("Error!!!")

    def addPanelA(self):
        self.panelA = tk.Label(self.master, text='xxxxxx')
        self.panelA.grid(row=1, column=0, sticky=("nw"))

    def updatePanelAImage(self, imageRGB):
        try:
            image = Image.fromarray(imageRGB)
            image = image.resize((int(self.w1 * self.PanelAscale), int(self.h1 * self.PanelAscale)), Image.ANTIALIAS)
            imageTk = ImageTk.PhotoImage(image)
            self.panelA.configure(image=imageTk)
            self.panelA.image = imageTk
        except:
            print("Error!!!")

    def _resize(self, event):
        try:
            self.width = event.width
            self.height = event.height
            '''Modify padding when window is resized.'''
            self.w, self.h = event.width, event.height
            self.w1, self.h1 = self.master.winfo_width(), self.master.winfo_height()
            print(self.w, self.h)
            print(self.w1, self.h1)  # should be equal
            self.resizePanelA()
            self.resizeLabel()
        except:
            print("Error!!!")

    def resizeLabel(self):
        try:
            fontsize = self.fontStyle['size']
            self.fontStyle.configure(size=int(self.h1 / 25))
        except:
            print("Error!!!")

    def resizePanelA(self):
        try:
            self.panelA.configure(width=int(self.w1 * self.PanelAscale), height=int(self.h1 * self.PanelAscale))
            self.resizeImageInPanel()
        except:
            print("Error!!!")

    def resizeImageInPanel(self):
        try:
            img = self.panelA.image
            img = ImageTk.getimage(img)
            image = img.resize((int(self.w1 * self.PanelAscale), int(self.h1 * self.PanelAscale)), Image.ANTIALIAS)
            imageTk = ImageTk.PhotoImage(image)
            self.panelA.configure(image=imageTk)
            self.panelA.image = imageTk
        except:
            print("Error!!!")

