#!/usr/bin/env python3

import os, shutil
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename

##############################################
def get_interfaces():
    interfaces = os.listdir('/etc/wireguard')
    clean_interfaces = list()
    for i in interfaces:
        clean_interfaces.append(i.split(".")[0])
    return clean_interfaces
def get_selected_interface():
    selected_index = listbox.curselection()
    return listbox.get(selected_index)

root = tk.Tk()
root.geometry('700x400')
root.resizable(False, False)
root.title('Wireguard GUI')
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

##############################################
#def button_add():
#    showinfo(message="Adding")
def button_remove():
    try:
        interface = get_selected_interface()
        command = f'rm -f /etc/wireguard/{interface}.conf'
        print("Command: %s" % (command))
        res = os.system(command)
        if res == 0:
            msg = f'Interface {interface} removed!'
            showinfo(message=msg)

            idx = listbox.get(0, tk.END).index(interface)
            listbox.delete(idx)
        else:
            msg = f'Could not remove interface {interface}...'
            showinfo(message=msg)
    except:
        msg = f'To remove an interface, please select one first.'
        showinfo(message=msg)

def button_import():
    filename = askopenfilename()
    print("You have selected: %s" % filename)
    basename = os.path.basename(filename)
    shutil.copyfile(filename, '/etc/wireguard/' + basename)
    if os.path.exists('/etc/wireguard/' + basename):
        msg = f'Interface {basename} imported'
        showinfo(message=msg)
        listbox.insert('end', basename.split(".")[0])
    else:
        msg = f'Could not import {basename}!'
        showinfo(message=msg)

#add_button = ttk.Button(root, text='Add', command=button_add)
#add_button.grid(column=0,row=0,sticky=tk.W)

remove_button = ttk.Button(root, text='Remove', command=button_remove)
remove_button.grid(column=0,row=0,sticky=tk.E)

import_button = ttk.Button(root, text='Import', command=button_import)
import_button.grid(column=0,row=0)

##############################################

# create a list box
interfaces = get_interfaces()
interfaces_var = tk.StringVar(value=interfaces)
listbox = tk.Listbox(
        root,
        listvariable=interfaces_var,
        height=6,
        selectmode='extended')
listbox.grid(
        column=0,
        row=1,
        sticky='nwes')

##############################################
def button_start():
    try:
        interface = get_selected_interface()
        command = f'systemctl start wg-quick@{interface}.service'
        print("Command: %s" % (command))
        res = os.system(command)
        if res == 0:
            msg = f'Interface {interface} started!'
            showinfo(message=msg)
        else:
            msg = f'Could not start interface {interface}...'
            showinfo(message=msg)
    except:
        msg = f'Please select an interface first'
        showinfo(message=msg)

def button_stop():
    try:
        interface = get_selected_interface()
        command = f'systemctl stop wg-quick@{interface}.service'
        print("Command: %s" % (command))
        res = os.system(command)
        if res == 0:
            msg = f'Interface {interface} stopped'
            showinfo(message=msg)
        else:
            msg = f'Could not stop interface {interface}!'
            showinfo(message=msg)
    except:
        msg = f'Please select an interface first'
        showinfo(message=msg)

def button_save():
    try:
        interface = get_selected_interface()
        iface_data = config_textbox.get('0.0','100000000.0')
        with open('/etc/wireguard/' + interface + '.conf', 'w') as f:
            lines = f.write(iface_data)
            msg = f'Lines written: {lines}'
            showinfo(message=msg)
    except:
        msg = f'Please select an interface first'
        showinfo(message=msg)

start_button = ttk.Button(root, text='Start', command=button_start)
start_button.grid(column=0,row=2,sticky=tk.W)

stop_button = ttk.Button(root, text='Stop', command=button_stop)
stop_button.grid(column=0,row=2,sticky=tk.E)

save_button = ttk.Button(root, text='Save', command=button_save)
save_button.grid(column=0,row=2)
##############################################
config_label = ttk.Label(root, text="Configuration")
config_label.grid(column=1, row=0, padx=5, pady=5)
config_textbox = tk.Text(root,height=15,width=40)
config_textbox.grid(column=1, row=1, padx=5, pady=5)
##############################################

def items_selected(event):
    ## Get interface name
    #selected_indices = listbox.curselection()
    ##selected_interfaces = ",".join([listbox.get(i) for i in selected_indices])

    selected_interface = get_selected_interface()
    
    ## Load file
    print("Loading config for: %s" % (selected_interface))
    file_data = ""
    with open('/etc/wireguard/' + selected_interface + '.conf', 'r') as f:
        file_data = f.read()
    config_textbox.delete('0.0', '10000000.0')
    config_textbox.insert('0.0', file_data)

listbox.bind('<<ListboxSelect>>', items_selected)
##############################################

root.mainloop()
