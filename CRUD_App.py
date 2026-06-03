import mysql.connector
from tabulate import tabulate

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Kingdom1914!'
)
cursor = conn.cursor()

cursor.execute("create database if not exists studentdb")
cursor.execute("use studentdb")

cursor.execute("""
    create table if not exists student (
        id int primary key auto_increment,
        name varchar(100),
        email varchar(100)
    )
""")


def createStudent():
    name = input("enter your name: ")
    email = input("enter your email: ")
    sql = "insert into student (name, email) values (%s, %s)"
    values = (name, email)
    cursor.execute(sql, values)
    conn.commit()  # auto save
    print("data added successfully")


def read_alldata():
    cursor.execute("select * from student")
    column = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    # print as table
    print(tabulate(rows, headers=column, tablefmt="pretty"))


def updateStudent():
    print("which one you want to update \n1. name \n2. email")
    option = int(input("Enter your choice: "))
    id = int(input("Enter your id: "))

    if option == 1:
        name = input("enter your updated name: ")
        sql = "update student set name = %s where id = %s"
        values = (name, id)
    elif option == 2:
        email = input("enter your email: ")
        sql = "update student set email = %s where id = %s"
        values = (email, id)

    cursor.execute(sql, values)
    conn.commit()  # auto save
    print("updated successfully")


def deleteStudent():
    id = int(input("which id you went to Delete: "))
    sql = "delete from student where id = %s"
    cursor.execute(sql, (id,))
    conn.commit()
    print("data deleted successfully")



# --- Main Program Menu Loop ---

data = 'y'
while data == 'y':
    print("\n" + "=" * 50)
    print("****** STUDENT MANAGEMENT SYSTEM ******".center(50))
    print("=" * 50)
    print("  1. Create Student")
    print("  2. Read Student")
    print("  3. Update Student")
    print("  4. Delete Student")
    print("=" * 50)

    choice = int(input("Enter your choice: "))
    print("-" * 50)

    if choice == 1:
        createStudent()
    elif choice == 2:
        read_alldata()
    elif choice == 3:
        updateStudent()
    elif choice == 4:
        deleteStudent()
    else:
        print("Please choose a valid option from the menu")

    print("-" * 50)
    data = input("Do you want to continue yes (y) no (n): ").lower()

cursor.close()
conn.close()