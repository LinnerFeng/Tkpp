import tkinter as tk
from ToolTip import ToolTips

class DraggableWindow(tk.Tk):
    def __init__(self,x,y,title,maxsize=False,icon=None):
        super().__init__()

        self.title_=title#redgist into global

        self.maxsize=maxsize
        self.icon=icon

        self.overrideredirect(1)
        
        self.geometry(f"{x}x{y}")

        self.update_idletasks()
        self.resize_control()
        self.main_frame()
        self.title_bar()
        self.bind_events()
        

        self.bind("<ButtonPress-1>", self.start_dragging)
        self.bind("<ButtonRelease-1>", self.stop_dragging)
        self.bind("<B1-Motion>", self.do_dragging)
        self.bind("<Configure>",self.on_resize)

        self.x = 0
        self.y = 0
        self.width=self.winfo_width()
        self.height=self.winfo_height()

        self.resize=False
        self.resize_direction=None
        


    def start_dragging(self, event):
        self.x = event.x
        self.y = event.y

    def stop_dragging(self, event):
        self.x = 0
        self.y = 0

    def do_dragging(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        new_x = self.winfo_x() + deltax
        new_y = self.winfo_y() + deltay
        self.geometry(f"+{new_x}+{new_y}")
        print("[INFO]Window drag")

    def bind_events(self):
        
        self.title_bar_.bind("<ButtonPress-1>", self.start_dragging)
        self.title_bar_.bind("<B1-Motion>", self.do_dragging)
        self.title_bar_.bind("<ButtonRelease-1>", self.stop_dragging)
        
        

    def resize_control(self):
        self.resize_corner = tk.Frame(self, width=15,bg="#797979", height=15, cursor="sizing")
        self.resize_corner.place(relx=1.0, rely=1.0, anchor="se")
        self.resize_corner.bind("<ButtonPress-1>", lambda e: self.resize_start("corner"))
        self.resize_corner.bind("<B1-Motion>", self.do_resize)
        self.resize_corner.bind("<ButtonRelease-1>", self.resize_stop)
        
        
        self.resize_right = tk.Frame(self, width=5,bg="#797979", cursor="right_side")
        self.resize_right.place(relx=1.0, rely=0.5, anchor="e", relheight=0.8)
        self.resize_right.bind("<ButtonPress-1>", lambda e: self.resize_start("right"))
        self.resize_right.bind("<B1-Motion>", self.do_resize)
        self.resize_right.bind("<ButtonRelease-1>", self.resize_stop)
        
    
        self.resize_bottom = tk.Frame(self, height=5, bg="#797979", cursor="bottom_side")
        self.resize_bottom.place(relx=0.5, rely=1.0, anchor="s", relwidth=0.8)
        self.resize_bottom.bind("<ButtonPress-1>", lambda e: self.resize_start("bottom"))
        self.resize_bottom.bind("<B1-Motion>", self.do_resize)
        self.resize_bottom.bind("<ButtonRelease-1>", self.resize_stop)
        
    def resize_start(self,direction):
        self.resize=True
        self.resize_direction=direction
        self.resize_start_x=self.winfo_pointerx()
        self.resize_start_y=self.winfo_pointery()
        self.resize_start_width=self.winfo_width()
        self.resize_start_height=self.winfo_height()

    def resize_stop(self,event):
        self.resize=False
        self.resize_direction=None

    def do_resize(self,event):
        if not self.resize:
            return
        self.current_x=self.winfo_pointerx()
        self.current_y=self.winfo_pointery()

        self.delta_x=self.current_x-self.resize_start_x
        self.delta_y=self.current_y-self.resize_start_y

        self.new_width=self.resize_start_width
        self.new_height=self.resize_start_height

        if self.resize_direction=="right" or self.resize_direction=="corner":
            self.new_width=max(200,self.resize_start_width+self.delta_x)
        
        if self.resize_direction=="bottom" or self.resize_direction=="corner":
            self.new_height=max(200,self.resize_start_height+self.delta_y)

        self.geometry(f"{self.new_width}x{self.new_height}")

    def on_resize(self,event):
        if event.widget == self:
            # 更新尺寸变量
            self.width = self.winfo_width()
            self.height = self.winfo_height()
            
            # 更新标题栏位置
            self.title_bar_.place(x=0, y=0, relwidth=1, height=30)
            
            # 更新内容区域位置
            self.content.place(x=0, y=30, relwidth=1, relheight=1, height=30)
            
            # 确保控件已创建后再更新位置
            if hasattr(self, 'resize_corner') and self.resize_corner.winfo_exists():
                self.resize_corner.place(relx=1.0, rely=1.0, anchor="se")
            
            if hasattr(self, 'resize_right') and self.resize_right.winfo_exists():
                self.resize_right.place(relx=1.0, rely=0.5, anchor="e", relheight=0.8)
            
            if hasattr(self, 'resize_bottom') and self.resize_bottom.winfo_exists():
                self.resize_bottom.place(relx=0.5, rely=1.0, anchor="s", relwidth=0.8)
            
            # 更新按钮容器位置
            self.button_frame.place(relx=1.0, y=0, anchor="ne")


    def main_frame(self):
        self.main=tk.Frame(self)
        self.main.pack(fill=tk.BOTH,expand=True)

    def title_bar(self):
        self.title_bar_=tk.Frame(self.main,bg="#2c3e50",bd=1,relief=tk.RAISED)
        self.title_bar_.place(x=0,y=0,relwidth=1,width=1)

        self.label=tk.Label(self.title_bar_,text=self.title_,bg="#2c3e50",\
                            fg="#ffffff",font="Consolas")
        self.label.place(x=10,y=5)

        self.button_frame=tk.Frame(self.title_bar_,bg="#2c3e50")
        self.button_frame.place(relx=1.0,y=0,anchor="ne")

        self.min_btn=tk.Button(self.button_frame,text="\u005f",relief="flat",fg="white",\
                               bg="#2c3e50",font=("Arial",10))
        self.min_btn.pack(side=tk.LEFT)
        self.max_btn=tk.Button(self.button_frame,text="\u25a1",relief="flat",fg="white",\
                               bg="#2c3e50",font=("Arial",10),command=self.max_size)
        self.max_btn.pack(side=tk.LEFT)
        self.close_btn=tk.Button(self.button_frame,text="\u00d7",relief="flat",fg="white",\
                               bg="#2c3e50",font=("Arial",10),command=self.close)
        self.close_btn.pack(side=tk.RIGHT)


        self.tooltip_min=ToolTips(self.min_btn,"最小化")
        self.tooltip_max=ToolTips(self.max_btn,"最大化")
        self.tooltip_close=ToolTips(self.close_btn,"关闭")

        self.content = tk.Frame(self.main, bg="#ecf0f1")
        self.content.place(x=0, y=30, relwidth=1, relheight=1, height=-30)
    
    def close(self):
        self.destroy()

    def button_exchange(self,widget,bg):
        self.widget=widget
        self.bg=bg

        self.widget.config(bg=self.bg)
    
    def max_size(self):
        self.state("zoomed")
        self.max_btn.config(text="\u2750")
        self.max_btn.config(command=self.normal_size)

    def normal_size(self):
        self.state("normal")
        self.max_btn.config(text="\u25a1")
        self.max_btn.config(command=self.max_size)



if __name__ == "__main__":
    app = DraggableWindow(600,600,"TEST")
    app.mainloop()
