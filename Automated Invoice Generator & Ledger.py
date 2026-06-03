# Tkinter Form
#       ↓
# Enter Customer + Item + Price
#       ↓
# Python calculates GST
#       ↓
# Save in MySQL
#       ↓
# Generate PDF Invoice

from tkinter import *
import mysql.connector
from tkinter import ttk
from reportlab.pdfgen import canvas


mydb = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,
    user="root",
    password="Kingdom1914!",
    database="invoice_db"
)

print("Connected Successfully")

mycursor = mydb.cursor()


# CREATE TKINTER WINDOW
root=Tk()
root.title("Invoice Generator")
root.geometry("400x400")


Label(root,text="Customer Name").pack()
customer_entry=Entry(root)
customer_entry.pack()


Label(root, text="Item").pack()
item_entry=Entry(root)
item_entry.pack()

Label(root, text="Price").pack()
price_entry=Entry(root)
price_entry.pack()

# CALCULATE GST
def generate_invoice():
    customer=customer_entry.get()
    item=item_entry.get()
    price=float(price_entry.get())

    gst=price*0.18

    total=gst+price
    #     SAVE INTO MYSQL
    sql="""INSERT INTO invoices
    (CUSTOMER_NAME,ITEM,PRICE,GST,TOTAL) VALUES
    (%s,%s,%s,%s,%s)"""

    values=(customer,item,price,gst,total)
    mycursor.execute(sql,values)
    mydb.commit()
    print("Invoice Generated")

    pdf = canvas.Canvas("invoice.pdf")

    pdf.drawString(100, 750, "INVOICE")
    pdf.drawString(100, 700, f"Customer: {customer}")
    pdf.drawString(100, 680, f"Item: {item}")
    pdf.drawString(100, 660, f"Price: {price}")
    pdf.drawString(100, 640, f"GST: {gst}")
    pdf.drawString(100, 620, f"Total: {total}")

    pdf.save()



Button(root,text="Generate Invoice",command=generate_invoice).pack()


root.mainloop()
