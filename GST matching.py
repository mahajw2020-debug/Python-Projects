import pandas as pd

# Step 1: read files
purchase = pd.read_excel(r"C:\Users\acer\OneDrive\Projects\purchase_large.xlsx")
gstr2b = pd.read_excel(r"C:\Users\acer\OneDrive\Projects\gstr2b_large.xlsx")

# Step 2: Compare using invoice no
merged=pd.merge(purchase,gstr2b,on="Invoice No",how="outer",indicator=True)

# Step3: Check results
print(merged)

# Missing
missing=merged[merged["_merge"]!="both"]
print(missing)

# Missmatch
missmatch=merged[
    (merged["_merge"]=="both") &
    (merged["GST Amount_x"]!=merged["GST Amount_y"])
]

print(missmatch)