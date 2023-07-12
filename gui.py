from scientist import *
import os
import tkinter as tk
import math
from tkinter import font as tkFont
from tkinter import filedialog
from PIL import ImageTk, Image

root = tk.Tk()

image_ratio = 1

guess = scientist()

def valid(string):
    for c in string:
        if c != '0' and c != '1':
            return False
    return True

root.title("Scientist")

accepted_frame = tk.Frame(root)
accepted_frame.grid(row=1, column=0, padx=10, pady=10)

accepted_title_label = tk.Label(accepted_frame, text="Accepted Strings")
accepted_title_label.pack()

accepted_scrollbar = tk.Scrollbar(accepted_frame)
accepted_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

accepted_listbox = tk.Listbox(accepted_frame, yscrollcommand=accepted_scrollbar.set)
accepted_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

accepted_scrollbar.config(command=accepted_listbox.yview)

def add_accepted_string(string):
    if string == "":
        accepted_listbox.insert(tk.END, "eps")
    else:
        accepted_listbox.insert(tk.END, string)
   

rejected_frame = tk.Frame(root)
rejected_frame.grid(row=1, column=1, padx=10, pady=10)

rejected_title_label = tk.Label(rejected_frame, text="Rejected Strings")
rejected_title_label.pack()

rejected_scrollbar = tk.Scrollbar(rejected_frame)
rejected_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

rejected_listbox = tk.Listbox(rejected_frame, yscrollcommand=rejected_scrollbar.set)
rejected_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

rejected_scrollbar.config(command=rejected_listbox.yview)

def add_rejected_string(string):
    if string == "":
        rejected_listbox.insert(tk.END, "eps")
    else:
        rejected_listbox.insert(tk.END, string)
        
        
def clear_accepted_text(event):
    current_text = accept_input.get()
    if current_text == accept_text:
        accept_input.delete(0, tk.END)
        
def restore_accepted_text(event):
    current_text = accept_input.get()
    if current_text == "":
        accept_input.insert(0, accept_text)

def accept_string(string):
    guess.add_string(1, string)
    add_accepted_string(string)
    accept_input.delete(0, tk.END)
    update_dfa_image()

def get_accepted_string():
    string = accept_input.get()
    if string == accept_text or guess.known_string(string) or (not valid(string) and string != 'eps'):
        return
    elif string == 'eps':
        accept_string('')
    else:
        accept_string(string)
    
    
accept_input_frame = tk.Frame(root)
accept_input_frame.grid(row=2, column=0, padx=10, pady=10)
  
accept_text = "String to accept"
accept_input = tk.Entry(accept_input_frame)
accept_input.insert(0, accept_text)
accept_input.bind("<FocusIn>", clear_accepted_text)
accept_input.bind("<FocusOut>", restore_accepted_text)
accept_input.grid(row=0, column=0)

accept_button = tk.Button(accept_input_frame, text="Accept string", command=get_accepted_string)
accept_button.grid(row=1, column=0)


def clear_rejected_text(event):
    current_text = reject_input.get()
    if current_text == reject_text:
        reject_input.delete(0, tk.END)
        
def restore_rejected_text(event):
    current_text = reject_input.get()
    if current_text == "":
        reject_input.insert(0, reject_text)
        
def reject_string(string):
    guess.add_string(0, string)
    add_rejected_string(string)
    reject_input.delete(0, tk.END)
    update_dfa_image()
    
def get_rejected_string():
    string = reject_input.get()
    if string == reject_text or guess.known_string(string) or (not valid(string) and string != 'eps'):
        return
    elif string == 'eps':
        reject_string('')
    else:
        reject_string(string)

rejected_input_frame = tk.Frame(root)
rejected_input_frame.grid(row=2, column=1, padx=10, pady=10)

reject_input = tk.Entry(rejected_input_frame)
reject_input.grid(row=0, column=1)

reject_text = "String to reject"
reject_input = tk.Entry(rejected_input_frame)
reject_input.insert(0, reject_text)
reject_input.bind("<FocusIn>", clear_rejected_text)
reject_input.bind("<FocusOut>", restore_rejected_text)
reject_input.grid(row=0, column=1)

reject_button = tk.Button(rejected_input_frame, text="Reject string", command=get_rejected_string)
reject_button.grid(row=1, column=1)

num_processed_dfa_label = tk.Label(root, text="Number of DFAs processed: " + str(guess.count))
num_processed_dfa_label.grid(row=3, column=0, padx=10, pady=10)

num_final_dfa_label = tk.Label(root, text="Number of Conjectures: " + str(guess.count_final))
num_final_dfa_label.grid(row=3, column=1, padx=10, pady=10)


curr_image = 0

image_path = "./current_session/out" + str(guess.count_final-1) + ".png"
image = Image.open(image_path)
image = image.resize((math.floor(image.width*image_ratio), math.floor(image.height*image_ratio)))
tk_image = ImageTk.PhotoImage(image)

image_box = tk.Canvas(root, width=image.width, height=image.height, bg="white")
image_box.grid(row=1, column=2, rowspan=2)
image_box.create_image(0, 0, image=tk_image, anchor="nw")


def update_dfa_image():
    global curr_image
    curr_image = guess.count_final-1
    
    
    image_path = "./current_session/out" + str(guess.count_final-1) + ".png"
    image = Image.open(image_path)
    image = image.resize((math.floor(image.width*image_ratio), math.floor(image.height*image_ratio)))
    tk_image = ImageTk.PhotoImage(image)
    
    global image_box
    image_box.configure(width=image.width, height=image.height)
    image_box.create_image(0, 0, image=tk_image, anchor="nw")
    image_box.image = tk_image
    
    global image_label
    image_label.configure(text=image_path)
    
    global num_processed_dfa_label
    num_processed_dfa_label.configure(text="Number of DFAs processed: " + str(guess.count))
    
    global num_final_dfa_label
    num_final_dfa_label.configure(text="Number of Conjectures: " + str(guess.count_final))
    
    root.update_idletasks()
    root.geometry('{}x{}'.format(root.winfo_reqwidth(), root.winfo_reqheight()))

def next_dfa_image():
    global curr_image
    curr_image += 1
    curr_image = curr_image % guess.count_final
    image_path = "./current_session/out" + str(curr_image) + ".png"
    image = Image.open(image_path)
    image = image.resize((math.floor(image.width*image_ratio), math.floor(image.height*image_ratio)))
    tk_image = ImageTk.PhotoImage(image)
    
    global image_box
    image_box.configure(width=math.floor(image.width), height=math.floor(image.height))
    image_box.create_image(0, 0, image=tk_image, anchor="nw")
    image_box.image = tk_image
    
    global image_label
    image_label.configure(text=image_path)
    
    root.update_idletasks()
    root.geometry('{}x{}'.format(root.winfo_reqwidth(), root.winfo_reqheight()))

def prev_dfa_image():
    global curr_image
    curr_image -= 1
    curr_image = curr_image % guess.count_final
    image_path = "./current_session/out" + str(curr_image) + ".png"
    image = Image.open(image_path)
    image = image.resize((math.floor(image.width*image_ratio), math.floor(image.height*image_ratio)))
    tk_image = ImageTk.PhotoImage(image)
    
    global image_box
    image_box.configure(width=image.width, height=image.height)
    image_box.create_image(0, 0, image=tk_image, anchor="nw")
    image_box.image = tk_image
    
    global image_label
    image_label.configure(text=image_path)

    root.update_idletasks()
    root.geometry('{}x{}'.format(root.winfo_reqwidth(), root.winfo_reqheight()))

image_label = tk.Label(root, text=image_path, bg="white")
image_label.grid(row=3, column=2)


image_button_frame = tk.Frame(root)
image_button_frame.grid(row=4, column=2, padx=10, pady=10)


backwards_button = tk.Button(image_button_frame, text="<", command=prev_dfa_image)
backwards_button.pack(side=tk.LEFT, padx=5)

forward_button = tk.Button(image_button_frame, text=">", command=next_dfa_image)
forward_button.pack(side=tk.LEFT, padx=5) 

def set_font_size():
    size = int(font_size_input.get())
    tkFont.nametofont("TkDefaultFont").configure(size=size)
    tkFont.nametofont("TkTextFont").configure(size=size)
    
    root.update_idletasks()
    root.geometry('{}x{}'.format(root.winfo_reqwidth(), root.winfo_reqheight())) 

font_size_input_frame = tk.Frame(root)
font_size_input_frame.grid(row=0, column=0, padx=10, pady=10)

font_size_input = tk.Entry(font_size_input_frame)
font_size_input.grid(row=0, column=0)
font_size_button = tk.Button(font_size_input_frame, text="Set Font Size", command=set_font_size)
font_size_button.grid(row=0, column=1)

def set_image_size():
    size = float(image_size_input.get())
    global image_ratio
    image_ratio = size
    
    global curr_image
    image_path = "./current_session/out" + str(curr_image) + ".png"
    image = Image.open(image_path)
    image = image.resize((math.floor(image.width*image_ratio), math.floor(image.height*image_ratio)))
    tk_image = ImageTk.PhotoImage(image)
    
    global image_box
    image_box.configure(width=image.width, height=image.height)
    image_box.create_image(0, 0, image=tk_image, anchor="nw")
    image_box.image = tk_image
    
    global image_label
    image_label.configure(text=image_path)
    
    root.update_idletasks()
    root.geometry('{}x{}'.format(root.winfo_reqwidth(), root.winfo_reqheight()))

image_size_input_frame = tk.Frame(root)
image_size_input_frame.grid(row=0, column=1, padx=10, pady=10)

image_size_input = tk.Entry(image_size_input_frame)
image_size_input.grid(row=0, column=0)
image_size_button = tk.Button(image_size_input_frame, text="Set Image Ratio", command=set_image_size)
image_size_button.grid(row=0, column=1)

def reset_dfa():
    global guess
    print("\r" + " " * 64 + "\r", end="")
    guess = scientist()
    accepted_listbox.delete(0, tk.END)
    rejected_listbox.delete(0, tk.END)
    update_dfa_image()

def load_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = filedialog.askopenfilename(initialdir=script_dir)
    
    if file_path:
        with open(file_path, 'r') as file:
            reset_dfa()
            for line in file:
                string = line.split()
                if string[1] == "eps":
                    if int(string[0]):
                        accept_string("")
                    else:
                        reject_string("")
                else:
                    if int(string[0]):
                        accept_string(string[1])
                    else:
                        reject_string(string[1])
            


def export_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    folder_path = filedialog.askdirectory(initialdir=script_dir)
    
    if folder_path:
        for file in os.listdir("./current_session/"):
            file_path = os.path.join("./current_session/", file)
            destination_path = os.path.join(folder_path, file)
            shutil.copy2(file_path, destination_path)
        
options_frame = tk.Frame(root)
options_frame.grid(row=0, column=2, padx=10, pady=10)

load_file_button = tk.Button(options_frame, text="Load file", command=load_file)
load_file_button.grid(row=0, column=0)

save_file_button = tk.Button(options_frame, text="Export", command=export_file)
save_file_button.grid(row=0, column=1)

reset_button = tk.Button(options_frame, text="Reset", command=reset_dfa)
reset_button.grid(row=0, column=2)

root.update_idletasks()
root.geometry('{}x{}'.format(root.winfo_reqwidth(), root.winfo_reqheight()))

root.mainloop()
