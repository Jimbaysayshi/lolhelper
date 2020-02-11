import tkinter as tk
from tkinter import Tk, Label, Entry, StringVar
import json

REGIONS = ["EUW", "EUNE", "NA"]


class Settings():
    def save(self):

        path = self.directory_text.get()
        region = self.region_text.get()

        settings = {}
        settings['path'] = path
        settings['chromepath'] = path+'\\chromedriver'
        settings['region'] = region
        settings['chrome_args'] = [
            "--ignore-certificate-errors",
            "--disable-popup-blocking",
            "--incognito"]
        settings['op'] = '.op.gg/multi/query='
        settings['uses'] = 1

        with open('settings.json', 'w', encoding='utf-8') as data:
            str_ = json.dumps(settings,
                              indent=4, sort_keys=True,
                              separators=(',', ': '), ensure_ascii=False)
            data.write(str(str_))

    def cancel(self):
        quit(1)

    def __init__(self):

        # root
        self.root = tk.Tk()
        self.root.resizable(width=False, height=False)

        # init frame
        self.frame = tk.Frame(self.root, height=100, width=50)
        self.frame.grid()

        # path
        self.path_text = StringVar()
        self.path_text.set("Path to lolhelper: ")
        self.path_directory = Label(
            self.frame, textvariable=self.path_text, height=4)
        self.path_directory.pack(side="left")

        self.directory_text = StringVar(None)
        self.dirname = Entry(
            self.frame, textvariable=self.directory_text, width=40)
        self.dirname.pack(side="left")

        # region
        self.region_text = StringVar(self.root)
        self.region_text.set(REGIONS[0])
        self.region_drop = tk.OptionMenu(self.root, self.region_text, *REGIONS)
        self.region_drop.grid(row=1, column=0)

        # buttons
        self.save_btn = tk.Button(
            self.root, command=self.save, text='Save')
        self.cancel_btn = tk.Button(
            self.root, command=self.cancel, text='Cancel')

        # Title
        self.root.title('LoLstats')

        self.save_btn.grid(row=3, column=0, sticky="W")
        self.cancel_btn.grid(row=3, column=0, sticky="E")

        # start tkinter loop
        self.root.mainloop()


instance = Settings()
