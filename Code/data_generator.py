"""
Data Generator for Food Delivery Time Prediction
Generates a realistic dataset with physical features impacting delivery time.
"""

import numpy as np
import pandas as pd

def generate_food_delivery_dataset(n_samples: int = 1500, random_state: int = 42) -> pd.DataFrame:
    """
    Generate synthetic yet realistic food delivery data.
    
    Features:
    - distance_km: Distance from restaurant to customer (1.0 to 18.0 km)
    - prep_time_min: Restaurant food preparation time (10 to 45 mins)
    - traffic_level: Congestion factor (1: Low, 2: Medium, 3: High, 4: Jam)
    - weather_condition: Weather impact (0: Clear, 1: Cloudy, 2: Rain, 3: Storm)
    - delivery_partner_rating: Rating out of 5 (3.2 to 5.0)
    - delivery_partner_age: Age of delivery rider (20 to 50 years)
    - num_items: Number of dishes in order (1 to 8)
    
    Target:
    - delivery_time_min: Total elapsed delivery time in minutes
    """
    np.random.seed(random_state)
    
    distance_km = np.round(np.random.uniform(1.0, 18.0, n_samples), 2)
    prep_time_min = np.round(np.random.normal(20, 6, n_samples), 1)
    prep_time_min = np.clip(prep_time_min, 8, 45)
    
    traffic_level = np.random.choice([1, 2, 3, 4], size=n_samples, p=[0.25, 0.40, 0.25, 0.10])
    weather_condition = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.50, 0.25, 0.18, 0.07])
    
    delivery_partner_rating = np.round(np.random.uniform(3.5, 5.0, n_samples), 2)
    delivery_partner_age = np.random.randint(20, 52, n_samples)
    num_items = np.random.choice([1, 2, 3, 4, 5, 6, 7], size=n_samples, p=[0.20, 0.35, 0.20, 0.12, 0.07, 0.04, 0.02])
    
    # Ground truth physics / dynamics:
    # Baseline overhead time: 5 minutes (parking, pickup, handover)
    # Travel time per km: ~2.2 mins/km under clear/low traffic
    # Traffic adds multiplier to transit time: traffic_level * 1.8 mins/km
    # Weather adds delay: weather * 2.5 mins
    # Prep time directly adds to delivery time: 0.95 * prep_time
    # High rating slightly reduces transit delay (-1.2 * (rating - 4.0))
    # Number of items adds small handling delay (0.8 * num_items)
    # Rider age has minor impact (0.05 * age)
    
    transit_speed_factor = 2.0 + (traffic_level * 0.9) + (weather_condition * 0.6)
    transit_time = distance_km * transit_speed_factor
    prep_contribution = prep_time_min * 0.92
    efficiency_bonus = (delivery_partner_rating - 4.0) * -1.5
    handling_time = num_items * 0.75 + (delivery_partner_age - 30) * 0.05
    noise = np.random.normal(0, 2.5, n_samples)  # Real-world measurement noise
    
    delivery_time_min = (
        6.0 
        + transit_time 
        + prep_contribution 
        + efficiency_bonus 
        + handling_time 
        + noise
    )
    
    # Clip to realistic lower bound (no delivery faster than 12 mins)
    delivery_time_min = np.round(np.clip(delivery_time_min, 12.0, 95.0), 1)
    
    df = pd.DataFrame({
        'distance_km': distance_km,
        'prep_time_min': prep_time_min,
        'traffic_level': traffic_level,
        'weather_condition': weather_condition,
        'delivery_partner_rating': delivery_partner_rating,
        'delivery_partner_age': delivery_partner_age,
        'num_items': num_items,
        'delivery_time_min': delivery_time_min
    })
    
    return df

if __name__ == '__main__':
    data = generate_food_delivery_dataset(n_samples=1500, random_state=42)
    output_path = 'food_delivery_data.csv'
    data.to_csv(output_path, index=False)
    print(f"Generated {len(data)} records saved to {output_path}")
    print("\nDataset Summary Preview:")
    print(data.head())
    print("\nStatistical Description:")
    print(data.describe())
