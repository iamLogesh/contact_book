import mysql.connector

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
    print("Contact table created successfully!")

# Function to create a new contact
def create_contact(cursor):
    name = input("Enter the contact's name: ")
    phone_number = input("Enter the contact's phone number: ")
    insert_query = "INSERT INTO contacts (name, phone_number) VALUES (%s, %s)"
    cursor.execute(insert_query, (name, phone_number))
    mydb.commit()
    print("Contact added successfully!")

# Function to view all contacts
def view_contacts(cursor):
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    if not contacts:
        print("No contacts found.")
    else:
        print("Contacts:")
        for contact in contacts:
            print(f"Name: {contact[1]}, Phone Number: {contact[2]}")

# Function to delete a contact
def delete_contact(cursor):
    phone_number = input("Enter the phone number of the contact to delete: ")
    delete_query = "DELETE FROM contacts WHERE phone_number = %s"
    cursor.execute(delete_query, (phone_number,))
    mydb.commit()
    if cursor.rowcount > 0:
        print("Contact deleted successfully!")
    else:
        print("Contact not found.")

# Function to search for a contact by name or phone number
def search_contact(cursor):
    keyword = input("Enter the name or phone number to search for: ")
    search_query = "SELECT * FROM contacts WHERE name LIKE %s OR phone_number LIKE %s"
    cursor.execute(search_query, (f'%{keyword}%', f'%{keyword}%'))
    contacts = cursor.fetchall()
    if not contacts:
        print("No matching contacts found.")
    else:
        print("Matching Contacts:")
        for contact in contacts:
            print(f"Name: {contact[1]}, Phone Number: {contact[2]}")

# Establish a connection to the MySQL database
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="pybase"
)

if mydb.is_connected():
    print("Connected to the MySQL database.")

cursor = mydb.cursor()

# Call the function to create the contact table
create_contact_table(cursor)

# Text-based menu
while True:
    print("\nOptions:")
    print("1. Create Contact")
    print("2. View Contacts")
    print("3. Delete Contact")
    print("4. Search Contact")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        create_contact(cursor)
    elif choice == "2":
        view_contacts(cursor)
    elif choice == "3":
        delete_contact(cursor)
    elif choice == "4":
        search_contact(cursor)
    elif choice == "5":
        break
    else:
        print("Invalid choice. Please select a valid option.")

# Close the cursor and the database connection
cursor.close()
mydb.close()
