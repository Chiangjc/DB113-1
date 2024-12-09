# import re
# import math
# import numpy as np
# from faker import Faker
# from datetime import datetime
# import random
# import pandas as pd
# from dateutil.relativedelta import relativedelta
# import string
# import csv

# from sympy import isprime

# fake = Faker()
# file_id = 'f'

# df = pd.read_csv(f"supplier_{file_id}.csv")
# s_id_list = df['s_id'].tolist()

# print(len(s_id_list))

# df = pd.read_csv(f"employee_{file_id}.csv")
# e_id_list = df[df['role'] == 'Admin']['e_id'].tolist()

# print(len(e_id_list))

# rate = []
# count = 0

# for i in range(28):
#     for j in range(len(s_id_list)):
#         count += 1
#         if isprime(count) == True:
#             continue
#         else:
#             o = random.randint(50,100)
#             q = random.randint(50,100)
#             a = random.randint(50,100)
#             final = o*0.3 + q*0.65 + a*0.05
#             row = {
#                 "s_id": s_id_list[j],
#                 "year": 1997+i,
#                 "on_time": o,
#                 "quality": q,
#                 "after-sales service": a,
#                 "final score": round(final, 2),
#                 "e_id": random.choice(e_id_list)
#             }
#             rate.append(row)
            
# data_rate = pd.DataFrame(rate)

# # 將資料寫入 CSV 檔案
# data_rate.to_csv("rate_f.csv", index=False)

# print(len(rate))

from datetime import datetime, timedelta
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

df = pd.read_csv(f"data_ff/supplier_{file_id}.csv")
s_id_list = df['s_id'].tolist()
print(len(s_id_list))


# 讀取員工資料
df = pd.read_csv(f"data_ff/employee_{file_id}.csv")
df['start_date'] = pd.to_datetime(df['start_date'], format='%Y-%m-%d', errors='coerce')
df['leave_date'] = pd.to_datetime(df['leave_date'], format='%Y-%m-%d', errors='coerce')

# 只選擇 admin 員工
admin_df = df[df['role'] == 'Admin']

# 定義檢查員工是否在某年份在職的函數
def is_employee_active_in_year(employee, year):
    start_year = employee['start_date'].year
    leave_year = employee['leave_date'].year if pd.notna(employee['leave_date']) else datetime.now().year
    return start_year <= year <= leave_year

# 創建一個儲存每年在職 admin 的字典
active_admins_per_year = {}
for year in range(1997, 2025):  # 假設年份範圍從 1997 到 2024
    active_admins = admin_df[admin_df.apply(lambda x: is_employee_active_in_year(x, year), axis=1)]
    active_admins_per_year[year] = active_admins['e_id'].tolist()

# 處理 rate 資料生成
rate = []
count = 0

# 隨機生成 rate 資料
for i in range(28):
    for j in range(len(s_id_list)):
        count += 1
        if isprime(count):
            continue
        else:
            o = random.randint(50, 100)
            q = random.randint(50, 100)
            a = random.randint(50, 100)
            final = o * 0.3 + q * 0.65 + a * 0.05
            
            year = 1997 + i
            active_admins = active_admins_per_year.get(year, [])
            if not active_admins:
                continue  # 如果當年沒有在職員工，跳過

            # 隨機選擇一個 admin 員工
            e_id = random.choice(active_admins)

            row = {
                "s_id": s_id_list[j],
                "year": year,
                "on_time": o,
                "quality": q,
                "after-sales service": a,
                "final score": round(final, 2),
                "e_id": e_id
            }
            rate.append(row)

# 儲存為 DataFrame 並寫入 CSV 檔案
data_rate = pd.DataFrame(rate)

folder_path = 'data_ff'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 儲存 CSV 檔案到資料夾中
file_path = os.path.join(folder_path, "rate_f.csv")
data_rate.to_csv(file_path, index=False)

print(len(rate))


