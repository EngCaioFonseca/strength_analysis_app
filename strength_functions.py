import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime




# Set background image
def set_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Convert image to base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# Function to convert DataFrame to CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Function to convert DataFrame to Excel
def convert_df_to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

# Function to calculate 1RM (One-Rep Max)
def calculate_1rm(weight, reps):
    return 100 * weight / (101.3 - 2.67123 * reps)



# Function to plot all data points for a specific exercise
def plot_data_points(data, lift_type):
    exercise_data = data[data['Lift'] == lift_type]
    if exercise_data.empty:
        st.write(f'No data available for {lift_type}')
        return

    exercise_data['Timestamp'] = pd.to_datetime(exercise_data['Timestamp'])
    exercise_data = exercise_data.sort_values('Timestamp')

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 10))

        # Plot Load vs. Timestamp
    ax1.scatter(exercise_data['Timestamp'], exercise_data['Weight'], color='blue', label='Data Points')
    ax1.plot(exercise_data['Timestamp'], exercise_data['Weight'], color='red', label='Trend Line')
    ax1.set_title(f'{lift_type} - Load vs. Timestamp')
    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Weight (kg)')
    ax1.legend()

        # Calculate Volume (Load * Reps)
    exercise_data['Volume'] = exercise_data['Weight'] * exercise_data['Reps']

        # Plot Volume vs. Timestamp
    ax2.scatter(exercise_data['Timestamp'], exercise_data['Volume'], color='green', label='Data Points')
    ax2.plot(exercise_data['Timestamp'], exercise_data['Volume'], color='purple', label='Trend Line')
    ax2.set_title(f'{lift_type} - Volume vs. Timestamp')
    ax2.set_xlabel('Timestamp')
    ax2.set_ylabel('Volume (kg * reps)')
    ax2.legend()

    st.pyplot(fig)

def plot_donut_chart(data):
    lift_counts = data['Lift'].value_counts()
    fig, ax = plt.subplots(figsize=(18, 10), subplot_kw=dict(aspect="equal"))

    wedges, texts, autotexts = ax.pie(lift_counts, autopct='%1.1f%%', startangle=90, counterclock=False,
                                          wedgeprops=dict(width=0.3, edgecolor='w'))

    for w in wedges:
        w.set_linewidth(0.5)
        w.set_edgecolor('w')

    ax.legend(wedges, lift_counts.index,
                  title="Lifts",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=12, weight="bold")
    plt.setp(texts, size=12)

    ax.set_title('Lift Distribution')
    st.pyplot(fig)



# Function to plot force-time and power-time curves for a specific exercise
def plot_curves(data, lift_type):
    exercise_data = data[data['Lift'] == lift_type]
    if exercise_data.empty:
        st.write(f'No data available for {lift_type}')
        return

    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    # Force-Time Curve
    ax[0].plot(exercise_data['Time'], exercise_data['Weight'], marker='o')
    ax[0].set_title(f'{lift_type} - Force-Time Curve')
    ax[0].set_xlabel('Time (s)')
    ax[0].set_ylabel('Force (N)')

    # Power-Time Curve
    power = exercise_data['Weight'] * 9.81 * exercise_data['Time']  # Simplified power calculation
    ax[1].plot(exercise_data['Time'], power, marker='o')
    ax[1].set_title(f'{lift_type} - Power-Time Curve')
    ax[1].set_xlabel('Time (s)')
    ax[1].set_ylabel('Power (W)')

    st.pyplot(fig)


    
# Function for Variable Resistance Training recommendations
def vrt_recommendations(estimated_1rm):
    target_load = 0.85 * estimated_1rm
    band_load_top = 0.20 * target_load
    load_with_bands = target_load - (0.5 * band_load_top)
    
    st.write(f"Estimated 1RM: {estimated_1rm:.2f} kg")
    st.write(f"Target Load (85% of 1RM): {target_load:.2f} kg")
    st.write(f"Required Band Load at Top (20% of Target Load): {band_load_top:.2f} kg")
    st.write(f"Load to Replace with Plates and Bands: {load_with_bands:.2f} kg")
    st.write("Recommendation: Perform 5 sets of 5 reps with the calculated load.")

# Function for Eccentric Training recommendations
def eccentric_recommendations(estimated_1rm):
    target_eccentric_load = 1.20 * estimated_1rm
    
    st.write(f"Estimated 1RM: {estimated_1rm:.2f} kg")
    st.write(f"Target Eccentric Load (120% of 1RM): {target_eccentric_load:.2f} kg")
    st.write("Recommendation: Perform 3 sets of 3 reps at the target load, focusing on lowering the load under control for 3-4 seconds, with assistance on the concentric part of the lift.")


