import tkinter
import tkinter.messagebox


def message_box(subject, content):
    root = tkinter.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    tkinter.messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
