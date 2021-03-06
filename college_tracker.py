'''
Main module for the application.

Run this module to run the application

python college_tracker.py
'''

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

__version__ = '0.1'

from tkinter import *
from ttkthemes import ThemedTk
from db import Database
from os import getenv, getcwd
from settings import PropsLoader
from tkinter import messagebox, filedialog, ttk

# Import setting
theme = PropsLoader()['theme']
icon_path = PropsLoader()['icon_path']
db_path = PropsLoader()['data_store']+'\\'+PropsLoader()['data_file']

db = Database(db_path)

# Create window object
app = ThemedTk(theme=theme)
app.title('College Tracker')
app.geometry('600x550')
app.iconbitmap(icon_path)

def throw_msg_and_clear(msg):
    messagebox.showerror("Invalid Entry", msg)
    clear_item()

def validate_data(col:str, value):
    if col.lower() == 'year':
        if not (int(value) >=1900 and int(value) <=2099):
            throw_msg_and_clear("Year out of range (1900, 2099)")
            return False
    elif col.lower() == 'term':
        if not int(value) in [1,2,3,4]:
            throw_msg_and_clear("Excepted values : 1, 2, 3, 4")
            return False
    return True

def populate_list():
    students_list.delete(*students_list.get_children())
    for i, row in enumerate(db.get_student()):
        tag ='even' if i % 2 == 0 else 'odd'
        students_list.insert(parent='', index='end', iid=row[0], values=tuple(row), tags = (tag,))

def add_item():
    cols = [
            ('year', year_entry.get()),
            ('term', term_entry.get()),
            ('program', program_entry.get()),
            ('tot_enroll_planned', tot_enroll_planned_entry.get()),
            ('plan_students', plan_students_entry.get()),
            ('pattern', pattern_entry.get()),
            ]
    if (year_entry.get() == '' or 
        term_entry.get() == '' or 
        program_entry.get() == '' or 
        tot_enroll_planned_entry.get() == '' or 
        plan_students_entry.get() == '' or 
        pattern_entry.get() == "") :
        messagebox.showerror("Required Fields", "Please enter all fields")
        return
    else:
        for col in cols:
            if not validate_data(col[0], col[1]):
                return

    db.insert_student(
        year_entry.get(), 
        term_entry.get(),
        program_entry.get(),
        tot_enroll_planned_entry.get(),
        plan_students_entry.get(),
        pattern_entry.get()
        )
    populate_list()

def select_item(event):
    global selected_item 
    selected = students_list.focus()
    selected_item = students_list.item(selected, 'values')

    year_entry.delete(0, END)
    year_entry.insert(END, selected_item[1])

    term_entry.delete(0, END)
    term_entry.insert(END, selected_item[2])

    program_entry.delete(0, END)
    program_entry.insert(END, selected_item[3])

    tot_enroll_planned_entry.delete(0, END)
    tot_enroll_planned_entry.insert(END, selected_item[4])

    plan_students_entry.delete(0, END)
    plan_students_entry.insert(END, selected_item[5])

    pattern_entry.delete(0, END)
    pattern_entry.insert(END, selected_item[6])

def clear_item():
    all_items = [
            year_entry, 
            term_entry, 
            program_entry,
            tot_enroll_planned_entry,
            plan_students_entry ,
            pattern_entry
            ]
    for entry in all_items:
        entry.delete(0,END)

def update_item():
    db.modify_sudent(
                    year_entry.get(), 
                    term_entry.get(), 
                    program_entry.get(), 
                    tot_enroll_planned_entry.get(),
                    plan_students_entry.get(), 
                    pattern_entry.get(),
                    selected_item[0]
                    )
    populate_list()

def remove_item():
    db.remove_student(selected_item[0])
    populate_list()

def export_data():
    file_selected = filedialog.asksaveasfilename(
                            defaultextension=".espace", 
                            filetypes=(
                                    ("Excel file", "*.xlsx"),
                                    ("All Files", "*.*") 
                                    )
                                    )
    db.export_data(file_selected)

# fields
# year
year_label = ttk.Label(app, text='Year')
year_label.grid(sticky=W, row=0, column=0, pady=10, padx=25)
year_entry = ttk.Entry(app, textvariable=IntVar())
year_entry.grid(sticky=W, row=0, column=1)
# term
term_label = ttk.Label(app, text='Term')
term_label.grid(sticky=W, row=1, column=0, pady=10, padx=25)
# term_entry = OptionMenu(app, StringVar(), "1","2","3","4")
term_entry = ttk.Entry(app, textvariable=StringVar())
term_entry.grid(sticky=W, row=1, column=1)
# program
program_label = ttk.Label(app, text='Program')
program_label.grid(sticky=W, row=2, column=0, pady=10, padx=25)
program_entry = ttk.Entry(app, textvariable=StringVar())
program_entry.grid(sticky=W, row=2, column=1)
# tepl
tot_enroll_planned_label = ttk.Label(app, text='Total Enrollment Planned')
tot_enroll_planned_label.grid(sticky=W, row=3, column=0, pady=10, padx=25)
tot_enroll_planned_entry = ttk.Entry(app, textvariable=StringVar())
tot_enroll_planned_entry.grid(sticky=W, row=3, column=1)
# plan_std
plan_students_label = ttk.Label(app, text='Planned Students')
plan_students_label.grid(sticky=W, row=4, column=0, pady=10, padx=25)
plan_students_entry = ttk.Entry(app, textvariable=StringVar())
plan_students_entry.grid(sticky=W, row=4, column=1)
# pattern
pattern_label = ttk.Label(app, text='Pattern')
pattern_label.grid(sticky=W, row=5, column=0, pady=10, padx=25)
pattern_entry = ttk.Entry(app, textvariable=StringVar())
pattern_entry.grid(sticky=W, row=5, column=1)

# Buttons
# Add
add_button = ttk.Button(app,
                    text='Add', 
                    width=8,
                    command=add_item)
add_button.grid(row=0, column=2)
# Remove
remove_button = ttk.Button(app,
                    text='Remove', 
                    width=8,
                    command=remove_item)
remove_button.grid(row=1, column=2)
# Modify
update_button = ttk.Button(app,
                    text='Update', 
                    width=8,
                    command=update_item)
update_button.grid(row=2, column=2)
# Clear entry
clear_button = ttk.Button(app,
                    text='Clear', 
                    width=8,
                    command=clear_item)
clear_button.grid(row=3, column=2)

export_data_button = ttk.Button(app,
                    text='Generate', 
                    width=8,
                    command=export_data)
export_data_button.grid(row=4, column=2)

students_list = ttk.Treeview(app)
# Define columns
students_list['columns']=('ID', 'Year', 'Term', 'Program', 'Total Enrollment Planned', 'Planned Students', 'Pattern')
students_list.column("#0", width=0, stretch=NO)
students_list.column("ID", width=40, minwidth=10, anchor=W)
students_list.column("Year", width=50, minwidth=10, anchor=W)
students_list.column("Term", width=50, minwidth=10, anchor=W)
students_list.column("Program", width=100, minwidth=25, anchor=W)
students_list.column("Total Enrollment Planned", width=145, minwidth=10, anchor=W)
students_list.column("Planned Students", width=100, minwidth=10, anchor=W)
students_list.column("Pattern", width=50, minwidth=10, anchor=W)
# Define heading 
students_list.heading("#0", text="ID", anchor=W)
students_list.heading("ID", text="ID", anchor=W)
students_list.heading("Year", text="Year", anchor=W)
students_list.heading("Term", text="Term", anchor=W)
students_list.heading("Program", text="Program", anchor=W)
students_list.heading("Total Enrollment Planned", text="Total Enrollment Planned", anchor=W)
students_list.heading("Planned Students", text="Planned Students", anchor=W)
students_list.heading("Pattern", text="Pattern", anchor=W)

students_list.grid(row=6, 
                    column=0, 
                    columnspan=3, 
                    # rowspan=6, 
                    pady=20,
                    padx=20,
                    sticky="nsew"
                    )

# strap tree
students_list.tag_configure('odd', background="#F4F6F7")
students_list.tag_configure('even', background="#ECF0F1")

students_list.bind('<<TreeviewSelect>>', select_item)

# Set scrollbar
scroll = ttk.Scrollbar(app, orient="vertical", command=students_list.yview)
scroll.grid(
        row=6, 
        column=0, 
        pady=20,
        columnspan=3,  
        sticky='nse'
        )

# configure scrollbar with tree
students_list.configure(yscrollcommand=scroll.set)

populate_list()

# start Program
app.mainloop()
