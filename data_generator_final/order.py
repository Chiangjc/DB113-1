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

# 127
all_positive_feedbacks = [
    "The part met all quality standards and performed flawlessly during assembly. ",
    "Excellent precision; the component fit perfectly without any adjustments. ",
    "Material strength was outstanding, ensuring long-term durability. ",
    "Surface finish was smooth and free from defects. ",
    "Fast delivery with no compromise on quality. ",
    "Exceeds our expectations in both functionality and reliability. ",
    "All specifications were met exactly as requested. ",
    "Tolerances were spot on; assembly was seamless. ",
    "The component performed exceptionally well under stress testing. ",
    "High-quality manufacturing with no visible flaws. ",
    "Consistent quality across multiple batches. ",
    "Reliable and robust components suitable for aviation standards. ",
    "Great communication during production ensured timely delivery. ",
    "Parts were lightweight yet incredibly strong. ",
    "Welds and joints were flawless, meeting safety standards. ",
    "Precision machining saved us time during final assembly. ",
    "Perfectly compatible with existing systems. ",
    "Quality control reports matched delivered components. ",
    "Outstanding corrosion resistance in harsh environments. ",
    "Highly impressed with the fatigue resistance of the part. ",
    "Delivered ahead of schedule without sacrificing quality. ",
    "The coating provided excellent protection and aesthetic appeal. ",
    "Suppliers demonstrated a strong commitment to quality. ",
    "Structural integrity was exceptional under load testing. ",
    "Customer support was responsive and helpful throughout the process. ",
    "This component exceeded all of our rigorous testing requirements. ",
    "The part's dimensional accuracy ensured a flawless installation. ",
    "We were impressed with the part's performance in real-world conditions. ",
    "The assembly process was straightforward thanks to the part's precision. ",
    "Exceptional attention to detail in every aspect of manufacturing. ",
    "The part's lightweight design contributed to fuel efficiency. ",
    "Very satisfied with the part's overall durability and performance. ",
    "We've experienced no issues with the components in extensive use. ",
    "The quality assurance process was thorough and effective. ",
    "The part delivered on all performance and safety metrics. ",
    "Impressed with the excellent balance of cost and quality. ",
    "The component's high tensile strength is ideal for aviation use. ",
    "This part has shown remarkable longevity under extreme conditions. ",
    "The components arrived in perfect condition and on time. ",
    "Fit and finish were outstanding, ensuring a smooth assembly process. ",
    "The supplier's quality control process was evident in the parts received. ",
    "The material quality exceeded expectations for aerospace standards. ",
    "The assembly process was quick and easy due to the quality of the part. ",
    "The part's superior build quality made it the best choice for the job. ",
    "Feedback from our engineering team was extremely positive. ",
    "Excellent attention to detail in the manufacturing process. ",
    "The part met all industry certification requirements. ",
    "The high quality of the part significantly reduced the assembly time. ",
    "This part has been proven to withstand high stress levels in testing. ",
    "The part performed well in all environmental tests, including vibration. ",
    "We have had no performance issues since installing this component. ",
    "The material choice was perfect for the intended application. ",
    "The welds were impeccable, ensuring structural integrity. ",
    "Outstanding performance in both dynamic and static testing. ",
    "The part functioned flawlessly in every test scenario. ",
    "The precise design of the part ensured ease of integration into the system. ",
    "The component was built to exact specifications and performed excellently. ",
    "Incredibly durable with no signs of wear after extensive use. ",
    "We appreciated the fast lead times and the consistent high quality. ",
    "The part arrived with no defects, ensuring smooth installation. ",
    "Excellent packaging ensured that parts were delivered without damage. ",
    "The part was well-engineered and met all required specifications. ",
    "We've been able to rely on this part for continuous, trouble-free operation. ",
    "The supplier's quality system ensured that all parts were up to standard. ",
    "Each batch of parts showed consistent quality from start to finish. ",
    "The part's high-quality finish made it easy to inspect for defects. ",
    "The part's performance exceeded the expectations of our engineering team. ",
    "The components have proven to be highly reliable under real-world conditions. ",
    "Highly satisfied with the overall quality of the parts supplied. ",
    "The part was easy to install, thanks to precise dimensions. ",
    "The durability of the part exceeded our expectations in every way. ",
    "The component's robust design helped improve overall system efficiency. ",
    "We've seen outstanding results from this part in field applications. ",
    "The part's resistance to corrosion is exactly what we needed. ",
    "Feedback from the production team was that the parts were excellent. ",
    "The component was easy to source and arrived promptly. ",
    "The manufacturing quality of the parts was exceptional. ",
    "The part performed without issue in all testing phases. ",
    "We appreciate the consistent quality and reliability of the components. ",
    "The part met all the stringent safety standards required in aviation. ",
    "The design and engineering of the part were exemplary. ",
    "The part's performance was flawless, meeting all operational requirements. ",
    "The overall quality and reliability of the part were outstanding. ",
    "The assembly process was quick and trouble-free due to part quality. ",
    "This part has demonstrated superior performance under extreme conditions. ",
    "Parts arrived well-packaged, free from any damage or defects. ",
    "We experienced no delays due to quality issues with this part. ",
    "The part was highly functional and met all of our design requirements. ",
    "The component showed remarkable strength and resilience during testing. ",
    "We received consistent quality on each batch of components. ",
    "We trust this supplier due to their commitment to quality. ",
    "The part was designed with great attention to detail, resulting in flawless performance. ",
    "Impressed with the quality of the materials used in the component. ",
    "The component's ability to handle high temperatures exceeded expectations. ",
    "The component showed excellent performance in all stress testing scenarios. ",
    "The high-quality construction of this part made it ideal for the application. ",
    "This part has proven to be durable and reliable in all testing environments. ",
    "Exceptional work on ensuring parts met all necessary aerospace specifications. ",
    "Feedback from the team was overwhelmingly positive regarding part quality. ",
    "The part arrived in perfect condition and fit perfectly with the assembly. ",
    "We've seen minimal wear and tear on this component, indicating its durability. ",
    "The part's functionality exceeded our expectations in all aspects. ",
    "Parts were manufactured to the highest industry standards. ",
    "The part's structural strength was evident from the initial installation. ",
    "The parts maintained excellent performance in extreme conditions. ",
    "Delivery was fast, and the parts were exactly as described. ",
    "The part's durability under testing proved its readiness for use in production. ",
    "The part's fitment was perfect, ensuring a seamless installation process. ",
    "The components showed no signs of degradation after long-term use. ",
    "The supplier provided great technical support during the production phase. ",
    "Outstanding accuracy and quality control made the part an ideal choice. ",
    "The part's consistent quality ensured minimal downtime during production. ",
    "The part's resistance to wear and tear was impressive during testing. ",
    "The component was easy to integrate and functioned exactly as required. ",
    "Excellent performance and reliability throughout the product lifecycle. ",
    "Parts met all engineering specifications and were easy to work with. ",
    "Impressed with the overall performance and efficiency of the component. ",
    "We have full confidence in the durability and functionality of this part. ",
    "The part's reliable performance made it a key component in the final product. ",
    "The manufacturing precision of this part was top-notch. ",
    "Exceptional quality control was evident in the final product. ",
    "The part was extremely durable, exceeding our expectations for longevity. ",
    "The component's precision manufacturing ensured a perfect fit. ",
    "The parts worked flawlessly after installation, providing no operational issues. ",
    "The supplier's commitment to quality resulted in an excellent product. ",
    "Parts consistently meet the highest industry standards, ensuring quality. ",
    "We are highly satisfied with the part's performance and reliability. "
]


# 139
all_negative_feedbacks = [
    "The part had visible defects, causing delays during assembly. ",
    "The material quality did not meet the required standards. ",
    "There were significant issues with part alignment during installation. ",
    "The surface finish was rough, requiring additional finishing work. ",
    "The component failed under stress testing, which delayed the project. ",
    "Parts arrived damaged, requiring rework before they could be used. ",
    "The part's dimensions were off, making installation difficult. ",
    "The component was not compatible with other parts in the assembly. ",
    "We received the parts late, affecting our production timeline. ",
    "The part showed signs of corrosion after a short period of use. ",
    "The part's material was not as durable as expected under extreme conditions. ",
    "Quality control was lacking, resulting in defective parts. ",
    "The part didn't meet the required fatigue resistance standards. ",
    "We had to reject several parts due to substandard quality. ",
    "The part's performance was below expectations during testing. ",
    "The part arrived with scratches and dents, which required rework. ",
    "Several parts had poor welds, impacting structural integrity. ",
    "The part didn't meet the required safety standards for aviation use. ",
    "We encountered delays due to poor quality assurance checks. ",
    "The components did not pass initial quality inspection. ",
    "The part's finish had visible imperfections, causing rework. ",
    "Several components were not delivered as per the agreed schedule. ",
    "The part's weight was heavier than specified, impacting performance. ",
    "The component's coating was inadequate and failed prematurely. ",
    "Poor communication during production led to missed deadlines. ",
    "The part failed to meet performance requirements during real-world testing. ",
    "We had compatibility issues with other system components due to design flaws. ",
    "The part showed poor reliability after extended use. ",
    "There were issues with the part's alignment during installation. ",
    "The part did not meet dimensional accuracy requirements. ",
    "The part was too brittle and cracked under normal stress. ",
    "We had to replace several parts due to poor performance. ",
    "The part's finish was not uniform, causing aesthetic concerns. ",
    "The supplier failed to meet the delivery deadline, causing project delays. ",
    "There was poor documentation regarding part specifications, causing confusion. ",
    "The part failed during routine testing, causing production halts. ",
    "Several parts had loose fittings, causing operational issues. ",
    "The part's material did not perform as expected in high-temperature conditions. ",
    "The part was not designed with enough strength to handle stress. ",
    "The supplier did not provide adequate support during the production phase. ",
    "We had to reject a batch of parts due to poor surface finish. ",
    "The part's manufacturing defects led to costly rework and delays. ",
    "The part showed early signs of wear and tear after minimal use. ",
    "The part's finish was inconsistent, affecting its aesthetic quality. ",
    "The part didn't meet the required load-bearing capacity. ",
    "We encountered issues with part fitment during assembly. ",
    "The part was not able to withstand vibration during testing. ",
    "The quality of materials used was subpar, affecting overall performance. ",
    "The supplier did not meet our expectations for quality or timeliness. ",
    "Several parts had to be returned due to defects. ",
    "The part did not meet corrosion resistance standards. ",
    "We encountered several manufacturing defects, leading to delays. ",
    "The component did not meet the necessary strength specifications. ",
    "Parts arrived with missing components, delaying assembly. ",
    "We had to replace a number of parts due to premature failure. ",
    "The component failed during stress testing, impacting our timeline. ",
    "The material used was not appropriate for the intended application. ",
    "The part's dimensions were inconsistent, making installation difficult. ",
    "The part was poorly manufactured, with many defects present. ",
    "The component failed quality control checks due to defects. ",
    "There was a significant delay in delivery, affecting production schedules. ",
    "Parts arrived in poor condition, requiring extensive rework. ",
    "The part did not meet dimensional tolerance requirements. ",
    "Several parts were defective, causing delays in assembly. ",
    "The part's coating was not durable enough for the required application. ",
    "The part did not pass all required tests, leading to rejection. ",
    "Quality control missed several critical defects, affecting assembly. ",
    "The component did not meet specifications, requiring adjustments. ",
    "The supplier failed to deliver the required quantity on time. ",
    "The part's performance was inconsistent during testing. ",
    "We encountered issues with part compatibility during installation. ",
    "The component's welds were weak, leading to structural concerns. ",
    "The part did not hold up to environmental testing. ",
    "There were discrepancies in the part dimensions, causing installation delays. ",
    "The part's resistance to wear and tear was below expectations. ",
    "The part did not meet the necessary vibration resistance standards. ",
    "We had issues with part misalignment during assembly. ",
    "The component did not meet the required fatigue resistance standards. ",
    "The part's design was flawed, leading to compatibility issues. ",
    "We had to reorder parts due to poor quality in the initial batch. ",
    "The component was brittle and broke under normal operational stress. ",
    "Parts arrived late, which impacted the overall schedule. ",
    "The component failed after a short period of use, leading to replacements. ",
    "The part was difficult to install due to dimensional inconsistencies. ",
    "Several parts showed visible defects, requiring rework before installation. ",
    "The part didn't meet aerospace standards for quality and performance. ",
    "The part's strength was insufficient for the required load-bearing application. ",
    "The part did not meet the expected environmental performance standards. ",
    "The part showed signs of premature wear after only a few cycles. ",
    "The part was not able to withstand high pressure as required. ",
    "There were defects in the part's welds that required rework. ",
    "The part's overall quality did not meet industry standards. ",
    "The part was delivered later than promised, causing delays in production. ",
    "There were visible defects on the part that affected its performance. ",
    "The part was difficult to integrate with other system components. ",
    "We had to replace several parts due to defects in material quality. ",
    "The part showed signs of rust after exposure to moisture. ",
    "The part was not up to specification, causing installation problems. ",
    "The material quality of the part was substandard, causing performance issues. ",
    "The part's fitment was problematic, delaying the production process. ",
    "The component did not meet the required safety performance standards. ",
    "There were manufacturing defects that impacted part quality. ",
    "The part's material did not perform as expected during testing. ",
    "The part failed to meet expected reliability standards in field testing. ",
    "Parts had to be reworked before installation due to quality issues. ",
    "The part's strength was below the required level, causing concerns. ",
    "We encountered issues with part incompatibility during assembly. ",
    "Parts arrived damaged, affecting the installation schedule. ",
    "The part did not pass quality control inspections, leading to delays. ",
    "We had issues with the supplier failing to meet quality expectations. ",
    "The component's material was not durable enough for the intended application. ",
    "Several components arrived with defects, causing rework and delays. ",
    "The part's coating failed under operational conditions, causing premature wear. ",
    "There were issues with part assembly due to dimensional inaccuracies. ",
    "The part did not meet the required tensile strength specifications. ",
    "The part's failure to meet performance requirements led to delays. ",
    "The part showed signs of early wear, leading to concerns about durability. ",
    "There were issues with part alignment, affecting assembly efficiency. ",
    "The component failed to meet the necessary load-bearing capacity. ",
    "The part did not perform well under testing conditions, leading to rejection. ",
    "Parts arrived damaged and required significant rework before use. ",
    "There were defects in the part's manufacturing process, affecting quality. ",
    "The part's coating peeled off after only a few cycles of use. ",
    "The part did not meet expected standards for strength and durability. ",
    "We experienced delays due to poor quality control on the part. ",
    "The part's performance was disappointing during real-world testing. ",
    "Parts did not meet the required specifications, causing issues during installation. ",
    "The component failed to perform as expected under environmental testing. ",
    "Parts arrived late, impacting the overall timeline for production. ",
    "The part's performance during stress testing was unsatisfactory. ",
    "We encountered compatibility issues due to incorrect dimensions on the part. ",
    "The part did not meet the required industry standards for safety. ",
    "The part was poorly designed, causing installation issues and delays. ",
    "The component did not pass necessary performance tests and was rejected. ",
    "We encountered several issues with the part's fitment and installation. ",
    "The part showed signs of failure after a short period of use. ",
    "Parts arrived with defects that required immediate attention. ",
    "The part's material did not perform under load as expected. ",
    "The part failed under vibration testing, requiring a redesign. "
]

cancel_reasons = [
    "The part does not meet the quality standards. ",
    "The delivery time is too long. ",
    "There was an error with the order. ",
    "The price is too high. ",
    "There is a lack of necessary accessories. ",
    "The part is incompatible with existing equipment. ",
    "The supplier failed to deliver on time. ",
    "There were unauthorized modifications made to the order. ",
    "The order was canceled due to budget limitations. ",
    "The part is out of stock. ",
    "The required specifications have changed. ",
    "Shipping delays have occurred. ",
    "The order is a duplicate. ",
    "The correct invoice or documents could not be provided. ",
    "The part is no longer needed. ",
    "The contract conditions were not met. ",
    "The product has been upgraded or replaced. ",
    "The part has been discontinued or is no longer available. ",
    "The supplier was unable to provide a replacement. ",
    "The order was canceled due to an internal decision. "
]

# print(len(all_positive_feedbacks))
# print(len(all_negative_feedbacks))

df = pd.read_csv(f"data_ff/inventory_{file_id}.csv")
inv_id_list = df['inv_id'].tolist()

print(len(inv_id_list))

# From Supplier
df = pd.read_csv(f"data_ff/employee_{file_id}.csv")
e_id_list = df[~pd.isna(df['leave_date'])]['e_id'].tolist()[2:]

print(len(e_id_list))

statuses_1 = ["Delivered", "Returned", "Deleted"]
all_feedbacks = []
statuses_2 = ["Not Yet Shipped", "In Transit", "Delivered", "Returned", "Deleted"]
statuses_3 = ["Not Yet Shipped", "In Transit"]
o_id = 1
order = []
all_orders = 0

# 測試資料生成器
def generate_test_data_before_2024(year, min_orders_per_year, max_orders_per_year):
    global o_id, all_orders, order
    # data = []
    current_date = datetime(year, 1, 1)  # 訂單的起始日期
    end_date = datetime(year, 12, 31)  # 訂單的結束日期

    # 確定總訂單數
    total_orders = random.randint(min_orders_per_year, max_orders_per_year)
    all_orders += total_orders

    # 平均每日下單數
    total_days = (end_date - current_date).days + 1
    avg_orders_per_day = total_orders / total_days
    while current_date <= end_date:
        # 當日的訂單數量（隨機波動，但符合平均範圍）
        orders_today = random.randint(int(avg_orders_per_day * 0.8), int(avg_orders_per_day * 1.2))
        for _ in range(orders_today):
            if o_id > all_orders:
                break
            
            # 截止日期：訂單日期後最多一年
            due_date = current_date + timedelta(days=random.randint(5, 365))
            
            status = random.choices(statuses_1, [0.9, 0.05, 0.05])[0]
            if status == "Returned" or status == "Delivered":
                arrive_date = due_date + timedelta(days=random.randint(-5, 5))
            else:
                arrive_date = None
            # 抵達日期：截止日期提前或延後最多 5 天

            # 根據狀態決定是否產生回饋
            if status == "Returned":
                rand_value = random.randint(1, 10)  # 隨機選擇1到5條檢查標準
                feedbacks = random.sample(all_negative_feedbacks, rand_value)  # 隨機選擇檢查標準
                feedback = ''.join(feedbacks)  # 拼接成一條標準字符串
            elif status == "Delivered":
                rand_value = random.randint(1, 10)  # 隨機選擇1到5條檢查標準
                feedbacks = random.sample(all_positive_feedbacks, rand_value)  # 隨機選擇檢查標準
                feedback = ''.join(feedbacks)  # 拼接成一條標準字符串
            else:
                rand_value = random.randint(1, 5)  # 隨機選擇1到5條檢查標準
                feedbacks = random.sample(cancel_reasons, rand_value)  # 隨機選擇檢查標準
                feedback = ''.join(feedbacks)

            e_id = random.choice(e_id_list)  # 員工編號
            inv_id = random.choice(inv_id_list)  # 庫存編號
            quantity = random.randint(1, 500)  
            
            arrive_date_str = arrive_date.strftime("%Y-%m-%d") if arrive_date else None

            order.append({
                "o_id": o_id,
                "inv_id": inv_id,
                "quantity": quantity,
                "order_date": current_date.strftime("%Y-%m-%d"),
                "due_date": due_date.strftime("%Y-%m-%d"),
                "arrive_date": arrive_date_str,
                "status": status,
                "feedback": feedback,
                "e_id": e_id
                
            })
            o_id += 1

        # 日期推進
        current_date += timedelta(days=1)
        
def generate_test_data_after_2024(year, min_orders_per_year, max_orders_per_year):
    global o_id, all_orders, order
    # data = []
    current_date = datetime(year, 1, 1)  # 訂單的起始日期
    end_date = datetime(year, 12, 31)  # 訂單的結束日期

    # 確定總訂單數
    total_orders = random.randint(min_orders_per_year, max_orders_per_year)
    all_orders += total_orders

    # 平均每日下單數
    total_days = (end_date - current_date).days + 1
    avg_orders_per_day = total_orders / total_days
    while current_date <= end_date:
        # 當日的訂單數量（隨機波動，但符合平均範圍）
        orders_today = random.randint(int(avg_orders_per_day * 0.8), int(avg_orders_per_day * 1.2))
        for _ in range(orders_today):
            if o_id > all_orders:
                break
            
            # 截止日期：訂單日期後最多一年
            due_date = current_date + timedelta(days=random.randint(5, 365))
            limit = datetime.strptime('2024-12-11', '%Y-%m-%d')
            if due_date > limit:
                status = random.choice(statuses_3)
            else:
                status = random.choices(statuses_2, [0.1, 0.1, 0.72, 0.04, 0.04])[0]
                
            if status in ["Not Yet Shipped", "In Transit", "Deleted"]:
                arrive_date = None
            else:
                arrive_date = due_date + timedelta(days=random.randint(-5, 5))
                # 抵達日期：截止日期提前或延後最多 5 天

            # 根據狀態決定是否產生回饋
            if status == "Returned":
                rand_value = random.randint(1, 10)  # 隨機選擇1到5條檢查標準
                feedbacks = random.sample(all_negative_feedbacks, rand_value)  # 隨機選擇檢查標準
                feedback = ''.join(feedbacks)  # 拼接成一條標準字符串
            elif status == "Delivered":
                rand_value = random.randint(1, 10)  # 隨機選擇1到5條檢查標準
                feedbacks = random.sample(all_positive_feedbacks, rand_value)  # 隨機選擇檢查標準
                feedback = ''.join(feedbacks)  # 拼接成一條標準字符串
            elif status == "Deleted":
                rand_value = random.randint(1, 5)  # 隨機選擇1到5條檢查標準
                feedbacks = random.sample(cancel_reasons, rand_value)  # 隨機選擇檢查標準
                feedback = ''.join(feedbacks)  # 拼接成一條標準字符串
            else:
                feedback = None

            e_id = random.choice(e_id_list)  # 員工編號
            inv_id = random.choice(inv_id_list)  # 庫存編號
            quantity = random.randint(1, 500)  
            
            arrive_date_str = arrive_date.strftime("%Y-%m-%d") if arrive_date else None

            order.append({
                "o_id": o_id,
                "inv_id": inv_id,
                "quantity": quantity,
                "order_date": current_date.strftime("%Y-%m-%d"),
                "due_date": due_date.strftime("%Y-%m-%d"),
                "arrive_date": arrive_date_str,
                "status": status,
                "feedback": feedback,
                "e_id": e_id
                
            })
            o_id += 1

        # 日期推進
        current_date += timedelta(days=1)

    


min_orders_per_year = 5000
max_orders_per_year = 10000

for i in range(1997, 2025):
    if i < 2024:
        generate_test_data_before_2024(i, min_orders_per_year, max_orders_per_year)
    else:
        generate_test_data_after_2024(i, min_orders_per_year, max_orders_per_year)

# 轉換為 DataFrame
data_order = pd.DataFrame(order)

# 將資料儲存為 CSV 文件
data_order.to_csv('order_f.csv', index=False)

# 顯示部分測試資料
print(len(order))
