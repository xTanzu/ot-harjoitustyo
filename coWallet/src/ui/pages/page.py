import tkinter

class Page(tkinter.Frame):

    def __init__(self, *args, **kwargs):
        self.name, parent, self.controller = (kwargs.pop(x) for x in ("name", "parent", "controller"))
        super().__init__(parent, *args, **kwargs)

    def show(self, **kwargs):
        self.lift()