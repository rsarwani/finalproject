# synthetic_restaurant_sales.py

import os
import pandas as pd
import numpy as np
import random
import string
from datetime import datetime, timedelta

def random_txn_id(n=9):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

def seasonal_weather_and_temp(ts, loc):
    m = ts.month
    if loc == 'NYC':
        avgs = {1:32,2:35,3:45,4:55,5:65,6:75,7:80,8:79,9:70,10:60,11:50,12:38}
        if m in (12,1,2):
            conds, probs = ['Snow','Cloudy','Sunny','Rain'], [0.3,0.3,0.2,0.2]
        elif m in (3,4,10,11):
            conds, probs = ['Rain','Cloudy','Sunny','Drizzle'], [0.4,0.3,0.2,0.1]
        else:
            conds, probs = ['Sunny','Cloudy','Rain','Drizzle'], [0.6,0.2,0.15,0.05]
    else:  # LA
        avgs = {1:58,2:60,3:62,4:65,5:68,6:72,7:75,8:76,9:75,10:70,11:64,12:58}
        if m in (12,1,2):
            conds, probs = ['Sunny','Cloudy','Drizzle'], [0.6,0.3,0.1]
        elif m in (3,4,10,11):
            conds, probs = ['Sunny','Cloudy','Rain'], [0.7,0.2,0.1]
        else:
            conds, probs = ['Sunny','Cloudy','Drizzle'], [0.8,0.15,0.05]
    weather = np.random.choice(conds, p=probs)
    temp = round(np.random.normal(avgs[m], 5), 1)
    return weather, temp

def build_menus():
    return {
      'Italian': {
        'Breakfast': [
          ('Frittata', 10.00), ('Italian Breakfast Sandwich', 9.50),
          ('Ricotta Pancakes', 11.00), ('Espresso', 3.00),
          ('Cappuccino', 4.50), ('Fresh Fruit Plate', 8.00),
          ('Prosciutto & Melon', 12.00), ('Breakfast Bruschetta', 9.00),
          ('Yogurt Parfait', 7.50), ('Latte', 4.00)
        ],
        'Lunch': [
          ('Bruschetta', 8.50), ('Margherita Pizza', 12.00),
          ('Fettuccine Alfredo', 14.00), ('Caprese Salad', 11.00),
          ('Lasagna', 15.00), ('Minestrone Soup', 7.00),
          ('Panini', 10.50), ('Chianti (glass)', 9.00),
          ('Espresso', 3.00), ('Gelato', 6.00)
        ],
        'Dinner': [
          ('Antipasto Platter', 14.00), ('Bistecca Fiorentina', 35.00),
          ('Seafood Risotto', 24.00), ('Osso Buco', 28.00),
          ('Tiramisu', 8.00), ('Arancini', 9.00),
          ('Gnocchi Sorrentina', 18.00), ('Chianti (bottle)', 45.00),
          ('Limoncello', 7.00), ('Affogato', 7.50)
        ]
      },
      'Indian': {
        'Breakfast': [
          ('Masala Dosa', 9.00), ('Idli & Sambar', 8.50),
          ('Paratha', 7.00), ('Chai Tea', 3.00),
          ('Upma', 8.00), ('Poori Bhaji', 8.50),
          ('Paneer Toast', 9.00), ('Filter Coffee', 3.50),
          ('Fruit Chaat', 6.50), ('Lassi Sweet', 4.00)
        ],
        'Lunch': [
          ('Samosa', 5.00), ('Butter Chicken', 15.00),
          ('Palak Paneer', 14.00), ('Biryani', 16.00),
          ('Naan', 2.50), ('Tandoori Chicken', 18.00),
          ('Chole Bhature', 12.00), ('Mango Lassi', 4.50),
          ('Gulab Jamun', 5.50), ('Raita', 3.00)
        ],
        'Dinner': [
          ('Lamb Rogan Josh', 22.00), ('Paneer Tikka Masala', 18.00),
          ('Dal Makhani', 14.00), ('Naan Basket', 8.00),
          ('Chicken Tikka', 17.00), ('Biryani Feast', 20.00),
          ('Saag Gosht', 21.00), ('Masala Chai', 3.50),
          ('Jalebi', 6.00), ('Kulfi', 5.50)
        ]
      },
      'Thai': {
        'Breakfast': [
          ('Thai Omelette', 8.00), ('Jok (Rice Porridge)', 7.50),
          ('Patongo', 5.00), ('Thai Iced Coffee', 4.00),
          ('Sticky Rice & Mango', 6.50), ('Papaya Salad', 7.00),
          ('Coconut Pancakes', 8.50), ('Fruit Smoothie', 5.50),
          ('Tea', 2.50), ('Congee', 6.00)
        ],
        'Lunch': [
          ('Spring Rolls', 6.00), ('Pad Thai', 13.00),
          ('Green Curry', 14.50), ('Tom Yum Soup', 7.00),
          ('Massaman Curry', 15.00), ('Papaya Salad', 8.00),
          ('Satay Skewers', 9.00), ('Thai Iced Tea', 4.00),
          ('Mango Sticky Rice', 6.00), ('Fried Rice', 11.00)
        ],
        'Dinner': [
          ('Drunken Noodles', 14.00), ('Panang Curry', 16.00),
          ('Seafood Platter', 25.00), ('Larb Gai', 12.00),
          ('Tom Kha Gai', 9.00), ('Coconut Shrimp', 13.00),
          ('Thai Beef Salad', 17.00), ('Singha (beer)', 6.00),
          ('Sticky Rice & Mango', 6.00), ('Thai Tea Float', 5.00)
        ]
      },
      'Mexican': {
        'Breakfast': [
          ('Chilaquiles', 9.50), ('Breakfast Burrito', 8.00),
          ('Huevos Rancheros', 10.00), ('Cafe de Olla', 3.00),
          ('Atole', 3.50), ('Pan Dulce', 4.00),
          ('Fruit Plate', 7.00), ('Tacos al Pastor', 9.00),
          ('Mexican Omelette', 8.50), ('Agua Fresca', 4.00)
        ],
        'Lunch': [
          ('Guacamole & Chips', 7.00), ('Tacos (3)', 12.00),
          ('Enchiladas', 13.50), ('Quesadilla', 11.00),
          ('Pozole', 12.00), ('Tamales', 10.00),
          ('Churros', 5.50), ('Margarita', 8.50),
          ('Horchata', 3.50), ('Sopa de Lima', 9.00)
        ],
        'Dinner': [
          ('Carne Asada', 18.00), ('Mole Poblano', 17.00),
          ('Seafood Fajitas', 22.00), ('Chiles Rellenos', 16.00),
          ('Elote', 5.00), ('Michelada', 7.00),
          ('Birria Latte', 6.50), ('Tostada', 9.50),
          ('Flan', 6.00), ('Tequila Flight', 15.00)
        ]
      },
      'Mediterranean': {
        'Breakfast': [
          ('Shakshuka', 9.00), ('Labneh Plate', 8.00),
          ('Feta Omelette', 10.00), ('Turkish Coffee', 3.50),
          ('Baklava', 5.00), ('Fruit Salad', 7.00),
          ('Za’atar Manakish', 8.50), ('Mint Tea', 3.00),
          ('Olive Plate', 6.00), ('Greek Yogurt', 7.00)
        ],
        'Lunch': [
          ('Hummus Plate', 8.00), ('Gyro Platter', 13.00),
          ('Falafel Wrap', 9.00), ('Tabbouleh', 7.50),
          ('Shawarma', 12.00), ('Dolma', 8.00),
          ('Baklava', 5.50), ('Ouzo (glass)', 7.50),
          ('Turkish Coffee', 3.50), ('Greek Salad', 9.00)
        ],
        'Dinner': [
          ('Lamb Kofta', 18.00), ('Moussaka', 16.00),
          ('Seafood Mezze', 22.00), ('Chicken Souvlaki', 15.00),
          ('Briam', 12.00), ('Spanakopita', 9.00),
          ('Ouzo Flight', 12.00), ('Baklava', 6.00),
          ('Turkish Delight', 5.50), ('Red Wine (glass)', 9.00)
        ]
      }
    }

def generate_sales_data(
    num_txns=50000,
    num_rest=5,
    start_date=datetime(2024,1,1),
    days_period=90
):
    cuisines    = list(build_menus().keys())
    menus       = build_menus()

    order_types = ['Dine-in','Takeout','Delivery','Catering']
    sizes       = [1,2,3,4,5,6,8,10,15,20,30,50]
    size_p      = [0.20,0.20,0.15,0.10,0.10,0.08,0.05,0.04,0.04,0.02,0.01,0.01]
    base_items  = [1,2,3,4,5]
    base_p      = [0.10,0.20,0.40,0.20,0.10]

    np.random.seed(42)
    random.seed(42)

    columns = [
        'restaurant_id','cuisine','transaction_id','transaction_time','date',
        'day_of_week','time_of_day','party_size','item_name','quantity',
        'item_price','transaction_amount','payment_method','order_type',
        'is_weekend','weather','temperature_f'
    ]
    records = {c:[] for c in columns}

    for _ in range(num_txns):
        # --- setup transaction metadata ---
        rid     = random.randint(0, num_rest-1)
        cuisine = cuisines[rid]
        txn_id  = random_txn_id()
        ts      = start_date + timedelta(
                    days=random.randint(0, days_period-1),
                    seconds=random.randint(0,86399)
                  )
        date_s   = ts.date().isoformat()
        wd       = ts.strftime('%A')
        wknd     = ts.weekday() >= 5
        hr       = ts.hour
        if 6 <= hr < 11: meal='Breakfast'
        elif 11 <= hr < 15: meal='Lunch'
        elif 17 <= hr < 22: meal='Dinner'
        else: meal=random.choice(['Lunch','Dinner'])
        loc, weather, temp = (
            ('NYC',)+seasonal_weather_and_temp(ts,'NYC')
            if rid%2==0 else
            ('LA',)+seasonal_weather_and_temp(ts,'LA')
        )
        party_size = np.random.choice(sizes, p=size_p)
        n_items    = sum(np.random.choice(base_items, p=base_p)
                         for _ in range(party_size))
        order_type = random.choices(order_types, weights=[0.5,0.15,0.15,0.20])[0]

        # --- build item rows and sum spend ---
        temp_rows = []
        total_food = 0.0
        for __ in range(n_items):
            item, price = random.choice(menus[cuisine][meal])
            qty = random.randint(1,2)
            amt = round(price*qty,2)
            total_food += amt
            temp_rows.append((item, price, qty, amt))

        # --- conditional payment logic ---
        if total_food > 100:
            pm_choices = ['Swipe/Insert Card','Cash','Tap to Pay']
            pm_weights = [0.5,0.3,0.2]
        else:
            pm_choices = ['Tap to Pay','Swipe/Insert Card','Cash']
            pm_weights = [0.5,0.3,0.2]
        payment = random.choices(pm_choices, weights=pm_weights, k=1)[0]

        # --- append each item row with chosen payment ---
        for item, price, qty, amt in temp_rows:
            for col,val in [
              ('restaurant_id',rid),('cuisine',cuisine),
              ('transaction_id',txn_id),('transaction_time',ts),
              ('date',date_s),('day_of_week',wd),
              ('time_of_day',meal),('party_size',party_size),
              ('item_name',item),('quantity',qty),
              ('item_price',price),('transaction_amount',amt),
              ('payment_method',payment),('order_type',order_type),
              ('is_weekend',wknd),('weather',weather),
              ('temperature_f',temp)
            ]:
                records[col].append(val)

    df = pd.DataFrame(records)

    # --- tip logic as before ---
    tip_stats = {'Dine-in':(0.18,0.05),'Delivery':(0.15,0.05),
                 'Takeout':(0.10,0.03),'Catering':(0.20,0.05)}
    def sample_pct(o):
        mu,sd = tip_stats.get(o,(0.12,0.04))
        return np.clip(np.random.normal(mu,sd),0,0.40)

    food = df.groupby('transaction_id')['transaction_amount']\
             .sum().rename('total_food_spend')
    ot   = df.groupby('transaction_id')['order_type']\
             .first().rename('order_type')
    pct  = ot.map(sample_pct)
    tip_amount = (food * pct).round(2).rename('tip_amount')

    return df.merge(tip_amount, on='transaction_id')

if __name__=="__main__":
    out = "synthetic_restaurant_sales.csv"
    if os.path.exists(out): os.remove(out)
    df = generate_sales_data(num_txns=50000)
    df.to_csv(out, index=False)
    print(f"Saved {len(df)} rows to {out}")
