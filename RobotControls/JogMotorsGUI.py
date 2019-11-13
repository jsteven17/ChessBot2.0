from tkinter import Tk, Label, Button, StringVar

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Jog Motors")

        self.l1 = Label(master, text="moveTo Value")
        self.l1.grid(row=0, column = 0)

        self.l2 = Label(master, text="Joint Angle")
        self.l2.grid(row=0, column = 3)

        self.bodyPlus = Button(master, text="+", command=self.plus)
        self.bodyPlus.grid(row=1, column=1)
        self.shoulderPlus = Button(master, text="+", command=self.greet)
        self.shoulderPlus.grid(row=2, column=1)
        self.elbowPlus = Button(master, text="+", command=self.greet)
        self.elbowPlus.grid(row=3, column=1)
        self.bodyMinus = Button(master, text="-", command=self.greet)
        self.bodyMinus.grid(row=1, column=2)
        self.shoulderMinus = Button(master, text="-", command=self.greet)
        self.shoulderMinus.grid(row=2, column=2)
        self.elbowMinus = Button(master, text="-", command=self.greet)
        self.elbowMinus.grid(row=3, column=2)

        mb = StringVar()
        mb.set("0")
        ms = StringVar()
        ms.set("0")
        me = StringVar()
        me.set("0")

        self.j0 = 0
        self.j1 = 0
        self.j2 = 0

        db = StringVar()
        db.set("0.0°")
        ds = StringVar()
        ds.set("0.0°")
        de = StringVar()
        de.set("0.0°")

        movBody = Label(master, textvariable=mb)
        movBody.grid(row=1, column = 0)
        movShoulder = Label(master, textvariable=ms)
        movShoulder.grid(row=2, column = 0)
        movElbow = Label(master, textvariable=me)
        movElbow.grid(row=3, column = 0)

        degBody = Label(master, textvariable=db)
        degBody.grid(row=1, column = 3)
        degShoulder = Label(master, textvariable=ds)
        degShoulder.grid(row=2, column = 3)
        degElbow = Label(master, textvariable=de)
        degElbow.grid(row=3, column = 3)

        allButtons = [self.bodyPlus, self.shoulderPlus, self.elbowPlus, self.bodyMinus, self.shoulderMinus, self.elbowMinus]
        for widget in allButtons:
            widget.configure(height=2, width=5)

    def plus0(self):
        self.j0 = self.j0 + 1


root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()