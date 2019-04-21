import tkinter as tk
import os

import LoginFrame as lf

import cryptor as cr
import database as db

FONT = ("DejaVu Sans Mono Bold", 12)
SFONT = (FONT[0], FONT[1] - 2)

class CreatePpdbFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        lblPpdb = tk.Label(self, text="Location:", font=FONT,
                           anchor=tk.W)
        lblPpdb.grid(row=0, column=0, sticky=tk.W)

        self.ppdbPath = tk.StringVar()
        self.ppdbPath.set(os.getcwd())
        self.entPpdb = tk.Entry(self, textvariable=self.ppdbPath,
                                font=FONT, width=30)
        self.entPpdb.grid(row=1, column=0, columnspan=3,
                          sticky=tk.W+tk.E+tk.S+tk.N)

        self.btnPpdb = tk.Button(self, text="...", font=FONT,
                                 command=self.btnPpdbClicked,
                                 anchor=tk.E)
        self.btnPpdb.grid(row=1, column=3, sticky=tk.E)

        lblPass = tk.Label(self, text="Password:", font=FONT,
                           anchor=tk.W)
        lblPass.grid(row=2, column=0, sticky=tk.W)

        self.userPass1 = tk.StringVar()
        self.entPass1 = tk.Entry(self, font=FONT, show='*',
                                 textvariable=self.userPass1)
        self.entPass1.grid(row=3, column=0, columnspan=4,
                           sticky=tk.W+tk.E+tk.S+tk.N)

        lblPass = tk.Label(self, text="Repeat password:", font=FONT,
                           anchor=tk.W)
        lblPass.grid(row=4, column=0, sticky=tk.W+tk.E)

        self.userPass2 = tk.StringVar()
        self.entPass2 = tk.Entry(self, font=FONT, show='*',
                                 textvariable=self.userPass2, width=3)
        self.entPass2.bind("<Return>", self.btnCreateClicked)
        self.entPass2.grid(row=5, column=0, columnspan=4, sticky=tk.W+tk.E+tk.S+tk.N)
        
        lblSec = tk.Label(self, text="Security mode:", font=FONT, 
                          anchor=tk.W)
        lblSec.grid(row=6, column=0, sticky=tk.W+tk.E)

        self.secMode = tk.IntVar()
        self.sclSec = tk.Scale(self, font=FONT, orient=tk.HORIZONTAL,
                               showvalue=0,
                               variable=self.secMode, to=2,
                               command=self.changeSecMode)
        self.sclSec.grid(row=7, column=0, columnspan=4, sticky=tk.W+tk.E+tk.S+tk.N)

        self.secModeStr = tk.StringVar()
        self.lblSecMode = tk.Label(self, font=FONT, textvariable=self.secModeStr,
                                   anchor=tk.W)
        self.lblSecMode.grid(row=8, column=0, columnspan=4,
                             sticky=tk.W)

        self.secModeDescr = tk.StringVar()
        lblSecModeDescr = tk.Label(self, font=SFONT, textvariable=self.secModeDescr,
                                   anchor=tk.W, justify=tk.LEFT)
        lblSecModeDescr.grid(row=9, column=0, columnspan=4,
                             sticky=tk.W)

        self.benchResult = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.benchResult[0].set("...")
        self.benchResult[1].set("...")
        self.benchResult[2].set("...")

        self.benchTxt = tk.StringVar()
        self.benchTxt.set("Run benchmark to see how long decryption\nwill take on your device in each security mode.")

        lblBench = tk.Label(self, font=SFONT, textvariable=self.benchTxt,
                            anchor=tk.W, justify=tk.LEFT, bd=4, relief="groove")
        lblBench.grid(row=10, column=0, columnspan=4, sticky=tk.W+tk.E)

        self.btnCancel = tk.Button(self, text="Cancel", font=FONT,
                              command=self.closeWindow,
                              anchor=tk.W)
        self.btnCancel.grid(row=11, column=0, sticky=tk.W)

        self.btnBench = tk.Button(self, text="Benchmark", font=FONT,
                             command=self.benchmark,
                             anchor=tk.E)
        self.btnBench.grid(row=11, column=2, sticky=tk.E)

        self.btnCreate = tk.Button(self, text="Create", font=FONT,
                              command=self.btnCreateClicked,
                              anchor=tk.E)
        self.btnCreate.grid(row=11, column=3, sticky=tk.E)


        self.changeSecMode("0")

        self.pack(padx=10, pady=10, anchor=tk.CENTER, expand=True)
        self.master.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.master.title("Creating Database - pyptopad")
        # THE END OF __INIT__

    def btnPpdbClicked(self):
        file = tk.filedialog.asksaveasfilename(filetypes=(("pyptopad dbs",
                                "*.ppdb"), ("all files", "*.*")))
        if file:
            self.ppdbPath.set(file)

    def btnCreateClicked(self, *args):
        if self.userPass1.get() != self.userPass2.get():
            tk.messagebox.showerror("", "Passwords don't match.")
            return
        c = cr.Cryptor()
        self.changeState("disabled")
        try:
            c.create(self.ppdbPath.get(), self.userPass1.get(), self.secMode.get())
        except Exception:
            tk.messagebox.showerror("", "Wrong file path.")
            self.changeState("normal")
            return
        d = db.Database()
        c.write(d.to_xml_string())
        c.close()
        self.closeWindow()

    def changeSecMode(self, mode):
        if mode == '0':
            self.lblSecMode["fg"] = "green"
            self.secModeStr.set("Nothing to Hide")
            self.secModeDescr.set("I put perfomance above security.\nIn this mode decryption will be quickest,\nbut you better use a strong password.")
        elif mode == '1':
            self.lblSecMode["fg"] = "dark goldenrod"
            self.secModeStr.set("Standard")
            self.secModeDescr.set("Decrypion will take a little bit longer in this mode,\nwhich makes brute-force attacks harder.")
        elif mode == '2':
            self.lblSecMode["fg"] = "red"
            self.secModeStr.set("Paranoia")
            self.secModeDescr.set("Just because you're paranoid,\ndoesn't mean they're not watching you.")

    def refreshBench(self):
        self.benchTxt.set("On this device decryption is going to take:\n" +
                          self.benchResult[0].get() + "s with Nothing to Hide Security Mode\n" +
                          self.benchResult[1].get() + "s with Standard Security Mode\n" +
                          self.benchResult[2].get() + "s with Paranoia Security Mode")

    def changeState(self, state):
        self.entPpdb["state"] = state
        self.btnPpdb["state"] = state
        self.entPass1["state"] = state
        self.entPass2["state"] = state
        self.btnCancel["state"] = state
        self.btnBench["state"] = state
        self.btnCreate["state"] = state
        self.sclSec["state"] = state
        self.master.update_idletasks()

    def benchmark(self, *args):
        self.refreshBench()
        self.changeState("disabled")
        self.benchResult[0].set(str(round(cr.benchmark(0), 2)))
        self.refreshBench()
        self.master.update_idletasks()
        self.benchResult[1].set(str(round(cr.benchmark(1), 2)))
        self.refreshBench()
        self.master.update_idletasks()
        self.benchResult[2].set(str(round(cr.benchmark(2), 2)))
        self.refreshBench()
        self.changeState("normal")

    def closeWindow(self):
        self.master.setFrame(lf.LoginFrame(self.master))