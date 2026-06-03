from tkinter.constants import INSERT

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from fontTools.voltLib.voltToFea import TABLES

# 1. Connect to Mysql
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kingdom1914!",
)

# 2. Create a cursor
mycursor = mydb.cursor()

# 3. Now you can run the SQL command inside quotes
mycursor.execute("CREATE DATABASE IF NOT EXISTS Shop_DB")
mycursor.execute("USE Shop_DB")
print("Database created")

mycursor.execute("""
Create TABLE if not exists Transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    type VARCHAR(50),
    category VARCHAR(50),
    amount DECIMAL(20,2)
)    
""")
print("Table created")


mycursor.execute("""
INSERT INTO TRANSACTION (date,type,category,amount) VALUES
('2026-04-01', 'Income', 'Sales', 5000),
('2026-04-01', 'Expense', 'Rent', 2000),
('2026-04-02', 'Expense', 'Salary', 1500),
('2026-04-03', 'Income', 'Sales', 6000),
('2026-04-04', 'Expense', 'Electricity', 800),
('2026-06-28', 'Income', 'Sales', 42000)

""")

df=pd.read_sql("SELECT * FROM Transaction",mydb)
print(df)


income=df[df["type"]=="Income"]
expense=df[df["type"]=="Expense"]

# Profit= Income - Expense
profit= income["amount"].sum()-expense["amount"].sum()
print("Net profit:",profit)



df["date"]=pd.to_datetime(df["date"])
df["month"]=df["date"].dt.month

expense=df[df["type"]=="Expense"]

grouped=expense.groupby(["month","category"])["amount"].sum().reset_index()
grouped=grouped.sort_values(["month","amount"],ascending=[True,False])

top5=grouped.groupby("month").head(5)
print("Top 5 expenses by month:")
print(top5)

# Pie chart
plt.subplot(1,2,1)
expense_data=expense.groupby("category")["amount"].sum()

plt.pie(expense_data,labels=expense_data.index,autopct='%1.1f%%')
plt.title("Expense Breakdown")

# Line graph (Sales growth)
plt.subplot(1,2,2)
income=df[df["type"]=="Income"]
df["date"]=pd.to_datetime(df["date"])
df["month"]=df["date"].dt.month

plt.plot(income["month"],income["amount"],marker='o',color='green',linestyle='-')
plt.title("Sales Growth Trend")
plt.xlabel("Month")
plt.ylabel("Income")
plt.tight_layout()
plt.show()