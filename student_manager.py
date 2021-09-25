from tkinter import *

# Create window object
app = Tk()

def add_item():
    pass

def clear_item():
    pass

def update_item():
    pass

def remove_item():
    pass

def clear_all_item():
    pass

def export_data():
    pass

# fields
year_label = Label(app, 
                    text='Year', 
                    font=('bold', 10), 
                    pady=15,
					padx=5
                    )
year_label.grid(sticky=W, row=0, column=0)
year_entry = Entry(app, textvariable=IntVar())
year_entry.grid(sticky=W, row=0, column=1)

term_label = Label(app, 
                    text='Term', 
                    font=('bold', 10), 
                    pady=15,
					padx=5
                    )
term_label.grid(sticky=W, row=0, column=2)
term_entry = Entry(app, textvariable=StringVar())
term_entry.grid(sticky=W, row=0, column=3)

program_label = Label(app, 
                        text='Program', 
                        font=('bold', 10), 
                        pady=15,
					    padx=5
                        )
program_label.grid(sticky=W, row=1, column=0)
program_entry = Entry(app, textvariable=StringVar())
program_entry.grid(sticky=W, row=1, column=1)

tot_enroll_planned_label = Label(app, 
                                text='Total Enrollment Planned', 
                                font=('bold', 10), 
                                pady=15,
					            padx=5
                                )
tot_enroll_planned_label.grid(sticky=W, row=1, column=2)
tot_enroll_planned_entry = Entry(app, textvariable=StringVar())
tot_enroll_planned_entry.grid(sticky=W, row=1, column=3)

plan_students_label = Label(app, 
                            text='Planned Students', 
                            font=('bold', 10), 
                            pady=15,
					        padx=5
                            )
plan_students_label.grid(sticky=W, row=2, column=0)
plan_students_entry = Entry(app, textvariable=StringVar())
plan_students_entry.grid(sticky=W, row=2, column=1)

pattern_label = Label(app, 
                        text='Pattern', 
                        font=('bold', 10), 
                        pady=15,
					    padx=5
                        )
pattern_label.grid(sticky=W, row=2, column=2)
pattern_entry = Entry(app, textvariable=StringVar())
pattern_entry.grid(sticky=W, row=2, column=3)


# List box
students_list = Listbox(app, 
                        height=20, 
                        width=80,
                        border=10
                        )
students_list.grid(row=5, 
                    column=0, 
                    columnspan=3, 
                    rowspan=6, 
                    pady=20,
                    padx=20)

# Set scrollbar
scroll = Scrollbar(app)
scroll.grid(row=5, column=3)

students_list.configure(yscrollcommand=scroll.set)
scroll.configure(command=students_list.yview)

# Buttons
add_button = Button(app,
                    text='Add Entry', 
                    width=10,
                    command=add_item)
add_button.grid(row=3, column=0, pady=20)

remove_button = Button(app,
                    text='Remove Entry', 
                    width=10,
                    command=remove_item)
remove_button.grid(row=3, column=1, pady=20)

update_button = Button(app,
                    text='Update Entry', 
                    width=10,
                    command=update_item)
update_button.grid(row=3, column=2, pady=20)

clear_button = Button(app,
                    text='Clear Entry', 
                    width=10,
                    command=clear_item)
clear_button.grid(row=3, column=3, pady=20)

clear_all_button = Button(app,
                    text='Clear All', 
                    width=10,
                    command=clear_all_item)
clear_all_button.grid(row=4, column=0, pady=20)

export_data_button = Button(app,
                    text='Export Data', 
                    width=10,
                    command=export_data)
export_data_button.grid(row=4, column=1, pady=20)

app.title('Part Manger')
app.geometry('700x700')

# start Program
app.mainloop()