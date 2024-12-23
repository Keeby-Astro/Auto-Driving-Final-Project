# Auto Driving GPS Data Plot
# Names: Caden Matthews and Lin Tan

'''
-- Purpose:
This code convert the Latitude and Longitude coordinates of the GPS data of the
autonomous 2014 Nissan Leaf vehicle to X/Y coordinates centered at (0,0).

--Original Data is attached:
Loyd_nobel_nav_rosbag2_2024_11_11-11_24_51.csv

--Latitude Column Names:
Latitude - deg
1deg of Latitude (Miles), 1deg of Latitude (Feet), 1deg of Latitude (Metres)
1' of Latitude (Miles), 1' of Latitude (Feet), 1' of Latitude (Metres)
1'' of Latitude (Miles), 1'' of Latitude (Feet), 1'' of Latitude (Metres)

--Longitude Column Names:
Latitude - deg
1deg of Longitude (Miles), 1deg of Longitude (Feet), 1deg of Longitude (Metres)
1' of Longitude (Miles), 1' of Longitude (Feet), 1' of Longitude (Metres)
1'' of Longitude (Miles), 1'' of Longitude (Feet), 1'' of Longitude (Metres)

--Test Data Column Names:
Time, Longitude, Latitude, Speed[mps], Brake_status
'''

# Import the required libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import odeint
from scipy.optimize import minimize

# Load the CSV files
latitude_distance_to_latitude = pd.read_csv('latitude_distance_to_latitude.csv')
longitude_distance_to_longitude = pd.read_csv('longitude_distance_to_longitude.csv')

# Ask the user to select the dataset
dataset_choice = input("Type 1 for Lloyd Noble or type 2 for Reaves Park: ")

if dataset_choice == '1':
    test_data_final = pd.read_csv('Loyd_nobel_nav_rosbag2_2024_11_11-11_24_51.csv')
    test_data_final = test_data_final.iloc[15:].reset_index(drop=True)
elif dataset_choice == '2':
    test_data_final = pd.read_csv('Reaves_Park_acc_group_3_2024_11_22-15_49_50.csv')
    test_data_final = test_data_final.iloc[123:].reset_index(drop=True)
else:
    raise ValueError("Invalid input. Please type 1 or 2.")
test_data_final['Local_X'], test_data_final['Local_Y'] = convert_to_local_x_y(
    test_data_final, latitude_distance_to_latitude, longitude_distance_to_longitude
)

# Convert the longitude and latitude in the three test data set to local x and y in meters
# using the following tables
def convert_to_local_x_y(test_data):
    # Interpolate latitude to meters
    latitude_meters = np.interp(test_data['Latitude'], latitude_distance_to_latitude['Latitude - deg'],
                                 latitude_distance_to_latitude['1deg of Latitude (Metres)'])
    latitude_meters = latitude_meters * (test_data['Latitude'] - test_data['Latitude'].iloc[0])

    # Interpolate longitude to meters
    longitude_meters_per_degree = np.interp(test_data['Latitude'], longitude_distance_to_longitude['Latitude - deg'],
                                             longitude_distance_to_longitude['1deg of Longitude (Metres)'])
    longitude_meters = longitude_meters_per_degree * (test_data['Longitude'] - test_data['Longitude'].iloc[0])

    return longitude_meters, latitude_meters

# Apply conversion to all test data sets
for test_data in [test_data_final]:
    test_data['Local_X'], test_data['Local_Y'] = convert_to_local_x_y(test_data)
    test_data['Local_X'] -= test_data['Local_X'].iloc[0]
    test_data['Local_Y'] -= test_data['Local_Y'].iloc[0]

# Plot the x, y and make sure to use square window to show the x,y trajectory with equal x/y direction distance window
# Mark the starting point and end point with '*' and '<' respectively
plt.figure(figsize=(8, 8))
size = 100
plt.plot(test_data_final['Local_X'], test_data_final['Local_Y'], label='Test Data Final')
plt.scatter(test_data_final['Local_X'].iloc[0], test_data_final['Local_Y'].iloc[0], marker='*', color='g', s=size, label='Start Test Data')
plt.scatter(test_data_final['Local_X'].iloc[-1], test_data_final['Local_Y'].iloc[-1], marker='<', color='r', s=size, label='End Test Data')
plt.xlabel('Local X (m)')
plt.ylabel('Local Y (m)')
plt.title('Local X and Y Trajectory')
plt.axis('equal')
plt.legend()
plt.show()
