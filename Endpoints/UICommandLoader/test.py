import tkFileDialog
# examples:
def open_it():
    filename = tkFileDialog.askopenfilename()
    print filename  # test
    
def save_it():
    filename = tkFileDialog.askopenfilename()
    print filename  # test
    
def save_as():
    filename = tkFileDialog.asksaveasfilename()
    print filename  # test
    
open_it()