import numpy as np
import matplotlib.pyplot as plt

# 
DAYS = 100
PRECIPITATION = np.random.uniform(0, 10, DAYS)  # (mm)
EVAPORATION = np.random.uniform(0, 5, DAYS)     # (mm)


soil_porosity = 0.4  # Porosity of the soil
hydraulic_conductivity = 0.05  #(mm/day)


initial_water_content = 100  #(mm)
initial_soil_moisture = 200  # Initial soil moisture content (mm)

soil_pH = 6.5   


def calculate_aquaporin_activity(pH):
    
    optimal_pH_range = (6.0, 7.0)
    
    
    activity = np.zeros_like(pH)
    
    
    activity = np.where(pH < optimal_pH_range[0], 0.5, activity)
    activity = np.where((optimal_pH_range[0] <= pH) & (pH <= optimal_pH_range[1]), 1.0, activity)
    activity = np.where(pH > optimal_pH_range[1], 0.7, activity)
    
    
    return np.mean(activity)


water_content_history = np.zeros(DAYS)
soil_moisture_history = np.zeros(DAYS)
aquaporin_activity_history = np.zeros(DAYS)


water_content_history[0] = initial_water_content
soil_moisture_history[0] = initial_soil_moisture


for day in range(1, DAYS):
    
    net_water_change = (PRECIPITATION[day] - EVAPORATION[day] +
                        hydraulic_conductivity * (soil_moisture_history[day-1] - soil_porosity * water_content_history[day-1]))


    soil_moisture_history[day] = soil_moisture_history[day-1] + net_water_change

 
    pH_fluctuations = np.random.normal(0, 0.5, DAYS) 
    soil_pH += pH_fluctuations[day]

    
    aquaporin_activity = calculate_aquaporin_activity(soil_pH)

    
    water_uptake = aquaporin_activity * min(soil_moisture_history[day - 1], initial_water_content)

   
    water_uptake = min(water_uptake, soil_moisture_history[day - 1])

   
    water_content_history[day] = water_content_history[day - 1] + water_uptake

   
    soil_moisture_history[day] -= water_uptake

  
    if water_content_history[day] < 0:
        water_content_history[day] = 0

    aquaporin_activity_history[day] = aquaporin_activity


time = np.arange(DAYS)

plt.figure(figsize=(10, 12))

plt.subplot(3, 1, 1)
plt.plot(time, water_content_history, label="Plant Water Content (mm)")
plt.xlabel("Time (days)")
plt.ylabel("Water Content (mm)")
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(time, soil_moisture_history, label="Soil Moisture (mm)")
plt.xlabel("Time (days)")
plt.ylabel("Soil Moisture (mm)")
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(time, aquaporin_activity_history, label="Aquaporin Activity")
plt.xlabel("Time (days)")
plt.ylabel("Aquaporin Activity")
plt.ylim(0, 1.1)
plt.legend()


plt.tight_layout()
plt.show()
