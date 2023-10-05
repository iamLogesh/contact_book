import mysql.connector
import streamlit as st

# Function to create a table for storing contacts
def create_contact_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS contacts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        phone_number VARCHAR(20)
    )
    """
    cursor.execute(create_table_query)
    mydb.commit()
    st.write("Contact table created successfully!")

# Function to create a new contact
def create_contact(cursor):
    name = st.text_input("Enter the contact's name:")
    phone_number = st.text_input("Enter the contact's phone number:")
    if st.button("Add Contact"):
        insert_query = "INSERT INTO contacts (name, phone_number) VALUES (%s, %s)"
        cursor.execute(insert_query, (name, phone_number))
        mydb.commit()
        st.write("Contact added successfully!")

# Function to view all contacts
def view_contacts(cursor):
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    if not contacts:
        st.write("No contacts found.")
    else:
        st.write("Contacts:")
        for contact in contacts:
            st.write(f"Name: {contact[1]}, Phone Number: {contact[2]}")

# Function to delete a contact
def delete_contact(cursor):
    phone_number = st.text_input("Enter the phone number of the contact to delete:")
    if st.button("Delete Contact"):
        delete_query = "DELETE FROM contacts WHERE phone_number = %s"
        cursor.execute(delete_query, (phone_number,))
        mydb.commit()
        if cursor.rowcount > 0:
            st.write("Contact deleted successfully!")
        else:
            st.write("Contact not found.")

# Function to search for a contact by name or phone number
def search_contact(cursor):
    keyword = st.text_input("Enter the name or phone number to search for:")
    if st.button("Search"):
        search_query = "SELECT * FROM contacts WHERE name LIKE %s OR phone_number LIKE %s"
        cursor.execute(search_query, (f'%{keyword}%', f'%{keyword}%'))
        contacts = cursor.fetchall()
        if not contacts:
            st.write("No matching contacts found.")
        else:
            st.write("Matching Contacts:")
            for contact in contacts:
                st.write(f"Name: {contact[1]}, Phone Number: {contact[2]}")

# Establish a connection to the MySQL database
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="pybase"
)

cursor = mydb.cursor()

# Call the function to create the contact table
create_contact_table(cursor)

# Streamlit app
st.title("Telephone Directory")

option = st.sidebar.selectbox("Select an option:", ["Create New Contact", "View Contacts", "Delete Contact", "Search Contact"])

if option == "Create New Contact":
    create_contact(cursor)
elif option == "View Contacts":
    view_contacts(cursor)
elif option == "Delete Contact":
    delete_contact(cursor)
elif option == "Search Contact":
    search_contact(cursor)

# Close the cursor and the database connection
cursor.close()
mydb.close()
