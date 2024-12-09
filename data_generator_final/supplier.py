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

fake = Faker()

# 設定生成數據的標題
headers = ['s_id', 's_name', 's_country', 's_address', 's_phone', 'super_name']

major_country_code_map = {
    'USA': '+1',          # 波音總部及主要製造基地
    'Canada': '+1',       # 鄰近美國的重要供應商
    'Mexico': '+52',      # 供應鏈延伸國
    'Japan': '+81',       # 主要航空零件供應商
    'South Korea': '+82', # 供應鏈合作夥伴
    'Australia': '+61',   # 航太工程合作
    'United Kingdom': '+44', # 技術與零件供應商
    'Germany': '+49',     # 高科技零件供應
    'France': '+33',      # 與歐洲航太產業合作
    'Italy': '+39',       # 輔助零件生產
    'China': '+86',       # 波音飛機組裝工廠
    'Singapore': '+65',   # 亞太區維修與零件供應中心
    'Malaysia': '+60',    # 部分零件製造
    'India': '+91',       # 軟體開發與設計外包
    'Brazil': '+55',      # 航空工業合作
    'Russia': '+7',       # 航空鋁供應與技術合作
    'Poland': '+48',      # 零件製造基地
    'Czech Republic': '+420', # 輔助零件供應商
}

minor_country_code_map = {
    'Argentina': '+54',
    'Chile': '+56',
    'Colombia': '+57',
    'Peru': '+51',
    'Venezuela': '+58',
    'South Africa': '+27',
    'Nigeria': '+234',
    'Egypt': '+20',
    'Turkey': '+90',
    'Saudi Arabia': '+966',
    'United Arab Emirates': '+971',
    'Israel': '+972',
    'Thailand': '+66',
    'Vietnam': '+84',
    'Philippines': '+63',
    'Indonesia': '+62',
    'Bangladesh': '+880',
    'Sri Lanka': '+94',
    'New Zealand': '+64',
    'Taiwan': '+886',
    'Hong Kong': '+852',
    'Belgium': '+32',
    'Netherlands': '+31',
    'Switzerland': '+41',
    'Austria': '+43',
    'Portugal': '+351',
    'Greece': '+30',
    'Hungary': '+36',
    'Romania': '+40',
    'Bulgaria': '+359',
}


# 定義主要國家和次要國家的權重
major_country_weights = {
    'USA': 10,          # 提高權重
    'Canada': 8,
    'Mexico': 2,
    'Japan': 5,
    'South Korea': 3,
    'Australia': 2,
    'United Kingdom': 10, # 提高權重
    'Germany': 3,
    'France': 10,       # 提高權重
    'Italy': 2,
    'China': 8,        # 提高權重
    'Singapore': 2,
    'Malaysia': 1,
    'India': 3,
    'Brazil': 2,
    'Russia': 1,
    'Poland': 1,
    'Czech Republic': 1,
}

minor_country_weights = {
    'Argentina': 1,
    'Chile': 1,
    'Colombia': 1,
    'Peru': 1,
    'Venezuela': 1,
    'South Africa': 1,
    'Nigeria': 1,
    'Egypt': 1,
    'Turkey': 1,
    'Saudi Arabia': 1,
    'United Arab Emirates': 1,
    'Israel': 1,
    'Thailand': 1,
    'Vietnam': 1,
    'Philippines': 1,
    'Indonesia': 1,
    'Bangladesh': 1,
    'Sri Lanka': 1,
    'New Zealand': 1,
    'Taiwan': 1,
    'Hong Kong': 1,
    'Belgium': 1,
    'Netherlands': 1,
    'Switzerland': 1,
    'Austria': 1,
    'Portugal': 1,
    'Greece': 1,
    'Hungary': 1,
    'Romania': 1,
    'Bulgaria': 1,
}

temp_data = []
# Generate customer data
data = pd.DataFrame(columns=headers)

for i in range(3000):
    # CustomerID
    id = i + 1

    # Name
    company = fake.company()

    if ((i + 1) % 4 != 0):
        # Country with weighted random selection
        country = random.choices(
            list(major_country_weights.keys()),
            weights=list(major_country_weights.values())
        )[0]
        country_code = major_country_code_map[country]
    else:
        # Minor countries
        country = random.choices(
            list(minor_country_weights.keys()),
            weights=list(minor_country_weights.values())
        )[0]
        country_code = minor_country_code_map[country]

    # Address
    address = fake.address()
    
    name = fake.name()

    # Phone number
    local_phone = fake.numerify('##########')  # 生成隨機10位數字
    phone = f"{country_code} {local_phone}"

    row = {
        "s_id": id,
        "s_name": company,
        "s_country": country,
        "s_address": address,
        "s_phone": phone,
        "super_name": name
    }
    
    temp_data.append(row)
    
print(len(temp_data))

data_s = pd.DataFrame(temp_data)

import os

# 確保資料夾存在，如果不存在則創建
folder_path = 'data_ff'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 儲存 CSV 檔案到資料夾中
file_path = os.path.join(folder_path, "supplier_f.csv")
data_s.to_csv(file_path, index=False)


