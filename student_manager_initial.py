from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
# from tkinter import ttk
from db import Database
from os import getenv, getcwd

home_path = getcwd()

db_path = getenv('APPDATA')+'\\student.db'
db = Database(db_path)

# Create window object
app = Tk()
app.title('Course Tracker')
app.geometry('550x550')
app.iconbitmap(home_path+'\\resources\\app-sample-collections.ico')
# canvas = Canvas(app, width=500, height=550)
# canvas.pack(fill="both", expand=True)
# canvas.grid(row=0, column=1)
# canvas.create_image(0, 0, image = PhotoImage(file=home_path+'\\resources\\houses-6504533_640.png'), anchor='nw')
def populate_list():
    students_list.delete(0, END)
    # students_list.insert(0, ('Year', 'Term', 'Program', 'Total Enrollment Planned', 'Planned Students', 'Pattern'))
    for row in db.get_student():
        students_list.insert(END, row)

def add_item():
    if (year_entry.get() == '' or 
        term_entry.get() == '' or 
        program_entry.get() == '' or 
        tot_enroll_planned_entry.get() == '' or 
        plan_students_entry.get() == '' or 
        pattern_entry.get() == "") :
        messagebox.showerror("Required Fields", "Please enter all fields")
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
    row = students_list.curselection()
    print(row)
    selected_item = students_list.get(row[0])
    print(selected_item)
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
    db.modify_sudent(year_entry.get(), term_entry.get(), program_entry.get(), tot_enroll_planned_entry.get(), plan_students_entry.get(), pattern_entry.get(),selected_item[0])
    populate_list()

def remove_item():
    db.remove_student(selected_item[0])
    populate_list()

def export_data():
    file_selected = filedialog.asksaveasfilename(defaultextension=".espace", filetypes=(("Excel file", "*.xlsx"),("All Files", "*.*") ))
    db.export_data(file_selected)

# fields
# year
year_label = Label(app, 
                    text='Year', 
                    font=("TkDefaultFont", 10), 
                    pady=15,
					padx=5
                    )
year_label.grid(sticky=W, row=0, column=0)
year_entry = Entry(app, textvariable=IntVar())
year_entry.grid(sticky=W, row=0, column=1)
# term
term_label = Label(app, 
                    text='Term', 
                    font=('TkDefaultFont', 10), 
                    pady=15,
					padx=5
                    )
term_label.grid(sticky=W, row=1, column=0)
# term_entry = OptionMenu(app, StringVar(), "1","2","3","4")
term_entry = Entry(app, textvariable=StringVar())
term_entry.grid(sticky=W, row=1, column=1)
# program
program_label = Label(app, 
                        text='Program', 
                        font=('TkDefaultFont', 10), 
                        pady=15,
					    padx=5
                        )
program_label.grid(sticky=W, row=2, column=0)
program_entry = Entry(app, textvariable=StringVar())
program_entry.grid(sticky=W, row=2, column=1)
# tepl
tot_enroll_planned_label = Label(app, 
                                text='Total Enrollment Planned', 
                                font=('TkDefaultFont', 10), 
                                pady=15,
					            padx=5
                                )
tot_enroll_planned_label.grid(sticky=W, row=3, column=0)
tot_enroll_planned_entry = Entry(app, textvariable=StringVar())
tot_enroll_planned_entry.grid(sticky=W, row=3, column=1)
# plan_std
plan_students_label = Label(app, 
                            text='Planned Students', 
                            font=('TkDefaultFont', 10), 
                            pady=15,
					        padx=5
                            )
plan_students_label.grid(sticky=W, row=4, column=0)
plan_students_entry = Entry(app, textvariable=StringVar())
plan_students_entry.grid(sticky=W, row=4, column=1)
# pattern
pattern_label = Label(app, 
                        text='Pattern', 
                        font=('TkDefaultFont', 10), 
                        pady=15,
					    padx=5
                        )
pattern_label.grid(sticky=W, row=5, column=0)
pattern_entry = Entry(app, textvariable=StringVar())
pattern_entry.grid(sticky=W, row=5, column=1)

# Buttons
# Add
add_button = Button(app,
                    text='Add Entry', 
                    width=10,
                    command=add_item)
add_button.grid(row=0, column=3)
# Remove
remove_button = Button(app,
                    text='Remove Entry', 
                    width=10,
                    command=remove_item)
remove_button.grid(row=1, column=3)
# Modify
update_button = Button(app,
                    text='Update Entry', 
                    width=10,
                    command=update_item)
update_button.grid(row=2, column=3)
# Clear entry
clear_button = Button(app,
                    text='Clear Entry', 
                    width=10,
                    command=clear_item)
clear_button.grid(row=3, column=3)

export_data_button = Button(app,
                    text='Export Data', 
                    width=10,
                    command=export_data)
export_data_button.grid(row=4, column=3)

# List box
students_list = Listbox(app, 
                        height=12, 
                        width=68,
                        border=1
                        )
# students_list = ttk.Treeview(
#                     app,
#                     columns = ('Year', 'Term', 'Program', 'Total Enrollment Planned', 'Planned Students', 'Pattern'),
#                     show = 'headings',
#                     height = 12
#                     )
students_list.grid(row=6, 
                    column=0, 
                    columnspan=3, 
                    rowspan=6, 
                    pady=20,

                    padx=20)
students_list.bind('<<ListboxSelect>>', select_item)                    
# students_list.bind('<Double-1>', select_item)

# Set scrollbar
scroll = Scrollbar(app)
scroll.grid(row=6, column=3)

students_list.configure(yscrollcommand=scroll.set)
scroll.configure(command=students_list.yview)

populate_list()

# start Program
app.mainloop()
