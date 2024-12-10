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

from sympy import isprime, primerange, primefactors

large = ["Fuselage", "Wings", "Engines", "Landing Gear", "Vertical Stabilizer",
               "Horizontal Stabilizer", "Cockpit", "Empennage", "Ailerons", "Flaps",
               "Spoilers", "Winglets", "Slats", "Rudders", "Elevators", "Propellers",
               "Tail Cone", "Nacelles", "Avionics", "Fuel Tanks", "Hydraulic Systems",
               "Electrical Systems", "Air Conditioning Systems", "Oxygen Systems",
               "Flight Control Systems", "Navigation Systems", "Landing Lights", "Taxi Lights",
               "Wingtips", "Struts", "Skins", "Bulkheads", "Frames", "Stringers", "Spars",
               "Flanges", "Fairings", "Access Panels", "Cargo Bays", "Pressure Bulkheads",
               "Thrust Reversers", "Exhaust Nozzles", "Wing Spar", "Wing Rib", "Wing Leading Edge",
               "Wing Trailing Edge", "Tail Boom", "Tail Skid", "Nose Gear", "Main Gear"]
medium = ["Avionics", "Air Conditioning Systems", "Oxygen Systems", "Flight Control Systems",
                "Navigation Systems", "Landing Lights", "Taxi Lights", "Wingtips", "Struts", "Skins",
                "Bulkheads", "Frames", "Stringers", "Spars", "Flanges", "Fairings", "Access Panels",
                "Cargo Bays", "Pressure Bulkheads", "Thrust Reversers", "Exhaust Nozzles", "Wing Spar",
                "Wing Rib", "Wing Leading Edge", "Wing Trailing Edge", "Tail Boom", "Tail Skid",
                "Nose Gear", "Main Gear", "Hydraulic Lines", "Electrical Wiring", "Fuel Lines",
                "Oxygen Lines", "Control Cables", "Landing Gear Doors", "Wing Flaps", "Spoilers",
                "Ailerons", "Rudders", "Elevators", "Propeller Blades", "Engine Cowlings",
                "Exhaust Ducts", "Winglets", "Slats", "Tail Cone", "Nacelles", "Avionics Bays",
                "Flight Deck", "Cockpit Windows", "Fuselage Panels", "Wing Panels", "Tail Panels",
                "Landing Gear Bays", "Cargo Doors", "Pressure Relief Valves", "Hydraulic Pumps",
                "Electrical Generators", "Fuel Pumps", "Oxygen Pumps", "Control Surfaces", "Navigation Lights",
                "Landing Gear Struts", "Wing Attachments", "Tail Attachments", "Nose Attachments",
                "Main Attachments", "Engine Mounts", "Propeller Mounts", "Thrust Reverser Mounts",
                "Exhaust Mounts", "Winglet Mounts", "Slats Mounts", "Tail Boom Mounts", "Tail Skid Mounts",
                "Nose Gear Mounts", "Main Gear Mounts", "Hydraulic Lines Mounts", "Electrical Wiring Mounts",
                "Fuel Lines Mounts", "Oxygen Lines Mounts", "Control Cables Mounts", "Landing Gear Doors Mounts",
                "Wing Flaps Mounts", "Spoilers Mounts", "Ailerons Mounts", "Rudders Mounts", "Elevators Mounts",
                "Propeller Blades Mounts", "Engine Cowlings Mounts", "Exhaust Ducts Mounts", "Winglets Mounts",
                "Slats Mounts", "Tail Cone Mounts", "Nacelles Mounts", "Avionics Bays Mounts", "Flight Deck Mounts",
                "Cockpit Windows Mounts", "Fuselage Panels Mounts", "Wing Panels Mounts"]
small = [
    "Washer", "Nut", "Bolt", "Rivet", "Screw", "Clamp", "Pin", "Spacer", "Spring", "Bushing", 
    "Retainer", "O-ring", "Seal", "Gasket", "Clip", "Bracket", "Hinge", "Latch", "Fastener", 
    "Connector", "Coupling", "Valve", "Pump", "Bearing", "Gear", "Shaft", "Actuator", "Servo", 
    "Motor", "Sensor", "Relay", "Switch", "Diode", "Resistor", "Capacitor", "Transformer", 
    "Rectifier", "Inverter", "Transistor", "Circuit", "Module", "Board", "Panel", "Display", 
    "Screen", "Monitor", "Indicator", "Gauge", "Meter", "Fuse", "Breaker", "Antenna", "Cable", 
    "Wire", "Plug", "Socket", "Connector", "Harness", "Strut", "Spring", "Damper", "Stabilizer", 
    "Support", "Bracket", "Shim", "Pad", "Washer", "Nut", "Bolt", "Rivet", "Screw", "Clamp", 
    "Pin", "Spacer", "Spring", "Bushing", "Retainer", "O-ring", "Seal", "Gasket", "Clip", 
    "Bracket", "Hinge", "Latch", "Fastener", "Connector", "Coupling", "Valve", "Pump", "Bearing", 
    "Gear", "Shaft", "Actuator", "Servo", "Motor", "Sensor", "Relay", "Switch", "Diode", "Resistor", 
    "Capacitor", "Transformer", "Rectifier", "Inverter", "Transistor", "Circuit", "Module", "Board", 
    "Panel", "Display", "Screen", "Monitor", "Indicator", "Gauge", "Meter", "Fuse", "Breaker", 
    "Antenna", "Cable", "Wire", "Plug", "Socket", "Connector", "Harness", "Strut", "Spring", "Damper", 
    "Stabilizer", "Support", "Bracket", "Shim", "Pad", "Washer", "Nut", "Bolt", "Rivet", "Screw", 
    "Clamp", "Pin", "Spacer", "Spring", "Bushing", "Retainer", "O-ring", "Seal", "Gasket", "Clip", 
    "Bracket", "Hinge", "Latch", "Fastener", "Connector", "Coupling", "Valve", "Pump", "Bearing", 
    "Gear", "Shaft", "Actuator", "Servo", "Motor", "Sensor", "Relay", "Switch", "Diode", "Resistor", 
    "Capacitor", "Transformer", "Rectifier", "Inverter", "Transistor", "Circuit", "Module", "Board", 
    "Panel", "Display", "Screen", "Monitor", "Indicator", "Gauge", "Meter", "Fuse", "Breaker", 
    "Antenna", "Cable", "Wire", "Plug", "Socket", "Connector", "Harness", "Strut", "Spring", "Damper", 
    "Stabilizer", "Support", "Bracket", "Shim", "Pad", "Washer", "Nut"
]

flight_adjectives = [
    "Aerodynamic", "Altitudinal", "Airborne", "Airy", "Ample", "Aerial", "Agile", "Atmospheric", "Autonomous", "Balanced",
    "Breezy", "Brilliant", "Buoyant", "Cloudless", "Colossal", "Convectional", "Controlled", "Cruising", "Daring", "Descending",
    "Dynamic", "Efficient", "Elevated", "Endless", "Expansive", "Fast", "Flightworthy", "Flowing", "Flying", "Gliding",
    "Gravitational", "Harmonious", "Hovering", "High", "High-flying", "Hovercraft", "Hypersonic", "Ideal", "Immense", "Impulsive",
    "Independent", "Infinite", "Innovative", "Invincible", "Iridescent", "Jetstream", "Lightweight", "Lifted", "Limitless", "Lofty",
    "Luminous", "Maneuverable", "Maximum", "Melodic", "Migratory", "Mighty", "Miraculous", "Nomadic", "Optimized", "Optimal",
    "Overhead", "Panoramic", "Perpetual", "Placid", "Powerful", "Precarious", "Pressurized", "Rapid", "Rising", "Rugged",
    "Sailing", "Sinuous", "Skyward", "Sleek", "Slippery", "Smooth", "Sonic", "Soaring", "Spectacular", "Speedy",
    "Stable", "Steady", "Stealthy", "Streamlined", "Sublime", "Sufficient", "Swift", "Turbulent", "Unyielding", "Vast",
    "Vertical", "Vibrational", "Vigilant", "Wavy", "Weightless", "Windborne", "Winging", "Winding", "Zealous", "Zippy",
    "Accelerating", "Active", "Apt", "Balletic", "Bright", "Bumpy", "Calm", "Choppy", "Climbing", "Crisp",
    "Defying", "Delicate", "Defiant", "Dynamic", "Eager", "Effortless", "Elastic", "Elevating", "Evolving", "Explosive",
    "Far-reaching", "Feather-light", "Fierce", "Flexible", "Floating", "Flow", "Fluent", "Forward", "Glorious", "Gravity-defying",
    "High-speed", "Hover", "Invisible", "Lithe", "Luxurious", "Magnetic", "Magnificent", "Majestic", "Melodious", "Navigational",
    "Never-ending", "On-the-go", "Overpowered", "Precise", "Propulsive", "Radiant", "Rapid-fire", "Revolutionary", "Rising",
    "Robust", "Round-the-clock", "Sleek", "Slim", "Smart", "Snappy", "Sonic-speed", "Sophisticated", "Stabilized", "Steady",
    "Superb", "Swift-moving", "Turbine", "Unstoppable", "Vigorous", "Vortex", "Wanderlust", "Whirling", "Wind-assisted", "Zero-gravity"
]

check_standards = [
    "Ensure the part is free from cracks or defects. ",
    "Verify dimensions and tolerance against engineering drawings. ",
    "Check the material strength using standard stress testing. ",
    "Verify the part is corrosion-resistant under high humidity conditions. ",
    "Perform a weight test to ensure it meets the required specifications. ",
    "Check for smooth operation under high pressure conditions. ",
    "Ensure the part functions under extreme temperatures without degradation. ",
    "Verify that the part passes a visual inspection for surface finish quality. ",
    "Ensure all fasteners are properly tightened and secured. ",
    "Test the part for functionality and durability in simulated flight conditions. ",
    "Ensure that no part is exposed to excessive wear and tear. ",
    "Check that the part is free from rust and other forms of corrosion. ",
    "Verify the part's performance under vibration testing. ",
    "Test the material for resistance to chemical exposure. ",
    "Ensure that all seals are in good condition and function properly. ",
    "Check the part's noise emissions under normal operation. ",
    "Ensure the part fits within the specified envelope for installation. ",
    "Perform impact testing to verify the part's integrity under sudden force. ",
    "Verify that the part passes electrical safety standards. ",
    "Ensure that the part is free of foreign material contamination. ",
    "Test the part's resistance to UV degradation over time. ",
    "Ensure that moving parts have sufficient lubrication. ",
    "Verify that the part operates correctly in varying load conditions. ",
    "Perform a stress test to ensure the part can handle extreme forces. ",
    "Verify the part's resistance to fatigue under repeated use. ",
    "Ensure that the part complies with environmental regulations. ",
    "Test the part for waterproofing or water resistance. ",
    "Ensure the part does not exceed noise level regulations. ",
    "Check that the part maintains performance in varying atmospheric pressures. ",
    "Verify that the part can withstand thermal cycling without damage. ",
    "Test the part for electrical conductivity where applicable. ",
    "Ensure the part is free from cracks that could lead to failure. ",
    "Check that the part meets aerodynamic efficiency standards. ",
    "Verify that the part does not generate excessive heat during operation. ",
    "Ensure the part passes all fire resistance tests. ",
    "Test the part for electromagnetic compatibility (EMC). ",
    "Ensure the part complies with safety guidelines for handling. ",
    "Perform a bending test to verify strength and flexibility. ",
    "Check for proper insulation in electrical components. ",
    "Ensure that the part performs correctly under high-altitude conditions. ",
    "Verify that the part meets all regulatory standards for safety. ",
    "Check the part's compliance with ISO quality standards. ",
    "Ensure that the part is compatible with other components. ",
    "Verify that the part is free from sharp edges or dangerous protrusions. ",
    "Test the part under extreme humidity to check for deterioration. ",
    "Ensure that any moving components are free from obstruction. ",
    "Check that the part's surface is free from dirt or oil. ",
    "Verify that the part maintains structural integrity after extended use. ",
    "Ensure that the part does not exhibit any abnormal vibrations during operation. ",
    "Test the part for proper sealing and airtightness. ",
    "Ensure the part is designed to minimize maintenance needs. ",
    "Test the part's ability to handle pressure fluctuations. ",
    "Ensure that the part is resistant to wear and abrasion over time. ",
    "Verify that the part meets the minimum lifespan requirements. ",
    "Ensure that the part has been properly treated for environmental protection. ",
    "Perform a leakage test to ensure proper containment. ",
    "Test the part for flexibility under different temperature conditions. ",
    "Ensure the part has sufficient tolerance for manufacturing variances. ",
    "Verify the part's resistance to rust under typical operating conditions. ",
    "Test the part's electrical components for short circuits or failures. ",
    "Ensure that any hydraulic or pneumatic components are leak-free. ",
    "Verify that all connections are correctly installed and functioning. ",
    "Ensure the part is designed to be easy to disassemble for maintenance. ",
    "Test the part for proper alignment with other components. ",
    "Ensure that the part meets weight specifications without sacrificing strength. ",
    "Verify that the part does not degrade under prolonged exposure to sunlight. ",
    "Ensure the part complies with fire retardant standards. ",
    "Verify the part's resistance to moisture absorption. ",
    "Test the part for smooth operation in both dry and wet conditions. ",
    "Ensure that the part maintains functionality after multiple cycles of use. ",
    "Test the part's ability to handle a sudden loss of power or failure. ",
    "Ensure the part is made of materials that are compatible with the environment it will operate in. ",
    "Verify that the part can withstand sudden temperature changes. ",
    "Ensure that the part has proper heat dissipation mechanisms. ",
    "Test the part's compliance with energy consumption regulations. ",
    "Verify that the part has sufficient clearance for installation. ",
    "Check that the part meets noise and vibration reduction requirements. ",
    "Ensure that any coatings or finishes are applied evenly and meet standards. ",
    "Verify that the part complies with environmental and safety guidelines. ",
    "Ensure that the part meets all technical specifications for performance. ",
    "Test the part for compatibility with other systems or modules. ",
    "Ensure that all fasteners and components are correctly sized and installed. ",
    "Verify the part's resistance to impacts from debris or foreign objects. ",
    "Ensure the part has a suitable fatigue life for its intended use. ",
    "Test the part for wear resistance under continuous motion. ",
    "Ensure the part's electrical systems function properly under load. ",
    "Verify that the part is free from manufacturing defects. ",
    "Ensure the part is designed to minimize risk of failure during operation. ",
    "Test the part for durability in both dry and wet environments. ",
    "Ensure that the part is properly balanced for vibration control. ",
    "Verify the part's resistance to high-stress conditions. ",
    "Check that the part has a minimal coefficient of friction where necessary. ",
    "Ensure the part is capable of handling varying levels of shock or impact. ",
    "Test the part's thermal conductivity and insulation properties. ",
    "Ensure the part is free from bubbles, voids, or defects in material composition. ",
    "Verify the part meets specific tolerances for functionality. ",
    "Ensure that the part is compatible with standard industry tools. ",
    "Test the part for appropriate resistance to external contaminants. ",
    "Ensure the part is designed for ease of assembly and maintenance. ",
    "Verify the part can handle operational load without deformation. ",
    "Ensure the part's interface with other components is secure and stable. ",
    "Test the part's strength under static and dynamic loads. ",
    "Ensure the part meets all performance benchmarks for efficiency. ",
    "Verify that the part can be safely used under varying operational conditions. ",
    "Ensure the part's design minimizes the potential for fatigue failure. ",
    "Test the part's chemical resistance in operating conditions. ",
    "Ensure the part is resistant to galvanic corrosion when used with dissimilar metals. ",
    "Verify that the part is suitable for long-term storage without degradation. ",
    "Ensure that the part's shape and design are optimized for aerodynamic efficiency. "
]

fake = Faker()
all_p = [] #紀錄所有 part 的 name
all_inv = []
small_parts = [] 
medium_parts = []
large_parts = []
temp_data = []

small_invs = []

plane_num = ["787-1", "787-2", "787-3", "787-4", "787-5", "787-6", "787-7", "787-8", "787-9", "787-10",
             "777-1", "777-2", "777-3", "777-4", "777-5", "777-6", "777-7",
             "767-1", "767-2", "767-3", "767-4", "767-5", "767-6", "767-7", "767-8", "767-9", "767-10", "767-11", "767-12", "767-13",
             "757-1", "757-2", "757-3", "757-4", "757-5", "757-6", "757-7", "757-8", "757-9", "757-10",
             "747-1", "747-2", "747-3",
             "737-1", "737-2", "737-3", "737-4", "737-5"
             ]
             
letters = [chr(i) for i in range(65, 91)]

count1 = 0
count2 = 0
m = 0
for i in range(200):
    rand_1 = random.randint(1, 10)
    unique_values = random.sample(range(0, 169), rand_1)  # 生成不重複的數字
    for j in unique_values:  # 使用這些數字作為索引
        plane_num_m = m%48
        pname = flight_adjectives[j] + " " + small[i]
        small_parts.append(pname)
        
        rand_value = random.randint(1, 10)  # 隨機選擇1到5條檢查標準
        standards = random.sample(check_standards, rand_value)  # 隨機選擇檢查標準
        standard = ''.join(standards)  # 拼接成一條標準字符串
        
        length = random.randint(5, 20)*5 + random.choices([0, 1, 2, 3, 0.75, 0.25, 0.5], [0.9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])[0]
        width = random.randint(5, 20)*5 + random.choices([0, 1, 2, 3, 0.75, 0.25, 0.5], [0.9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])[0]
        height = random.randint(5, 20)*5 + random.choices([0, 1, 2, 3, 0.75, 0.25, 0.5], [0.9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])[0]
        count1 += 1
        row1 = {
            "p_id": count1,
            "p_name": pname,
            "standard": standard,
            "length": length,
            "width": width,
            "height": height
        }
        
        all_p.append(row1)
        rand = random.randint(1, 5)
        for n in range(rand):
            inv_name = pname + " " + letters[n] 
            
            if isprime(count2) == True:
                status = "Not Using"
            else:
                status = "Using"
            row2 = {
                "inv_id": count2,
                "inv_name": inv_name,
                "status": status,
                "p_id": count1,
                "plane": plane_num[plane_num_m]
            }
            all_inv.append(row2)
            small_invs.append(row2)
        m += 1
            
medium_invs = []
            
for i in range(100):
    rand_1 = random.randint(1, 10)
    unique_values = random.sample(range(0, 169), rand_1)  # 生成不重複的數字
    for j in unique_values:  # 使用這些數字作為索引
        pname = flight_adjectives[j] + " " + small[i]
        medium_parts.append(pname)
        plane_num_m = m%48
        
        rand_value = random.randint(1, 10)  # 隨機選擇1到10條檢查標準
        standards = random.sample(check_standards, rand_value)  # 隨機選擇檢查標準
        standard = ''.join(standards)  # 拼接成一條標準字符串
        
        length = random.randint(20, 1000)*5 + random.choices([0, 2, 5], [0.6, 0.2, 0.2])[0]
        width = random.randint(20, 1000)*5 + random.choices([0, 2, 5], [0.6, 0.2, 0.2])[0]
        height = random.randint(20, 1000)*5 + random.choices([0, 2, 5], [0.6, 0.2, 0.2])[0]
        count1 += 1
        row1 = {
            "p_id": count1,
            "p_name": pname,
            "standard": standard,
            "length": length,
            "width": width,
            "height": height
        }
        
        all_p.append(row1)
        rand = random.randint(1, 5)
        for n in range(rand):
            inv_name = pname + " " + letters[n] 
            
            if isprime(count2) == True:
                status = "Not Using"
            else:
                status = "Using"
            row2 = {
                "inv_id": count2,
                "inv_name": inv_name,
                "status": status,
                "p_id": count1,
                "plane": plane_num[plane_num_m]
            }
            all_inv.append(row2)
            medium_invs.append(row2)
        m += 1

large_invs = []

for i in range(50):
    rand_1 = random.randint(1, 10)
    unique_values = random.sample(range(0, 169), rand_1)  # 生成不重複的數字
    for j in unique_values:  # 使用這些數字作為索引
        pname = flight_adjectives[j] + " " + small[i]
        large_parts.append(pname)
        plane_num_m = m%48
        
        rand_value = random.randint(1, 10)  # 隨機選擇1到10條檢查標準
        standards = random.sample(check_standards, rand_value)  # 隨機選擇檢查標準
        standard = ''.join(standards)  # 拼接成一條標準字符串
        
        length = random.randint(1000, 20000)*5 + random.choices([0, 2, 5], [0.6, 0.2, 0.2])[0]
        width = random.randint(1000, 20000)*5 + random.choices([0, 2, 5], [0.6, 0.2, 0.2])[0]
        height = random.randint(1000, 20000)*5 + random.choices([0, 2, 5], [0.6, 0.2, 0.2])[0]
        count1 += 1
        row1 = {
            "p_id": count1,
            "p_name": pname,
            "standard": standard,
            "length": length,
            "width": width,
            "height": height
        }
        
        all_p.append(row1)
        rand = random.randint(1, 5)
        for n in range(rand):
            inv_name = pname + " " + letters[n] 
            
            if isprime(count2) == True:
                status = "Not Using"
            else:
                status = "Using"
            row2 = {
                "inv_id": count2,
                "inv_name": inv_name,
                "status": status,
                "p_id": count1,
                "plane": plane_num[plane_num_m]
            }
            all_inv.append(row2)
            large_invs.append(row2)
        m += 1

plane_num = ["787-1", "787-2", "787-3", "787-4", "787-5", "787-6", "787-7", "787-8", "787-9", "787-10",
             "777-1", "777-2", "777-3", "777-4", "777-5", "777-6", "777-7",
             "767-1", "767-2", "767-3", "767-4", "767-5", "767-6", "767-7", "767-8", "767-9", "767-10", 
             "767-11", "767-12", "767-13", 
             "757-1", "757-2", "757-3", "757-4", "757-5", "757-6", "757-7", "757-8", "757-9", "757-10",
             "747-1", "747-2", "747-3",
             "737-1", "737-2", "737-3", "737-4", "737-5"]

dimensions = {
    "737": {"length": 39.5, "width": 34.3, "height": 12.5},
    "747": {"length": 70.6, "width": 64.4, "height": 19.4},
    "757": {"length": 47.3, "width": 35.8, "height": 13.0},
    "767": {"length": 48.5, "width": 47.6, "height": 13.1},
    "777": {"length": 73.8, "width": 60.9, "height": 18.5},
    "787": {"length": 56.7, "width": 51.7, "height": 15.8}
}

plane_invs = []

for plane in plane_num:
    count1 += 1
    model = plane.split("-")[0]
    if model in dimensions:
        length = dimensions[model]["length"]
        width = dimensions[model]["width"]
        height = dimensions[model]["height"]

    row1 = {
        "p_id": count1,
        "p_name": plane,
        "standard": standard,
        "length": length,
        "width": width,
        "height": height
    }
    
    all_p.append(row1)
    
    count2 += 1
    
    if plane == ("737-1" or "737-2" or "737-3" or "747-1" or "757-1" or "767-1" or "767-5"):
        row2 = {
            "inv_id": count2,
            "inv_name": plane,
            "status": "Not Using",
            "p_id": None,
            "plane": plane
        }
    else:
        row2 = {
            "inv_id": count2,
            "inv_name": plane,
            "status": "Using",
            "p_id": None,
            "plane": plane  
        }
    
    all_inv.append(row2)
    plane_invs.append(row2)
    
print(len(all_inv))
print(len(all_p))

data_p = pd.DataFrame(all_p)
data_inv = pd.DataFrame(all_inv)
data_inv = data_inv.iloc[:, :4]
data_small = pd.DataFrame(small_invs)
data_medium = pd.DataFrame(medium_invs)
data_large = pd.DataFrame(large_invs)
data_plane = pd.DataFrame(plane_invs)

items = []
# 獲取所有父零件和子零件的 inv_id
def add_relationships(parent_inv_df, child_inv_df, n1, n2, m1, m2):
    parent_ids = parent_inv_df["inv_id"].tolist()
    child_ids = child_inv_df["inv_id"].tolist()

    # 隨機選擇每個父零件的子零件數量（從 n1 到 n2 範圍內）
    for parent_inv_id in parent_ids:
        # 隨機選擇數量的子零件
        num_children = random.randint(n1, n2)

        # 隨機選擇 num_children 個子零件
        selected_children = random.sample(child_ids, num_children)

        # 為每個子零件建立父子關係
        for child_inv_id in selected_children:
            row = {
                "parent_inv": parent_inv_id,
                "child_inv": child_inv_id,
                "quantity": random.randint(m1, m2)  # 隨機選擇子零件的數量
            }
            items.append(row)


# 找到飛機零件的父子關係
for plane in plane_num:
    add_relationships(data_plane, data_large, 35, 60, 1, 10)
    add_relationships(data_large, data_medium, 15, 30, 2, 10)
    add_relationships(data_medium, data_small, 2, 10, 2, 10)
    
            
data_item = pd.DataFrame(items)

print(len(items))


# 確保資料夾存在，如果不存在則創建
folder_path = 'data_ff'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 儲存 CSV 檔案到資料夾中
file_path = os.path.join(folder_path, "item_f.csv")
data_item.to_csv(file_path, index=False)

file_path = os.path.join(folder_path, "part_f.csv")
data_p.to_csv(file_path, index=False)

file_path = os.path.join(folder_path, "inventory_f.csv")
data_inv.to_csv(file_path, index=False)
