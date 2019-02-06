import socket
import tkinter
from threading import Thread


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = sock.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = client_msg.get()
    client_msg.set("")  # Clears input field.
    sock.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        sock.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    client_msg.set("{quit}")
    send()


top = tkinter.Tk()
top.title("Chatter")

msg_frame = tkinter.Frame(top)
client_msg = tkinter.StringVar()
client_msg.set("Now type your name and press enter!")
scrollbar = tkinter.Scrollbar(msg_frame)

msg_list = tkinter.Listbox(msg_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
msg_frame.pack()

entry_field = tkinter.Entry(top, textvariable=client_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

# ----Now comes the sockets part----
BUFSIZ = 1024
HOST, PORT = "localhost", 57695

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
