import pandas as pd
import numpy as np

df = pd.read_csv("accounts.csv")
df[['EmployeeID', 'BillType', 'Month', 'FileName']] = df['File_Name'].str.split('*', expand=True)

max_mobile_charges = 500
max_internet_charges = 1000
max_fuel_bike = 1000
max_fuel_car = 3000


def agg_sum_per_employee(data):
    grouped_emp = data.groupby(['EmployeeID', 'BillType'], as_index=False).sum()

    grouped_emp['Remarks'] = ""

    grouped_emp.loc[(grouped_emp['Ext_invoice_amount'] > max_mobile_charges) &
                    (grouped_emp['BillType'] == "mobile"),
                    'Remarks'] = "Amount 500 has been reimbursed"

    grouped_emp.loc[(grouped_emp['Ext_invoice_amount'] > max_internet_charges) &
                    (grouped_emp['BillType'] == "internet"),
                    'Remarks'] = "Amount 1000 has been reimbursed"

    grouped_emp.loc[(grouped_emp['Ext_invoice_amount'] > max_fuel_bike) &
                    (grouped_emp['BillType'] == "bike"),
                    'Remarks'] = "Amount 1000 has been reimbursed"

    grouped_emp.loc[(grouped_emp['Ext_invoice_amount'] > max_fuel_car) &
                    (grouped_emp['BillType'] == "car"),
                    'Remarks'] = "Amount 3000 has been reimbursed"

    return grouped_emp


res = agg_sum_per_employee(df)
print("2nd Sheet: \n", res)

df_user = pd.read_csv("accounts_user.csv")


def is_matched(data):
    new_df = df.merge(df_user, on="File_Name", how="inner")
    new_df['matched'] = ""

    new_df.loc[(new_df['Ext_invoice_number'] != new_df['Invoice_number']) |
               (new_df['Ext_invoice_date'] != new_df['Invoice_date']) |
               (new_df['Ext_invoice_amount'] != new_df['Invoice_amount']),
               'matched'] = "Not matched"

    new_df.loc[(new_df['Ext_invoice_amount'] > max_mobile_charges) &
               (new_df['BillType'] == "mobile"),
               'matched'] = "Not matched"

    new_df.loc[(new_df['Ext_invoice_amount'] > max_internet_charges) &
               (new_df['BillType'] == "internet"),
               'matched'] = "Not matched"

    new_df.loc[(new_df['Ext_invoice_amount'] > max_fuel_bike) &
               (new_df['BillType'] == "bike"),
               'matched'] = "Not matched"

    new_df.loc[(new_df['Ext_invoice_amount'] > max_fuel_car) &
               (new_df['BillType'] == "car"),
               'matched'] = "Not matched"

    return new_df


res_1 = is_matched(df)

print("3rd Sheet: \n", res_1)

with pd.ExcelWriter('output.xlsx') as writer:
  res.to_excel(writer, sheet_name='Total Sum')
  res_1.to_excel(writer, sheet_name='Individual files')