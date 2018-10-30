from tkinter import *
from tkinter import ttk
from pubsub import pub
import renewal as ren
import autori as ri
import threading
from datetime import datetime

class Application(Frame):
    def __init__(self, master=None):
        pub.subscribe(self.process_message, 'message')
        super().__init__(master)
        self.grid(row=0, column=0, sticky=N + E + S + W)
        self['bg'] = 'black'
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0,weight=1)
        self.create_widget()


    def create_widget(self):

        style = ttk.Style(self)
        style.configure("C.TButton", background="white", font=("Fixedsys", 10, 'bold'), foreground='black')

        fr_functionality = Frame(self, bg='black')
        self.place_in_grid(fr_functionality,uniform="nj")

        fr_status = Frame(self,bg='black')
        self.place_in_grid(fr_functionality,row=10,uniform="nj")

        self.create_functionality(fr_functionality)
        self.create_status_widget(fr_functionality)
    
    def create_functionality(self,fr):
        self.btn_renewal = ttk.Button(fr,text="Renewal",style="C.TButton")
        self.place_in_grid(widget=self.btn_renewal,row=0,column=0,uniform="james",columnspan=4,width=15,padding={'padx':(2,2),'pady':(2,2),'i_padx':2,'i_pady':2})

        self.btn_auto_ri = ttk.Button(fr,text="Auto RI",style="C.TButton")
        self.place_in_grid(widget=self.btn_auto_ri,row=0,column=5,uniform="james",columnspan=4,width=15,padding={'padx':(2,2),'pady':(2,2),'i_padx':2,'i_pady':2})
        
        self.btn_renewal.bind('<Button>',self.process_renewal)
        self.btn_auto_ri.bind('<Button>',self.process_auto_ri)

    def create_status_widget(self,fr):
        self.text_status_log = Text(fr,bg='white',exportselection=1,height=10,width=10)
        self.place_in_grid(widget=self.text_status_log,row=5,column=0,columnspan=5000)

        scrollbar = Scrollbar(self.text_status_log,command=self.text_status_log.yview)

        self.text_status_log['yscrollcommand']= scrollbar.set

        self.text_status_log.tag_config("e", background="white", foreground="red")
        self.text_status_log.tag_config("s", background="white", foreground="green")
        self.text_status_log.tag_config("i", background="white", foreground="blue")
        self.text_status_log.tag_config("u", background="white", foreground="green", underline=1)
    
    def process_message(self,message1,message=None):
        print (message1)
        if message1['type'] == 'err':
            tag = "e"
        elif message1['type'] == 'info':
            tag = "i"
        elif message1['type'] == 'succ':
            tag = "s"
        msg = message1['msg']
        self.text_status_log.insert(END, f" {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {msg} \n", tag)
        self.text_status_log.see("end")
    
    
    def process_renewal(self,e):
        pub.sendMessage('message',message1={'type':'info','msg':f'Renewal - Processing Renewal'})
        #pub.sendMessage('message',message1="Hello")
        threading.Thread(target=ren.process_renewal).start() 

    def process_auto_ri(self,e):
        threading.Thread(target=ri.process_auto_ri).start() 

    def place_in_grid(self,widget,row=0,column=0,uniform=None,columnspan=None,sticky='ST',width=None,padding=None):    
        if sticky=='ST':
            stretch = N + E + W + S
        elif sticky=='LJ':
            stretch = W
        elif sticky == 'RJ':
            stretch = E

        i_padx = None
        i_pady = None
        padx = None
        pady = None
        if padding is not None:
            i_padx = padding['i_padx']
            i_pady = padding['i_pady']
            padx = padding['padx']
            pady = padding['pady']

        if columnspan is not None:
            widget.grid(row=row, column=column, sticky=stretch,columnspan=columnspan,padx=padx,pady=pady,ipadx=i_padx, ipady=i_pady)
        else:
            widget.grid(row=row, column=column, sticky=N + E + W + S,padx=padx,pady=pady,ipadx=i_padx, ipady=i_pady)
        
        widget.rowconfigure(row, weight=1)
        widget.columnconfigure(column, weight=1,uniform=uniform)

        if width is not None:
            widget.config(width=width)

root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.title("TRANSFORMED XML GENERATOR")
app = Application(master=root)
app.mainloop()
