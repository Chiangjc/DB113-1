import re
import math
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import pandas as pd
from dateutil.relativedelta import relativedelta
import string
import csv
from english_words import get_english_words_set
import os

file_id = 'f'

# Password（隨機組合單詞和數字）
def generate_password():
    part1 = random.choice(word_list)
    part2 = random.choice(word_list) if random.random() > 0.5 else ''
    numbers = ''.join(random.choices(string.digits, k=random.randint(2, 4)))
    patterns = [
        part1 + part2 + numbers,
        numbers + part1 + part2,
        part1 + numbers + part2
    ]
    return random.choice(patterns)

# 獲取所有的英文字
word_list = list(get_english_words_set(["web2"], lower=True))  # 確保轉換為列表

fake = Faker()

# 設定生成數據的標題
headers_e = ['e_id', 'e_name', 'start_date', 'leave_date', 'password', 'mgr_id', 'role']

# 員工數量
num_employees = 100000

# 初始化資料
data_e = pd.DataFrame(columns=headers_e)

# 生成所有 e_id，確保英文字母為大寫
e_ids = [
    ''.join(random.choices(string.ascii_uppercase, k=2)) + fake.numerify('#########')
    for _ in range(num_employees)
]

# 隨機選擇 5% 的 e_id 作為主管
num_managers = round(num_employees * 0.05)
mgr_ids = random.sample(e_ids, k=num_managers)  # 約 5% 的員工為主管

# 保留 Kelly Ortberg 和 Steve Mollenkopf 的 id
fixed_managers = ['Kelly Ortberg', 'Steve Mollenkopf']

# 為這兩個特定的主管生成 id
fixed_mgr_ids = []
for name in fixed_managers:
    fixed_id = ''.join(random.choices(string.ascii_uppercase, k=3)) + fake.numerify('#########')
    fixed_mgr_ids.append(fixed_id)
    
temp_data = []

# 確保這兩個固定的主管有專門的資料行
for i, name in enumerate(fixed_managers):
    password = generate_password()
    row = {
        'e_id': fixed_mgr_ids[i],
        'e_name': name,
        'start_date': fake.date_between(start_date='-27y', end_date='today').strftime('%Y-%m-%d'),
        'leave_date': None,  # 固定主管不會離職
        'password': password,
        'mgr_id': None,
        'role': 'Admin',
    }
    temp_data.append(row)

# 生成剩餘的員工數據
for eid in e_ids:
    if eid in fixed_mgr_ids:
        continue  # 已經為固定主管生成數據

    # Name
    ename = fake.name()

    # Start date
    start_date = fake.date_between(start_date='-27y', end_date='today').strftime('%Y-%m-%d')
    password = generate_password()

    # 判斷角色和指定 mgr_id
    if eid in mgr_ids:
        role = 'Admin'
        if eid in mgr_ids[:10]:
            mgr_id = random.choice(fixed_mgr_ids)  # 確保指向CEO或Stockboard
        else:
            mgr_id = random.choice(mgr_ids[:10])
    else:
        role = 'User'
        mgr_id = random.choice(mgr_ids[10:])
        while mgr_id in fixed_mgr_ids:
            mgr_id = random.choice(mgr_ids)  # 確保不指向CEO和Stockboard

    # 根據入職日期決定是否離職
    leave_date = None
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    today_date_obj = datetime.today()
    start_year = start_date_obj.year

    # 假設2005年以前的員工大多已經離職
    if start_year < 2005:
        leave_date = fake.date_between(
            start_date=start_date_obj,
            end_date=today_date_obj - timedelta(days=1)  # 確保離職日期小於今天
        ).strftime('%Y-%m-%d')

    # 假設2005到2010年入職的員工可能離職
    elif 2005 <= start_year <= 2010:
        if random.random() < 0.6:  # 60% 機率離職
            leave_date = fake.date_between(
                start_date=start_date_obj,
                end_date=today_date_obj - timedelta(days=1)
            ).strftime('%Y-%m-%d')

    # 假設2010到2015年入職的員工可能離職
    elif 2010 < start_year <= 2015:
        if random.random() < 0.3:  # 30% 機率離職
            leave_date = fake.date_between(
                start_date=start_date_obj,
                end_date=today_date_obj - timedelta(days=1)
            ).strftime('%Y-%m-%d')
    # 建立新資料
    row = {
        'e_id': eid,
        'e_name': ename,
        'start_date': start_date,
        'leave_date': leave_date,
        'password': password,
        'mgr_id': mgr_id,
        'role': role,
    }

    temp_data.append(row)
    
print(len(temp_data))

data_e = pd.DataFrame(temp_data)

# 確保資料夾存在，如果不存在則創建
folder_path = 'data_ff'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 儲存 CSV 檔案到資料夾中
file_path = os.path.join(folder_path, "employee_f.csv")
data_e.to_csv(file_path, index=False)

#================================================================

factory_country_weights = {
    'USA': 20,          # 提高權重
    'Canada': 11,
    'Mexico': 2,
    'Japan': 5,
    'South Korea': 3,
    'Australia': 2,
    'United Kingdom': 17, # 提高權重
    'Germany': 3,
    'France': 13,       # 提高權重
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

factory_country_code_map = {
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

headers_f = ['f_id', 'f_name', 'f_country', 'f_address', 'f_phone', 'super_id']

data_f = pd.DataFrame(columns=headers_f)

factories = [
    "AeroCore Components A", "AeroCore Components B", "AeroCore Components C", "AeroCore Components D", "AeroCore Components E",
    "SkyLift Technologies A", "SkyLift Technologies B", "SkyLift Technologies C", "SkyLift Technologies D", "SkyLift Technologies E",
    "Stellar Dynamics A", "Stellar Dynamics B", "Stellar Dynamics C", "Stellar Dynamics D",
    "NovaJet Systems A", "NovaJet Systems B", "NovaJet Systems C", "NovaJet Systems D", "NovaJet Systems E",
    "Infinity Assemblies A", "Infinity Assemblies B", "Infinity Assemblies C", "Infinity Assemblies D", "Infinity Assemblies E",
    "FlightCore Manufacturing A", "FlightCore Manufacturing B", "FlightCore Manufacturing C", "FlightCore Manufacturing D", "FlightCore Manufacturing E",
    "BlueHorizon Industries A", "BlueHorizon Industries B", "BlueHorizon Industries C",
    "Cloudline Assemblies A", "Cloudline Assemblies B", "Cloudline Assemblies C", "Cloudline Assemblies D", "Cloudline Assemblies E",
    "JetMax Fabrication A", "JetMax Fabrication B",
    "Altitude AeroParts A", "Altitude AeroParts B", "Altitude AeroParts C", "Altitude AeroParts D",
    "Horizon Aerospace A", "Horizon Aerospace B", "Horizon Aerospace C", "Horizon Aerospace D", "Horizon Aerospace E",
    "Starline Assemblies A", "Starline Assemblies B", "Starline Assemblies C", "Starline Assemblies D", "Starline Assemblies E",
    "Stratosphere Systems A", "Stratosphere Systems B", "Stratosphere Systems C", "Stratosphere Systems D",
    "TurboWing Assembly A", "TurboWing Assembly B", "TurboWing Assembly C", "TurboWing Assembly D", "TurboWing Assembly E",
    "GlideTech Manufacturing A", "GlideTech Manufacturing B",
    "Apex Avionics A", "Apex Avionics B", "Apex Avionics C",
    "Eagle Precision Works A", "Eagle Precision Works B", "Eagle Precision Works C", "Eagle Precision Works D", "Eagle Precision Works E",
    "FlightPath Engineering A", "FlightPath Engineering B", "FlightPath Engineering C",
    "Titan AeroParts A", "Titan AeroParts B",
    "JetBridge Systems A", "JetBridge Systems B", "JetBridge Systems C",
    "LunarJet Components A", "LunarJet Components B", "LunarJet Components C", "LunarJet Components D", "LunarJet Components E",
    "SolarWing Systems A",
    "AeroVerge Manufacturing A", "AeroVerge Manufacturing B", "AeroVerge Manufacturing C", "AeroVerge Manufacturing D", "AeroVerge Manufacturing E",
    "FalconTech Assembly A", "FalconTech Assembly B", "FalconTech Assembly C", "FalconTech Assembly D", "FalconTech Assembly E",
    "JetCore Solutions A", "JetCore Solutions B", "JetCore Solutions C", "JetCore Solutions D",
    "Skyward Manufacturing A", "Skyward Manufacturing B",
    "StellarCraft Manufacturing A", "StellarCraft Manufacturing B", "StellarCraft Manufacturing C", "StellarCraft Manufacturing D", "StellarCraft Manufacturing E",
    "TrueFlight Technologies A", "TrueFlight Technologies B",
    "Helios Aerospace A",
    "AeroFusion Works A",
    "NovaCraft Systems A", "NovaCraft Systems B", "NovaCraft Systems C", "NovaCraft Systems D", "NovaCraft Systems E",
    "CloudWorks Manufacturing A", "CloudWorks Manufacturing B", "CloudWorks Manufacturing C", "CloudWorks Manufacturing D",
    "JetFusion Assemblies A", "JetFusion Assemblies B", "JetFusion Assemblies C",
    "Polaris Avionics A", "Polaris Avionics B", "Polaris Avionics C", "Polaris Avionics D", "Polaris Avionics E",
    "StratosFlight Systems A", "StratosFlight Systems B", "StratosFlight Systems C", "StratosFlight Systems D", "StratosFlight Systems E",
    "AeroVantage Systems A", "AeroVantage Systems B", "AeroVantage Systems C", "AeroVantage Systems D", "AeroVantage Systems E",
    "Zenith Wingworks A", "Zenith Wingworks B", "Zenith Wingworks C",
    "SkyBound Precision A", "SkyBound Precision B", "SkyBound Precision C", "SkyBound Precision D", "SkyBound Precision E",
    "Phoenix JetTech A", "Phoenix JetTech B",
    "HighPoint Assemblies A", "HighPoint Assemblies B"
]

temp_data =[]

for i in range(150):
    # Factoryid
    fid = i + 1

    # Name
    fname = factories[i]

    # Country with weighted random selection
    fcountry = random.choices(
        list(factory_country_weights.keys()),
        weights=list(factory_country_weights.values())
    )[0]
    country_code = factory_country_code_map[fcountry]

    # Address
    faddress = fake.address()

    # Phone number
    local_phone = fake.numerify('##########')  # 生成隨機10位數字
    fphone = f"{country_code} {local_phone}"
    
    superid = random.choices(mgr_ids[10:])

    row = {
        'f_id': fid, 
        'f_name': fname,
        'f_country' :fcountry, 
        'f_address': faddress, 
        'f_phone': fphone, 
        'super_id': superid
    }
    
    temp_data.append(row)

print(len(temp_data))

data_f = pd.DataFrame(temp_data)


# 確保資料夾存在，如果不存在則創建
folder_path = 'data_ff'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 儲存 CSV 檔案到資料夾中
file_path = os.path.join(folder_path, "factory_f.csv")
data_f.to_csv(file_path, index=False)


