import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import mysql.connector as Sql


mycon = Sql.connect(
    host="localhost",
    user="root",
    password="Kingdom1914!",
    database="hubnet"
)
mycur = mycon.cursor()

special_symbols = ['$', '@', '#', '%']


class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CANARA BANK")
        self.username = None
        self.create_login_ui()

    def clear_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_ui(self):
        self.clear_ui()
        tk.Label(self.root, text="--- Login ---", font=("Arial", 20)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.login_user = tk.Entry(self.root)
        self.login_user.pack()

        tk.Label(self.root, text="Password").pack()
        self.login_pass = tk.Entry(self.root, show="*")
        self.login_pass.pack()

        tk.Button(self.root, text="Login", command=self.sign_in).pack(pady=5)
        tk.Button(self.root, text="Sign Up", command=self.create_signup_ui).pack(pady=10)

    def sign_in(self):
        username = self.login_user.get()
        password = self.login_pass.get()

        operation = "SELECT * FROM bank WHERE UserName = %s AND Password = %s"
        params = (username, password)
        mycur.execute(operation, params)
        user = mycur.fetchone()

        if user:
            self.username = username
            self.create_dashboard_ui()
        else:
            messagebox.showerror(title="Login Failed", message="Invalid username or password.")

    def create_signup_ui(self):
        self.clear_ui()
        tk.Label(self.root, text="--- Sign Up ---", font=("Arial", 18)).pack(pady=5)

        tk.Label(self.root, text="Full Name").pack()
        self.sign_name = tk.Entry(self.root)
        self.sign_name.pack()

        tk.Label(self.root, text="Username").pack()
        self.sign_user = tk.Entry(self.root)
        self.sign_user.pack()

        tk.Label(self.root, text="Password").pack()
        self.sign_pass = tk.Entry(self.root, show="*")
        self.sign_pass.pack()

        tk.Label(self.root, text="DOB (YYYY-MM-DD)").pack()
        self.sign_dob = tk.Entry(self.root)
        self.sign_dob.pack()

        tk.Label(self.root, text="Address").pack()
        self.sign_address = tk.Entry(self.root)
        self.sign_address.pack()

        tk.Label(self.root, text="Mobile Number").pack()
        self.sign_mobile = tk.Entry(self.root)
        self.sign_mobile.pack()

        tk.Label(self.root, text="Aadhaar No").pack()
        self.sign_aadhaar = tk.Entry(self.root)
        self.sign_aadhaar.pack()

        tk.Button(self.root, text="Submit Registration", command=self.signUp_submit).pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.create_login_ui).pack()

    def signUp_submit(self):
        name = self.sign_name.get()
        username = self.sign_user.get()
        password = self.sign_pass.get()
        dob = self.sign_dob.get()
        address = self.sign_address.get()
        mobile = self.sign_mobile.get()
        aadhaar = self.sign_aadhaar.get()
        balance = 0.00

        if (len(name) == 0 or len(username) == 0 or len(password) == 0 or
                len(dob) == 0 or len(address) == 0 or len(mobile) == 0 or len(aadhaar) == 0):
            messagebox.showerror(title="Error", message="All fields are required!")
            return

        try:
            sql = """INSERT INTO bank (Name, UserName, Password, DOB, Address, Mobile_Number, Aadhaar_no, Balance) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            mycur.execute(sql, (name, username, password, dob, address, mobile, aadhaar, balance))
            mycon.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            self.create_login_ui()
        except Sql.Error as err:
            messagebox.showerror("Error", f"Failed to create account: {err}")

    def create_dashboard_ui(self):
        self.clear_ui()
        tk.Label(self.root, text=f"Welcome {self.username}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="View Profile", command=self.view_profile).pack(pady=5)
        tk.Button(self.root, text="Deposit", command=self.deposit_ui).pack(pady=5)
        tk.Button(self.root, text="Withdraw", command=self.withdraw_ui).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.create_login_ui).pack(pady=20)

    def view_profile(self):
        operation = "SELECT Name, UserName, Address, Mobile_Number, Aadhaar_no, Balance FROM bank WHERE UserName = %s"
        params = (self.username,)
        mycur.execute(operation, params)
        user = mycur.fetchone()

        profile = f"Name : {user[0]}\nUsername : {user[1]}\nAddress : {user[2]}\nMobile : {user[3]}\nAadhaar : {user[4]}\nBalance : ₹{user[5]}"
        messagebox.showinfo(title="Profile", message=profile)

    # --- Completed Deposit UI and Processing ---
    def deposit_ui(self):
        self.clear_ui()
        tk.Label(self.root, text="--- Deposit Money ---", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.root, text="Enter Amount to Deposit:").pack(pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(pady=5)

        tk.Button(self.root, text="Confirm Deposit", command=self.process_deposit).pack(pady=10)
        tk.Button(self.root, text="Back to Dashboard", command=self.create_dashboard_ui).pack(pady=5)

    def process_deposit(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than zero.")
                return

            # Update customer balance
            mycur.execute("UPDATE bank SET Balance = Balance + %s WHERE UserName = %s", (amount, self.username))
            # Log inside transaction table
            mycur.execute("INSERT INTO Transaction (Credited, Debited, UserName) VALUES (%s, 0.00, %s)",
                          (amount, self.username))
            mycon.commit()

            messagebox.showinfo("Success", f"₹{amount} deposited successfully!")
            self.create_dashboard_ui()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric amount.")

    # --- Completed Withdraw UI and Processing ---
    def withdraw_ui(self):
        self.clear_ui()
        tk.Label(self.root, text="--- Withdraw Money ---", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.root, text="Enter Amount to Withdraw:").pack(pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(pady=5)

        tk.Button(self.root, text="Confirm Withdrawal", command=self.process_withdrawal).pack(pady=10)
        tk.Button(self.root, text="Back to Dashboard", command=self.create_dashboard_ui).pack(pady=5)

    def process_withdrawal(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than zero.")
                return

            # Check current balance first
            mycur.execute("SELECT Balance FROM bank WHERE UserName = %s", (self.username,))
            current_balance = mycur.fetchone()[0]

            if amount > current_balance:
                messagebox.showerror("Error", "Insufficient balance available.")
                return

            # Deduct balance
            mycur.execute("UPDATE bank SET Balance = Balance - %s WHERE UserName = %s", (amount, self.username))
            # Log inside transaction table
            mycur.execute("INSERT INTO Transaction (Credited, Debited, UserName) VALUES (0.00, %s, %s)",
                          (amount, self.username))
            mycon.commit()

            messagebox.showinfo("Success", f"₹{amount} withdrawn successfully!")
            self.create_dashboard_ui()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric amount.")


if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("450x550")
    app = BankApp(window)
    window.mainloop()