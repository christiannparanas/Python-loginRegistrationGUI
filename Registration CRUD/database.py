from tkinter import *
from tkinter import messagebox
# need to import the sqlite3
import sqlite3
import time


root = Tk()
root.title('Using Databases')
root.iconbitmap('icons\christian.ico')
root.geometry('360x500+400+80')


#============== DATABASE CONFIGURATION =========================

# Create a Database or if already exist connect to it, have the same syntax
conn = sqlite3.connect('address_book.db')

# create cursor, thing you send to do stuff, doing some sort of commands
cur = conn.cursor()

# sqlite3 only have 5 datatypes, text, integer=whole numbers, real=float, null=doesn't exist, blob

# create table, you comment the table if its already created
# try and except handle the error of creating already exist table in the database
# because if you'll not handle that statement it will throw an error

try:
    cur.execute("""CREATE TABLE addresses (
        first_name text,
        last_name text,
        address text,
        city text,
        state text,
        zipcode integer
    )""")
except:
    print(" ")
    # print("An exception occured!, because table already exist in the database.\n\n")


#===================== FUNCTIONS ==================================


# Create a Submit Function
def submit():
    # connection inside of the function
    conn = sqlite3.connect('address_book.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO addresses VALUES (:first, :last, :add, :city, :state, :zip)",
            {
                'first': f_name.get().capitalize(),
                'last': l_name.get().capitalize(),
                'add': address.get().capitalize(),
                'city': city.get().capitalize(),
                'state': state.get().capitalize(),
                'zip': zipcode.get()
            }
        )

    # Commit changes
    conn.commit()
    # Close connection
    conn.close()

    # clear the textboxes everytime we click the sunmit button
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)

# Query - request to retrieve data or show data from the database
def query():
    # connection inside of the function
    conn = sqlite3.connect('address_book.db')
    cur = conn.cursor()

    # Query the database
    # you should create a primary key for each record in the database, unique number
    # in sqite3 it will create for you or you want to create a primary key yourself
    # oid - unique id number of each record
    cur.execute("SELECT oid, * FROM addresses")

    # fetchall to fetch all of the records in the table on the database
    # fetchone = fetch one rcord
    # fetchmany(50) = fetch 50 records, depends on you, how many records you want to fetch
    records = cur.fetchall()    # put the fetch records to a variable

    # print(records)

    # kailangan mo munang ideclare yung variable bago mo ilagay sa label or function, or in the other methods
    print_records = ""

    # Loop para makuha lahat ng value ng table, na hindi na nakalagay sa list at tuple
    for record in records:
        # need mo munang icast kasi int yung ibang value sa table, cast into string to concatinate it with "\n" new line
        # kailangan ng newline kasi para ibaba yung susunod na value
        print_records += str(record[0]) + "\t" + record[1] + " " + record[2] + "\n"


    # Result of the query put in a Label
    query_label = Label(root, text=print_records)
    query_label.grid(row=14, column=0, columnspan=2)


    # Commit changes
    conn.commit()
    # Close connection
    conn.close()


# Create a Delete function to delete a record
def delete():
    conn = sqlite3.connect('address_book.db')
    cur = conn.cursor()

    # Delete a Record
    # Delete a record reference to its unique id number, you can reference the values but sometimes values have a similar to the other values
    cur.execute("DELETE FROM addresses WHERE oid= " + select_box.get())

    # Commit changes
    conn.commit()
    # Close connection
    conn.close()
    # to delete the content of the entry box after the button got pressed
    select_box.delete(0, END)


# Save function to the updated info's
def save():
    conn = sqlite3.connect('address_book.db')
    cur = conn.cursor()

    # put the selected oid/id, to a variable
    record_id = select_box.get()

    # Save updated info to the database
    cur.execute("""UPDATE addresses SET
        first_name = :first,
        last_name = :last,
        address = :address,
        city = :city,
        state = :state,
        zipcode = :zipcode

        WHERE oid = :oid""",
        {
            'first': f_name_editor.get(),
            'last': l_name_editor.get(),
            'address': address_editor.get(),
            'city': city_editor.get(),
            'state': state_editor.get(),
            'zipcode': zipcode_editor.get(),

            'oid': record_id
        }
        )

    # Commit changes
    conn.commit()
    # Close connection
    conn.close()
    showinfo()



def showinfo():
    response = messagebox.showinfo("Pasabot hahaha", "Data Updated!")
    # time.sleep(1)
    editor.destroy()



# Update or Edit Function
def edit():
    global editor
    editor = Tk()
    editor.title('Update Record')
    editor.iconbitmap('icons\christian.ico')
    editor.geometry('360x190+410+85')

    conn = sqlite3.connect('address_book.db')
    cur = conn.cursor()

    # Create a variable and put the select box value to a variable
    record_id = select_box.get()

    cur.execute("SELECT * FROM addresses WHERE oid = " + record_id)
    records = cur.fetchall()

    select_box.delete(0, END)


    # Make the variable Global to able use it in the other/outside functions
    # Global variable for entry box
    global f_name_editor
    global l_name_editor
    global address_editor
    global city_editor
    global state_editor
    global zipcode_editor

    # Entry boxes
    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))

    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=1, column=1, padx=20)

    address_editor = Entry(editor, width=30)
    address_editor.grid(row=2, column=1, padx=20)

    city_editor = Entry(editor, width=30)
    city_editor.grid(row=3, column=1, padx=20)

    state_editor = Entry(editor, width=30)
    state_editor.grid(row=4, column=1, padx=20)

    zipcode_editor = Entry(editor, width=30)
    zipcode_editor.grid(row=5, column=1, padx=20)

    # Entry boxes Labels
    f_label = Label(editor, text='First Name').grid(row=0, column=0, pady=(10, 0))
    l_label = Label(editor, text='Last Name').grid(row=1, column=0)
    add_label = Label(editor, text='Address').grid(row=2, column=0)
    city_label = Label(editor, text='City').grid(row=3, column=0)
    state_label = Label(editor, text='Province').grid(row=4, column=0)
    zip_label = Label(editor, text='Zipcode').grid(row=5, column=0)

    # Loop thru results
    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        address_editor.insert(0, record[2])
        city_editor.insert(0, record[3])
        state_editor.insert(0, record[4])
        zipcode_editor.insert(0, record[5])

    # Update Button
    update_btn = Button(editor, text="Update Record", pady=5, command=tunnel_two)
    update_btn.grid(row=7, column=0, columnspan=2, pady=(10, 5), padx=10, ipadx=125)


# Error Function, if something wrong in the tunnel function it will pop-up

def showError():
    messagebox.showerror("Sayop", "No Input!")


# Tunnel functions, where the buttons go thru if the entry boxes is empty or not

def tunnel_one():
    # if the f_name entry box is empty it will throw an error messagebox
    if f_name.get() == "":
        showError()
    else:
        submit()

def tunnel_two():
    if f_name_editor.get() == "":
        showError()
    else:
        save()

def tunnel_three():
    if select_box.get() == "":
        showError()
    else:
        # I put it so that if delete button is pressed it automatically refresh the show reseult list
        delete()
        query()

def tunnel_four():
    # if the entry box is empty it throw an error message box
    if select_box.get() == "":
        showError()
    # if else, it just go straight to the edit function
    else:
        edit()






#================= ENTRY BOXES AND LABELS =====================


# Entry boxes
f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20, pady=(10, 0))  # if you want to add padding on the top and not on the bottom, left = Top, right = Bottom

l_name = Entry(root, width=30)
l_name.grid(row=1, column=1, padx=20)

address = Entry(root, width=30)
address.grid(row=2, column=1, padx=20)

city = Entry(root, width=30)
city.grid(row=3, column=1, padx=20)

state = Entry(root, width=30)
state.grid(row=4, column=1, padx=20)

zipcode = Entry(root, width=30)
zipcode.grid(row=5, column=1, padx=20)

# Delete Entry box
select_box = Entry(root, width=30)
select_box.grid(row=8, column=1, columnspan=2)

# Entry boxes Labels
f_label = Label(root, text='First Name').grid(row=0, column=0, pady=(10, 0))  # add also here because they're partner, the enrty box and the label
l_label = Label(root, text='Last Name').grid(row=1, column=0)
add_label = Label(root, text='Address').grid(row=2, column=0)
city_label = Label(root, text='City').grid(row=3, column=0)
state_label = Label(root, text='Province').grid(row=4, column=0)
zip_label = Label(root, text='Zipcode').grid(row=5, column=0)

# Delete Label
delete_label = Label(root, text="Select ID:")
delete_label.grid(row=8, column=0)


#=================== BUTTONS ==========================

# Submit Button
submit_btn = Button(root, text='Add Record To Database', pady=5, command=tunnel_one)
submit_btn.grid(row=6, column=0, columnspan=2, pady=(10, 5), padx=10, ipadx=100)

# Query Button
query_btn = Button(root, text="Show Records", pady=5, command=query)
query_btn.grid(row=7, column=0, columnspan=2, pady=(0, 20), padx=10, ipadx=127)

# Delete Button
delete_btn = Button(root, text="Delete Record", pady=5, command=tunnel_three)
delete_btn.grid(row=10, column=0, columnspan=2, pady=(5, 4), padx=10, ipadx=127)

# Update Button

update_btn = Button(root, text="Edit Record", pady=5, command=tunnel_four)
update_btn.grid(row=11, column=0, columnspan=2, pady=(2, 5), padx=10, ipadx=133)






# anytime we need to change in our database we need to commit that change
conn.commit()

# when we're done, we need to close the connection
conn.close()


root.mainloop()
