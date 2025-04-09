import psycopg2
import csv
def connect_to_db():
    return psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="localhost",
        port="5432"
    )
def create_table():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            phone_number VARCHAR(15) UNIQUE NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
def insert_data_from_csv(csv_filename):
    conn = connect_to_db()
    cur = conn.cursor()

    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            first_name = row['first_name']
            last_name = row['last_name']
            phone_number = row['phone_number']

            cur.execute("""
                INSERT INTO phonebook (first_name, last_name, phone_number)
                VALUES (%s, %s, %s)
            """, (first_name, last_name, phone_number))

    conn.commit()
    cur.close()
    conn.close()
    print("Data inserted from CSV.")
def insert_data_from_console():
    conn = connect_to_db()
    cur = conn.cursor()

    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone_number = input("Enter phone number: ")

    cur.execute("""
        INSERT INTO phonebook (first_name, last_name, phone_number)
        VALUES (%s, %s, %s)
    """, (first_name, last_name, phone_number))

    conn.commit()
    cur.close()
    conn.close()
    print("User added successfully.")
def update_data():
    conn = connect_to_db()
    cur = conn.cursor()

    phone_number = input("Enter the phone number of the user to update: ")
    new_first_name = input("Enter the new first name: ")
    new_phone_number = input("Enter the new phone number: ")

    cur.execute("""
        UPDATE phonebook
        SET first_name = %s, phone_number = %s
        WHERE phone_number = %s
    """, (new_first_name, new_phone_number, phone_number))

    conn.commit()
    cur.close()
    conn.close()
    print("User data updated successfully.")
def query_by_phone():
    conn = connect_to_db()
    cur = conn.cursor()

    phone_number = input("Enter the phone number to search for: ")

    cur.execute("""
        SELECT * FROM phonebook WHERE phone_number = %s
    """, (phone_number,))

    user = cur.fetchone()
    if user:
        print(f"User found: {user}")
    else:
        print("User not found.")

    cur.close()
    conn.close()
def query_by_name():
    conn = connect_to_db()
    cur = conn.cursor()

    name = input("Enter the first or last name to search for: ")

    cur.execute("""
        SELECT * FROM phonebook WHERE first_name = %s OR last_name = %s
    """, (name, name))

    users = cur.fetchall()
    if users:
        for user in users:
            print(f"User: {user}")
    else:
        print("No users found.")

    cur.close()
    conn.close()
def delete_by_phone():
    conn = connect_to_db()
    cur = conn.cursor()

    phone_number = input("Enter the phone number of the user to delete: ")

    cur.execute("""
        DELETE FROM phonebook WHERE phone_number = %s
    """, (phone_number,))

    conn.commit()
    cur.close()
    conn.close()
    print("User deleted successfully.")
def delete_by_name():
    conn = connect_to_db()
    cur = conn.cursor()

    first_name = input("Enter the first name of the user to delete: ")

    cur.execute("""
        DELETE FROM phonebook WHERE first_name = %s
    """, (first_name,))

    conn.commit()
    cur.close()
    conn.close()
    print("User deleted successfully.")
def main():
    while True:
        print("\nPhoneBook System")
        print("1. Create PhoneBook Table")
        print("2. Insert data from CSV")
        print("3. Insert data from Console")
        print("4. Update data")
        print("5. Query by phone number")
        print("6. Query by name")
        print("7. Delete by phone number")
        print("8. Delete by name")
        print("9. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            create_table()
        elif choice == '2':
            csv_filename = input("Enter CSV file name: ")
            insert_data_from_csv(csv_filename)
        elif choice == '3':
            insert_data_from_console()
        elif choice == '4':
            update_data()
        elif choice == '5':
            query_by_phone()
        elif choice == '6':
            query_by_name()
        elif choice == '7':
            delete_by_phone()
        elif choice == '8':
            delete_by_name()
        elif choice == '9':
            print("Exiting PhoneBook System.")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()
