from tkinter import *
from tkinter import ttk, simpledialog, messagebox
from classes.dbutils import DbUtils


def get_database_options():
    # Connect to the MySql server (database=None means that no specific database is selected)
    connection = DbUtils.get_connection(user="root", password="", host="localhost", database=None)

    # If the connection is unsuccessful, return an empty list
    if connection is None:
        return []

    # If the connection is successful, get all databases and return them
    databases = DbUtils.get_all_databases(connection)

    # If the statement is unsuccessful, return an empty list
    if databases is None:
        return []

    # Close the connection
    connection.close()

    return databases


def get_table_options(database):
    # Connect to the MySql server's specified database
    connection = DbUtils.get_connection(user="root", password="", host="localhost", database=database)

    # If the connection is unsuccessful, return an empty list
    if connection is None:
        return []

    # If the connection is successful, get all tables and return them
    tables = DbUtils.get_all_tables(connection)

    # If the statement is unsuccessful, return an empty list
    if tables is None:
        return []

    # Close the connection
    connection.close()

    return tables


def insert_record(database, table, columns, values):
    # Connect to the MySql server's specified database
    connection = DbUtils.get_connection(user="root", password="", host="localhost", database=database)

    # If the connection is unsuccessful, return False
    if connection is None:
        return False

    # If the connection is successful, insert the record and return True
    result = DbUtils.insert_row(connection, table, columns, values)

    # If the statement is unsuccessful, return False
    if result is None:
        return False

    # Close the connection
    connection.close()

    return True


def get_table(database, table):
    # Connect to the MySql server's specified database
    connection = DbUtils.get_connection(user="root", password="", host="localhost", database=database)

    # If the connection is unsuccessful, return an empty list
    if connection is None:
        return []

    # If the connection is successful, get table's content and headers and return them
    table = DbUtils.get_table(connection, table)

    # If the statement is unsuccessful, return an empty list
    if table is None:
        return []

    # Close the connection
    connection.close()

    return table


def create_database(database):
    # Connect to the MySql server (database=None means that no specific database is selected)
    connection = DbUtils.get_connection(user="root", password="", host="localhost", database=None)

    # If the connection is unsuccessful, return False
    if connection is None:
        return False

    # If the connection is successful, create the database and return its name
    result = DbUtils.create_database(connection, database)

    # If the statement is unsuccessful, return False
    if result is None:
        return False

    # Close the connection
    connection.close()

    return database


def delete_database(database):
    # Connect to the MySql server (database=None means that no specific database is selected)
    connection = DbUtils.get_connection(user="root", password="", host="localhost", database=None)

    # If the connection is unsuccessful, return False
    if connection is None:
        return False

    # If the connection is successful, delete the database and return True
    result = DbUtils.delete_database(connection, database)

    # If the statement is unsuccessful, return False
    if result is None:
        return False

    # Close the connection
    connection.close()

    return True


def create_table(database, table, properties):
    # Connect to the MySql server's specified database
    connection = DbUtils.get_connection(user="root", password="", host="localhost", database=database)

    # If the connection is unsuccessful, return False
    if connection is None:
        return False

    # If the connection is successful, create the table and return True
    result = DbUtils.create_table(connection, table, properties)

    # If the statement is unsuccessful, return False
    if result[0] is None:
        messagebox.showerror("Error", result[1])
        return False

    # Close the connection
    connection.close()

    return True


def delete_table(database, table):
    # Connect to the MySql server's specified database
    connection = DbUtils.get_connection(user="root", password="", host="localhost", database=database)

    # If the connection is unsuccessful, return False
    if connection is None:
        return False

    # If the connection is successful, delete the table and return True
    result = DbUtils.delete_table(connection, table)

    # If the statement is unsuccessful, return False
    if result is None:
        return False

    # Close the connection
    connection.close()

    return True


def delete_record(database, table, columns, values):
    # Connect to the MySql server's specified database
    connection = DbUtils.get_connection(user="root", password="", host="localhost", database=database)

    # If the connection is unsuccessful, return False
    if connection is None:
        return False

    # If the connection is successful, delete the record and return True
    result = DbUtils.delete_row(connection, table, columns, values)

    # If the statement is unsuccessful, return False
    if result is None:
        return False

    # Close the connection
    connection.close()

    return True


class App:
    def __init__(self):
        # Frame for database and table selection
        self.select_frame = None

        # Database and table variables
        self.database = None
        self.table = None

        # Database and table options
        self.database_options = []
        self.table_options = []

        # Table dropdown menu
        self.table_menu = None

        # Table data and its frame
        self.table_data = None
        self.table_frame = None
        self.table_data_display = None

        # Frame for action buttons
        self.action_frame = None

        # New table data
        self.table_create_name = None
        self.table_create_property_name = None
        self.table_create_property_type = None
        self.table_create_property_unique = None
        self.table_create_property_not_null = None
        self.table_create_property_auto_increment = None
        self.table_create_property_primary_key = None

        # New table data frame
        self.table_create_frame = None
        self.table_create_buttons_frame = None
        self.table_create_window = None
        self.table_create_tree = None
        self.table_create_property_frame = None

        # Record action frame
        self.table_records_action_frame = None

        # Record window
        self.table_record_create_window = None
        self.table_record_create_frame = None
        self.table_record_create_inputs = []

        self.root = Tk()
        self.root.title("TkinterAdmin")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Title label
        Label(self.root, text="TkinterAdmin", font=("Arial", 20)).pack()

        # Frame for database and table selection
        self.select_frame = Frame(self.root)
        self.select_frame.pack()

        # Database and table dropdowns' labels
        Label(self.select_frame, text="Database").grid(row=0, column=0)
        Label(self.select_frame, text="Table").grid(row=0, column=1)

        # Database and table options are stored in StringVar variables
        self.database = StringVar()
        self.table = StringVar()

        # Get the options for the dropdowns and set the default values
        # Trace the database dropdown's value and call the handle_database_change() method when it changes
        # Set the first table and dropdown menu as well
        self.database_options = get_database_options()

        self.set_new_option_menu("database")

        self.database.trace("w", lambda *args: self.handle_database_change())

        self.table_options = get_table_options(self.database.get())

        self.set_new_option_menu("table")

        # Get the table content and headers, display them in a table-like presentation
        self.table_frame = Frame(self.root)
        self.table_frame.pack()

        self.set_new_table()
        self.table.trace("w", lambda *args: self.set_new_table())

        # Frame for action buttons
        self.action_frame = Frame(self.root)
        self.action_frame.pack()

        # Database action buttons
        Label(self.action_frame, text="Database").grid(row=0, column=0)
        Button(self.action_frame, text="Create", command=self.handle_database_create).grid(row=1, column=0)
        Button(self.action_frame, text="Delete", command=self.handle_database_delete).grid(row=2, column=0)

        # Table action buttons
        Label(self.action_frame, text="Table").grid(row=0, column=1)
        Button(self.action_frame, text="Create", command=self.handle_table_create).grid(row=1, column=1)
        Button(self.action_frame, text="Delete", command=self.handle_table_delete).grid(row=2, column=1)

        # Frame for table's records action buttons
        self.table_records_action_frame = Frame(self.root)
        self.table_records_action_frame.pack()

        # Table's records action buttons
        Label(self.table_records_action_frame, text="Table's records").grid(row=0, column=0)
        Button(self.table_records_action_frame, text="Create", command=self.handle_table_record_create).grid(row=1, column=0)
        Button(self.table_records_action_frame, text="Update", command=self.handle_table_record_update).grid(row=2, column=0)
        Button(self.table_records_action_frame, text="Delete", command=self.handle_table_record_delete).grid(row=3, column=0)

    def set_new_option_menu(self, table_type):
        # If the table type is database, create a new database dropdown menu
        # If the table type is table, create a new table dropdown menu
        # If there are no results, set the corresponding variable to an empty string
        if table_type == "database":
            if len(self.database_options) > 0:
                self.database.set(self.database_options[0])
                OptionMenu(self.select_frame, self.database, *self.database_options).grid(row=1, column=0)
            else:
                self.table.set("")
                OptionMenu(self.select_frame, self.database, "").grid(row=1, column=0)
        elif table_type == "table":
            if len(self.table_options) > 0:
                self.table.set(self.table_options[0])
                self.table_menu = OptionMenu(self.select_frame, self.table, *self.table_options)
            else:
                self.table.set("")
                self.table_menu = OptionMenu(self.select_frame, self.table, "")

            self.table_menu.grid(row=1, column=1)

    def handle_database_change(self):
        # Get the options for the table dropdown and set the default value
        if self.database.get() != "":
            self.table_options = get_table_options(self.database.get())

            # Destroy the old table dropdown and create a new one
            self.table_menu.destroy()

            self.set_new_option_menu("table")

    def handle_table_change(self):
        self.set_new_table()

    def set_new_table(self):
        # Get the table content and headers once again and refresh their presentation
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        if self.table.get() != "":
            self.table_data = get_table(self.database.get(), self.table.get())
        else:
            return

        # Display the data in a Treeview widget
        if len(self.table_data) > 0:
            self.table_data_display = ttk.Treeview(self.table_frame, columns=self.table_data[0], show="headings")

            for column in self.table_data[0]:
                self.table_data_display.heading(column, text=column)

            for row in self.table_data[1]:
                self.table_data_display.insert("", "end", values=row)

            self.table_data_display.pack()

    def handle_database_create(self):
        # Create a new database with a name that the user inputs
        database = simpledialog.askstring("Create database", "Enter the name of the new database:")

        if database is not None:
            if create_database(database):
                self.database_options = get_database_options()
                self.set_new_option_menu("database")
                self.database.set(database)
            else:
                messagebox.showerror("Error", "The database could not be created.")

    def handle_database_delete(self):
        # Delete the selected database
        if self.database.get() != "":
            if delete_database(self.database.get()):
                self.database_options = get_database_options()
                self.set_new_option_menu("database")
            else:
                messagebox.showerror("Error", "The database could not be deleted.")

    def handle_table_create(self):
        # Spawn a new window with a treeview widget that displays the created columns and their properties
        # The user can add new columns and change their properties using a set of inputs and checkboxes in property_frame
        # The user can also delete columns
        # The user can save the table and its columns
        self.table_create_window = Toplevel(self.root)
        self.table_create_window.title("Create table")

        self.table_create_frame = Frame(self.table_create_window)
        self.table_create_frame.pack()

        self.table_create_name = Entry(self.table_create_frame)
        self.table_create_name.pack()

        self.table_create_tree = ttk.Treeview(self.table_create_frame, columns=("name", "type", "not null", "unique", "primary key", "auto increment"), show="headings")

        for column in ("name", "type", "not null", "unique", "primary key", "auto increment"):
            self.table_create_tree.heading(column, text=column)

        self.table_create_tree.pack()

        self.table_create_buttons_frame = Frame(self.table_create_window)
        self.table_create_buttons_frame.pack()

        Button(self.table_create_buttons_frame, text="Add column", command=self.handle_table_create_add_column).grid(row=0, column=0)
        Button(self.table_create_buttons_frame, text="Delete column", command=self.handle_table_create_delete_column).grid(row=0, column=1)
        Button(self.table_create_buttons_frame, text="Edit column", command=self.handle_table_create_edit_column).grid(row=0, column=3)
        Button(self.table_create_buttons_frame, text="Save", command=self.handle_table_create_save).grid(row=0, column=2)

        self.table_create_property_frame = Frame(self.table_create_window)
        self.table_create_property_frame.pack()

        Label(self.table_create_property_frame, text="Name").grid(row=0, column=1)
        self.table_create_property_name = Entry(self.table_create_property_frame)
        self.table_create_property_name.grid(row=0, column=2)

        Label(self.table_create_property_frame, text="Type").grid(row=1, column=1)
        self.table_create_property_type = Entry(self.table_create_property_frame)
        self.table_create_property_type.grid(row=1, column=2)

        self.table_create_property_unique = IntVar()
        Checkbutton(self.table_create_property_frame, text="Unique", variable=self.table_create_property_unique).grid(row=3, column=0)

        self.table_create_property_not_null = IntVar()
        Checkbutton(self.table_create_property_frame, text="Not null", variable=self.table_create_property_not_null).grid(row=3, column=1)

        self.table_create_property_primary_key = IntVar()
        Checkbutton(self.table_create_property_frame, text="Primary key", variable=self.table_create_property_primary_key).grid(row=3, column=2)

        self.table_create_property_auto_increment = IntVar()
        Checkbutton(self.table_create_property_frame, text="Auto increment", variable=self.table_create_property_auto_increment).grid(row=3, column=3)

        self.table_create_property_frame.grid_remove()

    def handle_table_delete(self):
        # Delete the selected table
        if self.table.get() != "":
            if delete_table(self.database.get(), self.table.get()):
                self.table_options = get_table_options(self.database.get())
                self.set_new_option_menu("table")
            else:
                messagebox.showerror("Error", "The table could not be deleted.")

    def handle_table_create_add_column(self):
        # Show an error if the user tries to add a column without filling in the name and type
        if self.table_create_property_name.get() == "" or self.table_create_property_type.get() == "":
            messagebox.showerror("Error", "Please fill in the name and type of the column.")
            return
        # Add a new column to the table
        self.table_create_tree.insert("", "end", values=(self.table_create_property_name.get(),
                                                         self.table_create_property_type.get(),
                                                         self.table_create_property_unique.get(),
                                                         self.table_create_property_not_null.get(),
                                                         self.table_create_property_primary_key.get(),
                                                         self.table_create_property_auto_increment.get()))
        self.clear_table_create_inputs()

    def clear_table_create_inputs(self):
        # Clear the inputs in the property_frame
        self.table_create_property_name.delete(0, "end")
        self.table_create_property_type.delete(0, "end")
        self.table_create_property_unique.set(0)
        self.table_create_property_not_null.set(0)
        self.table_create_property_primary_key.set(0)
        self.table_create_property_auto_increment.set(0)

    def handle_table_create_delete_column(self):
        # Delete the selected column
        selected = self.table_create_tree.selection()
        if len(selected) > 0:
            self.table_create_tree.delete(selected[0])

    def handle_table_create_edit_column(self):
        # Edit the selected column
        selected = self.table_create_tree.selection()
        if len(selected) > 0:
            self.table_create_property_name.insert(0, self.table_create_tree.item(selected[0])["values"][0])
            self.table_create_property_type.insert(0, self.table_create_tree.item(selected[0])["values"][1])
            self.table_create_property_unique.set(self.table_create_tree.item(selected[0])["values"][2])
            self.table_create_property_not_null.set(self.table_create_tree.item(selected[0])["values"][3])
            self.table_create_property_primary_key.set(self.table_create_tree.item(selected[0])["values"][4])
            self.table_create_property_auto_increment.set(self.table_create_tree.item(selected[0])["values"][5])
            self.table_create_tree.delete(selected[0])

    def handle_table_create_save(self):
        # Get the data from the treeview widget and save it to the database
        if self.table_create_name.get() == "":
            messagebox.showerror("Error", "Please fill in the name of the table.")
            return
        columns = []
        for row in self.table_create_tree.get_children():
            columns.append(self.table_create_tree.item(row)["values"])
        column_string = ""
        for column in columns:
            column_string += column[0] + " " + column[1]
            if column[2] != 0:
                column_string += " NOT NULL"
            if column[3] != 0 and column[4] == 0:
                column_string += " UNIQUE"
            if column[4] != 0:
                column_string += " PRIMARY KEY"
            if column[5] != 0:
                column_string += " AUTO_INCREMENT"
            if column != columns[-1]:
                column_string += ",\n"
        if create_table(self.database.get(), self.table_create_name.get(), column_string):
            self.table_create_window.destroy()
            self.table_options = get_table_options(self.database.get())
            self.set_new_option_menu("table")

    def handle_table_record_create(self):
        # Show a window to create a new record with all the columns of the currently selected table
        self.table_record_create_window = Toplevel(self.root)
        self.table_record_create_window.title("Create record")
        self.table_record_create_window.resizable(False, False)
        self.table_record_create_window.grab_set()
        self.table_record_create_window.focus_set()

        self.table_record_create_frame = Frame(self.table_record_create_window)
        self.table_record_create_frame.pack()

        # Create inputs for each column of treeview widget
        self.table_record_create_inputs = []
        for column in self.table_data_display["columns"]:
            Label(self.table_record_create_frame, text=column).grid(row=0, column=self.table_data_display["columns"].index(column))
            self.table_record_create_inputs.append(Entry(self.table_record_create_frame))
            self.table_record_create_inputs[-1].grid(row=1, column=self.table_data_display["columns"].index(column))

        # Create a button to save the record
        Button(self.table_record_create_frame, text="Save", command=self.handle_table_record_create_save).grid(row=2, column=0, columnspan=2)

    def handle_table_record_create_save(self):
        # Save the record to the database
        values = []
        for record_entry in self.table_record_create_inputs:
            if record_entry.get() == "":
                values.append("")
            else:
                values.append(record_entry.get())
        if insert_record(self.database.get(), self.table.get(), self.table_data_display["columns"], values):
            self.table_record_create_window.destroy()
            # Refresh the table data by simulating a change in the table option menu
            self.table.set(self.table.get())
        else:
            messagebox.showerror("Error", "The record could not be created.")

    def handle_table_record_update(self):
        pass

    def handle_table_record_delete(self):
        # Get selected record from the table treeview widget
        selected = self.table_data_display.selection()
        if len(selected) > 0:
            # Get the values of the selected record
            values = self.table_data_display.item(selected[0])["values"]
            # Delete the record from the database
            if delete_record(self.database.get(), self.table.get(), self.table_data_display["columns"], values):
                # Refresh the table data by simulating a change in the table option menu
                self.table.set(self.table.get())
            else:
                messagebox.showerror("Error", "The record could not be deleted.")

    def run(self):
        self.root.mainloop()
