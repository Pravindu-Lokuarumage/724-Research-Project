import numpy as np
import csv
import math

# Define materials and their corresponding densities
densities = {'rubber': 1000, 'steel': 7850, 'plastic': 2800, 'wood':400, 'glass':2500, 'aluminum': 2700}
friction_coeff = {'rubber': 0.9, 'steel': 0.6, 'plastic': 0.35, 'wood':0.75, 'glass':0.5, 'aluminum':0.6 }
modulus = {'rubber': 0.05, 'steel': 210, 'plastic': 3, 'wood':12, 'glass':90, 'aluminum': 70}




# Define gripper parameters
gripper_width = 0.05  # m
gripper_depth = 0.05  # m
gripper_height = 0.05  # m
gripper_center = np.array([0, 0, 0.05])  # m

# Define ball parameters
ball_sizes = [0.02, 0.04, 0.06, 0.08, 0.1, 0.12]  # m
ball_materials = ['rubber', 'steel', 'plastic','wood','glass','aluminum']

# Define simulation parameters
num_simulations = 300

# Create CSV file
with open("gripper_data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    # Write header row
    header = ["Material","Size", "Gripper Force", "X Force", "Y Force", "Z Force", "X Torque", "Y Torque", "Z Torque", "Deflection"]
    writer.writerow(header)

    ## for size in ball_sizes:
        #grip_area = 2 * math.pi * size/2 * 0.01
    for material in ball_materials:
        for i in range(num_simulations):
            size = np.random.uniform(0.03,0.1) + np.random.uniform(-0.001, 0.001)
            size = math.ceil(size * 1000) / 1000
            density = densities[material]
            mass = density * (4/3) * np.pi * (size/2)**3
            inertia = (2/5) * mass * (size/2)**2
            print(f"Ball Size: {size}m, Material: {material}")
            # Generate random position for ball within the gripper
            x = np.random.uniform(-gripper_width/2, gripper_width/2)
            y = np.random.uniform(-gripper_depth/2, gripper_depth/2)
            z = np.random.uniform(-gripper_height/2, gripper_height/2)
            ball_pos = np.array([x, y, z])
            # Generate random gripper alignment 
            angle_offset = np.random.uniform(-90, 90)  # degrees

            # Convert the angle offset to radians
            angle_offset_rad = math.radians(angle_offset)

            # Calculate grip force for one grip claw
            grip_force = (mass * 9.81 * friction_coeff[material]) + np.random.uniform(-0.1, 0.1)
            grip_force = math.ceil(grip_force * 100) / 100

            #grip_force = 40 + np.random.uniform(-1 ,1)
            # Calculate force on each axis
            force_z = grip_force * math.cos(angle_offset_rad)
            force_x = grip_force * math.sin(angle_offset_rad)
            force_y = 0

            # Calculate torque on each axis
            torque_x = (ball_pos[1] - gripper_center[1]) * force_z - (ball_pos[2] - gripper_center[2]) * force_y
            torque_y = (ball_pos[2] - gripper_center[2]) * force_x - (ball_pos[0] - gripper_center[0]) * force_z
            torque_z = (ball_pos[0] - gripper_center[0]) * force_y - (ball_pos[1] - gripper_center[1]) * force_x

            deflection = (grip_force*size**3)/(3*modulus[material]*1000000000*(2/5) * densities[material] * (np.pi/6) * (size)**5) + np.random.uniform(-0.001, 0.001)
            row = [material,size,grip_force,force_x, force_y, force_z, torque_x, torque_y, torque_z,deflection]
            writer.writerow(row)
                
            print(f"Simulation {i+1}:")
            print(f"Force (X, Y, Z): ({force_x:.2f} N, {force_y:.2f} N, {force_z:.2f} N)")
            print(f"Torque (X, Y, Z): ({torque_x:.2f} Nm, {torque_y:.2f} Nm, {torque_z:.2f} Nm)")
            print("")
