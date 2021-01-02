from tkinter import *
import tkinter as tk
import sqlite3

window = tk.Tk()

# Data base
money_list = []

# Create a data base or connect to one
conn = sqlite3.connect('Pet_expense.db')

# Creating a cursor
c = conn.cursor()

# Creating a table
'''
c.execute("""CREATE TABLE addresses (
	money real,
	info text,
	gender text,
	name text)""")
'''


# Commit connection

#  Creating aa submitting function for data base
def submit():
    # Create a data base or connect to one
    conn = sqlite3.connect('Pet_expense.db')

    # Creating a cursor
    c = conn.cursor()

    # Inserting data into table
    c.execute("INSERT INTO addresses VALUES (:money, :info, :gender, :name)",
              {
                  'money': entry.get(),
                  'info': spent_on_input.get(),
                  'gender': gender_input.get(),
                  'name': name_entry.get()
              })

    conn.commit()

    # Close connection
    conn.close()

    # Clearing  text box
    entry.delete(0, END)
    spent_on_input.delete(0, END)
    gender_input.delete(0, END)
    name_entry.delete(0, END)


# Create function to delete record
def delete():
    # Create a data base or connect to one
    conn = sqlite3.connect('Pet_expense.db')

    # Creating a cursor
    c = conn.cursor()

    # Delete a record
    c.execute("DELETE from addresses WHERE oid= " + delete_box.get())

    conn.commit()

    # Close connection
    conn.close()


def update():
    conn = sqlite3.connect('Pet_expense.db')

    # Creating a cursor
    c = conn.cursor()

    record_id = delete_box.get()
    c.execute("""UPDATE addresses SET
        money = :money,
        info = :info,
        gender = :gender,
        name = :name
    
        WHERE oid = :oid""",
              {'money': entry_editor.get(),
               'info': spent_on_input_editor.get(),
               'gender': gender_input_editor.get(),
               'name': name_entry_editor.get(),

               'oid': record_id
               })

    conn.commit()

    # Close connection
    conn.close()

    editor.destroy()


# Create edit function to update record
def edit():
    global editor
    editor = tk.Tk()
    editor.title("Update a record!")
    editor.geometry("400x600")

    conn = sqlite3.connect('Pet_expense.db')

    # Creating a cursor
    c = conn.cursor()

    record_id = delete_box.get()
    # Query the data base
    c.execute("SELECT * FROM addresses WHERE oid = " + record_id)
    records = c.fetchall()

    # Create global vars for text box editor
    global entry_editor
    global spent_on_input_editor
    global gender_input_editor
    global name_entry_editor

    background_editor = tk.Frame(editor, bg="#00FC45")
    background_editor.place(relwidth=1, relheight=1)

    # User Enters Price
    entry_editor = tk.Entry(background_editor, font=('Impact', 13))
    entry_editor.place(relx=0.4, rely=0.05, relwidth=0.2, relheight=0.05)

    enter_expenses_label_editor = tk.Label(background_editor, bg="#DC43D3", text="Enter your expenses",
                                           font=('Times New Roman CYR', 13, 'bold'))
    enter_expenses_label_editor.place(relx=0.2, rely=0.05, relwidth=.2, relheight=.05)

    # Gender/Info of pet
    gender_label_editor = tk.Label(background_editor, bg="#43CCDC", text="Choose Gender",
                                   font=('Times New Roman CYR', 13, 'bold'))
    gender_label_editor.place(relx=0.2, rely=0.2, relwidth=.2, relheight=.05)

    gender_input_editor = Entry(background_editor, font=('Impact', 13))
    gender_input_editor.place(relx=0.4, rely=0.2, relwidth=.2, relheight=.05)

    # Birth of pet
    birth_label_editor = Label(background_editor, text="Enter your pets birthdate", bg="#DC43D3",
                               font=('Times New Roman CYR', 13, 'bold'))
    birth_label_editor.place(relx=0.2, rely=0.15, relwidth=.2, relheight=.05)

    name_entry_editor = Entry(background_editor, font=('Impact', 13))
    name_entry_editor.place(relx=0.4, rely=0.15, relwidth=0.2, relheight=0.05)

    # Lets user input what money was spent on
    money_spent_on_editor = tk.Label(background_editor, bg="#43CCDC", text="Money spent on: ",
                                     font=('Times New Roman CYR', 13, 'bold'))
    money_spent_on_editor.place(relx=0.2, rely=0.1, relwidth=.2, relheight=.05)

    spent_on_input_editor = Entry(background_editor, font=('Impact', 13))
    spent_on_input_editor.place(relx=0.4, rely=0.1, relwidth=.2, relheight=.05)

    # SAVE BUTTON
    save_button_editor = tk.Button(background_editor, bg="#DC43D3", text="SAVE RECORD",
                                   font=('Times New Roman CYR', 13, 'bold'), command=update)
    save_button_editor.place(relx=0.4, rely=0.25, relwidth=.2, relheight=.05)

    # Loop through results
    for record in records:
        entry_editor.insert(0, record[0])
        spent_on_input_editor.insert(0, record[1])
        gender_input_editor.insert(0, record[2])
        name_entry_editor.insert(0, record[3])

    conn.commit()

    # Close connection
    conn.close()


def query():
    conn = sqlite3.connect('Pet_expense.db')

    # Creating a cursor
    c = conn.cursor()

    conn.commit()

    # Query the data base
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()
    # Loop through results
    print_records = ""
    total = 0.0
    for record in records:
        print_records += str(record[0]) + " spent on " + str(record[1]) + " | ID: " + str(record[4]) + "\n"
    for money in records:
        money_list.append(float(money[0]))
    for i in money_list:
        float(i)
        total += i
    query_label = Label(background, text=print_records, bg="#00CDFF", font=('Times New Roman CYR', 12, 'bold'))
    query_label.place(rely=0.5, relwidth=1, relheight=0.5)

    grand_total = Label(query_label, text=f"Grand total: ${total}", bg="#00CDFF",
                        font=('Times New Roman CYR', 12, 'bold'))
    grand_total.place(relx=.7, relwidth=.3, relheight=0.5)

    # Close connection
    conn.close()


# Function to view actual info on pet (Pulls from SQL data base)
def info_pull():
    conn = sqlite3.connect('Pet_expense.db')

    # Creating a cursor
    c = conn.cursor()

    conn.commit()

    # Query the data base
    c.execute("SELECT *, oid FROM addresses")
    info_pet = c.fetchall()
    print_info = ""
    for info in info_pet:
        print_info += "Gender:" + str(info[2]) + ", Birthdate " + str(info[3]) + "\n"
    info_label = Label(background, text=print_info, bg="#00CDFF", font=('Times New Roman CYR', 12, 'bold'))
    info_label.place(rely=0.5, relwidth=1, relheight=0.5)
    # Close connection
    conn.close()


def ask_view():
    view = tk.Label(background, bg="#00CDFF", text="What would you like to view?",
                    font=('Times New Roman CYR', 13, 'bold'))
    view.place(relx=0.8, rely=0.05, relwidth=.2, relheight=.05)
    # Expenses button
    expense_button = tk.Button(background, bg="#00FF9E", text="Expenses", font=('Times New Roman CYR', 13, 'bold'),
                               command=lambda: query())
    expense_button.place(relx=0.8, rely=0.1, relwidth=.2, relheight=.05)
    # Info Button
    info_button = tk.Button(background, bg="#FFC500", text="Information", font=('Times New Roman CYR', 13, 'bold'),
                            command=lambda: info_pull())
    info_button.place(relx=0.8, rely=0.15, relwidth=.2, relheight=.05)


# Creating label widget
window.title("Pet Expenses App")
canvas = tk.Canvas(window, height=440, width=700, )

background = tk.Frame(window, bg="#00FC45")
background.place(relwidth=1, relheight=1)

intro = tk.Label(background, bg="#F0FF00", text="PET EXPENSE TRACKER", font=('Times New Roman CYR', 13, 'bold'))
intro.place(relwidth=1, relheight=.05)

pets = tk.Label(background, bg="#352CFF", text="PETS", font=('Times New Roman CYR', 13, 'bold'))
pets.place(rely=0.05, relwidth=.2, relheight=0.05)

miloButton = tk.Button(background, bg="#C100FF", text="Pet (click me)", font=('Times New Roman CYR', 13, 'bold'), bd=0,
                       command=lambda: ask_view())
miloButton.place(rely=0.1, relwidth=.2, relheight=.05)

# User Enters Price
entry = tk.Entry(background, font=('Impact', 13))
entry.place(relx=0.4, rely=0.05, relwidth=0.2, relheight=0.05)

enter_expenses_label = tk.Label(background, bg="#DC43D3", text="Enter your expenses",
                                font=('Times New Roman CYR', 13, 'bold'))
enter_expenses_label.place(relx=0.2, rely=0.05, relwidth=.2, relheight=.05)

# Gender/Info of pet
gender_label = tk.Label(background, bg="#43CCDC", text="Choose Gender",
                        font=('Times New Roman CYR', 13, 'bold'))
gender_label.place(relx=0.2, rely=0.25, relwidth=.2, relheight=.05)

gender_input = Entry(background, font=('Impact', 13))
gender_input.place(relx=0.4, rely=0.25, relwidth=.2, relheight=.05)

# Name of pet
name_label = Label(background, text="Enter your pets name", bg="#DC43D3",
                   font=('Times New Roman CYR', 13, 'bold'))
name_label.place(relx=0.2, rely=0.2, relwidth=.2, relheight=.05)

name_entry = Entry(background, font=('Impact', 13))
name_entry.place(relx=0.4, rely=0.2, relwidth=0.2, relheight=0.05)

# Lets user input what money was spent on
money_spent_on = tk.Label(background, bg="#43CCDC", text="Money spent on: ",
                          font=('Times New Roman CYR', 13, 'bold'))
money_spent_on.place(relx=0.2, rely=0.1, relwidth=.2, relheight=.05)

spent_on_input = Entry(background, font=('Impact', 13))
spent_on_input.place(relx=0.4, rely=0.1, relwidth=.2, relheight=.05)

enter_button = tk.Button(background, bg="#DC43D3", text="ENTER TO DATA BASE", font=('Times New Roman CYR', 13, 'bold'),
                         command=lambda: submit())
enter_button.place(relx=0.4, rely=0.30, relwidth=.2, relheight=.05)

# DELETE SECTION FOR DELETING DATA
delete_button = tk.Button(background, bg="#DC43D3", text="DELETE RECORD", font=('Times New Roman CYR', 13, 'bold'),
                          command=lambda: delete())
delete_button.place(relx=0.4, rely=0.4, relwidth=.2, relheight=.05)

delete_box = Entry(background, font=('Impact', 13))
delete_box.place(relx=0.4, rely=0.15, relwidth=0.2, relheight=0.05)

delete_label = tk.Label(background, bg="#DC43D3", text="Select ID to delete (press expense to view):",
                        font=('Times New Roman CYR', 13, 'bold'))
delete_label.place(relx=0.2, rely=0.15, relwidth=.2, relheight=.05)

query_button = Button(background, text="Show Records", bg="#DC43D3", font=('Times New Roman CYR', 13, 'bold'),
                      command=query)
query_button.place(relx=0.4, rely=0.35, relwidth=.2, relheight=.05)

# Edit record button
edit_button = tk.Button(background, bg="#DC43D3", text="EDIT RECORD", font=('Times New Roman CYR', 13, 'bold'),
                        command=lambda: edit())
edit_button.place(relx=0.40, rely=0.4, relwidth=.2, relheight=.05)

# Instructions for user

free_label = Label(background, bg="#DC43D3", text="""If you got something for free, type 0 in 
money spent on""", font=('Times New Roman CYR', 13, 'bold'))
free_label.place(relx=0.6, rely=0.05, relwidth=.2, relheight=.2)

# Commit connection

conn.commit()

# Close connection
conn.close()

window.mainloop()
