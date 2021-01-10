import re
import tkinter
import tkinter.messagebox


def message_box(subject, content):
    """
    message box using tkinter
    :param subject: message box subject
    :param content: message box content
    :return: None
    """
    root = tkinter.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    tkinter.messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def is_valid_ip(s_address):
    """
    check if string is IP v4 address
    :param s_address: address string
    :return: True if string ip is IP v4 address
    """
    match = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", s_address)
    return bool(match) and all(map(lambda n: 0 <= int(n) <= 255, match.groups()))

def is_valid_ip_with_port(s_address):
    """
    check if string is IP v4 address with port number
    :param s_address: address string
    :return: True if string ip is IP v4 address with port number
    """
    match = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\:(\d{1,4})$", s_address)
    groups = match.groups()
    return bool(match) and all(map(lambda n: 0 <= int(n) <= 255, groups[:-1])) and str.isdecimal(groups[-1])


