from tkinter.ttk import *
import tkinter as tk
from idlelib.tooltip import OnHoverTooltipBase



class ToolTip(OnHoverTooltipBase):
    def __init__(self,parent,content,image=None,hover_delay=1000,**kwargs):
        super().__init__(parent,hover_delay=hover_delay)
        self.content=content
        self.image=image
        self.style={
            "bg":"#FFFE00",
            "fg":"black",
            "bd":2,
            "relief":tk.RAISED,
            "padx":4,
            "pady":2,
            "justify":"left"
        }
        self.style.update(kwargs)
    def showcontents(self):
        content = self.get_content()
        
        frame = tk.Frame(self.tipwindow, 
                         bg=self.style["bg"],
                         bd=self.style["bd"],
                         relief=self.style["relief"])
        frame.pack()
        
        label = tk.Label(frame, 
                         text=content,
                         bg=self.style["bg"],
                         fg=self.style["fg"],
                         padx=self.style["padx"],
                         pady=self.style["pady"],
                         font=self.style["font"],
                         justify=self.style["justify"])
        label.pack()
    
    def get_content(self):
       
        if callable(self.content):
            return self.content()
        return self.content if hasattr(self, 'content_func') else ""

