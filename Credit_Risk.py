from itertools import groupby

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

from Small_shop import grouped

mydb=mysql.connector.connect(
    host='127.0.0.1',
    port=3307,
    user="root",
    password="your_password_here",
    database='creditrisk_db'
)

print("Connected to database")

df=pd.read_sql("Select * from customer",mydb)


risk=[]

for days in df["payment_days"]:
    if days<=10:
        risk.append("Low Risk")
    elif days<=30:
        risk.append('Medium Risk')
    else:
        risk.append("High Risk")

df["Risk_level"]=risk
print(df)

group=df.groupby("Risk_level")["amount_due"].sum()
print(group)

plt.bar(df["Risk_level"], df["amount_due"])

plt.title("Total money stock by Risk Level")
plt.xlabel("Risk Level")
plt.ylabel("Amount Due")

plt.show()