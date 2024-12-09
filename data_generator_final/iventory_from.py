import re
import math
import numpy as np
from faker import Faker
from datetime import datetime
import random
import pandas as pd
from dateutil.relativedelta import relativedelta
import string
import csv
import os

from sympy import isprime

fake = Faker()
file_id = 'f'

# plane_num 清單
plane_num = [
    "787-1", "787-2", "787-3", "787-4", "787-5", "787-6", "787-7", "787-8", "787-9", "787-10",
    "777-1", "777-2", "777-3", "777-4", "777-5", "777-6", "777-7",
    "767-1", "767-2", "767-3", "767-4", "767-5", "767-6", "767-7", "767-8", "767-9", "767-10", "767-11", "767-12", "767-13",
    "757-1", "757-2", "757-3", "757-4", "757-5", "757-6", "757-7", "757-8", "757-9", "757-10",
    "747-1", "747-2", "747-3",
    "737-1", "737-2", "737-3", "737-4", "737-5"
]
df = pd.read_csv(f"data_ff/inventory_{file_id}.csv")

# 篩選出 inv_name 不在 plane_num 中的 inv_id
inv_id_list = df[~df['inv_name'].isin(plane_num)]['inv_id'].tolist()
plane_inv_list = df[df['inv_name'].isin(plane_num)]['inv_id'].tolist()

print(len(inv_id_list))
print(len(plane_inv_list))

# From Supplier
df = pd.read_csv(f"supplier_{file_id}.csv")
s_id_list = df['s_id'].tolist()

print(len(s_id_list))

# From Factory
df = pd.read_csv(f"data_ff/factory_{file_id}.csv")
f_id_list = df['f_id'].tolist()
f_usa_list = df[df['f_country'].isin(["USA"])]['f_id'].tolist()

print(len(f_id_list))

inv_length = len(inv_id_list)


from_supplier = []

from_factory = []

plane_num = ["787-1", "787-2", "787-3", "787-4", "787-5", "787-6", "787-7", "787-8", "787-9", "787-10",
             "777-1", "777-2", "777-3", "777-4", "777-5", "777-6", "777-7",
             "767-1", "767-2", "767-3", "767-4", "767-5", "767-6", "767-7", "767-8", "767-9", "767-10", "767-11", "767-12", "767-13",
             "757-1", "757-2", "757-3", "757-4", "757-5", "757-6", "757-7", "757-8", "757-9", "757-10",
             "747-1", "747-2", "747-3",
             "737-1", "737-2", "737-3", "737-4", "737-5"
             ]
count = 0
for i in range(inv_length):
    count += 1
    for j in range(28):
        f_1 = f_id_list[random.randint(0, 149)]
        f_2 = f_id_list[random.randint(0, 149)]
        s_1 = s_id_list[random.randint(0, 2999)]
        s_2 = s_id_list[random.randint(0, 2999)]
       
        if count % 10 == 0 or count % 1001 == 5:
            row2 = {
                "inv_id": inv_id_list[i],
                "f_id": random.choices([f_1, f_2], [0.95, 0.05])[0],
                "year": 1997+j
            }
            from_factory.append(row2)
        else:
            row1 = {
                "inv_id": inv_id_list[i],
                "s_id": random.choices([s_1, s_2], [0.95, 0.05])[0],
                "year": 1997+j
            }
            from_supplier.append(row1)
                
for i in range(48):
    row2 = {
        "inv_id": inv_id_list[i],
        "f_id": f_usa_list[random.randint(5, 8)],
        "year": 1997+j
    }
    from_factory.append(row2)

data_from_supplier = pd.DataFrame(from_supplier)

data_from_factory = pd.DataFrame(from_factory)

print(len(from_supplier))

print(len(from_factory))

folder_path = 'data_ff'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 儲存 CSV 檔案到資料夾中
file_path = os.path.join(folder_path, "inventory_from_supplier_f.csv")
data_from_supplier.to_csv(file_path, index=False)

file_path = os.path.join(folder_path, "inventory_from_factory_f.csv")
data_from_factory.to_csv(file_path, index=False)

