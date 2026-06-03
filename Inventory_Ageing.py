import mysql.connector
import pandas as pd
from datetime import datetime

# CONNECT MYSQL
mydb=mysql.connector.connect(
    host="127.0.0.1",
    port=3307,
    user="root",
    password="your_password_here",
    database="inventory_db"
)
print("Connected")

# READ TABLE
df=pd.read_sql("SELECT * FROM stock",mydb)
print(df)

# COVERT DATE
df["purchase_date"]=pd.to_datetime(df["purchase_date"])

# TODAY DATE
today=pd.Timestamp.today()

# CALCULATE DAYS
df["days_in_stock"]=(today-df["purchase_date"]).dt.days


status=[]

for i in df["days_in_stock"]:
    if i>60:
        status.append("Dead Stock")
    else:
        status.append("Good")

df["Status"]=status

print(df)


import matplotlib.pyplot as plt

plt.bar(df["product_name"], df["days_in_stock"])

plt.xlabel("Products")
plt.ylabel("Days in Stock")
plt.title("Inventory Ageing")

plt.show()




