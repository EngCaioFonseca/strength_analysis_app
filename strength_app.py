import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from strength_functions import *
from strength_auth import *
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import base64
from io import BytesIO
from datetime import datetime




# Streamlit app
st.title('Strength and Power Analysis App')

# Set background image
#background_image_url = "https://images.unsplash.com/photo-1580261450046-d0a30080dc9b?q=80&w=2018&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"  # Replace with your image URL
#background_image_url = "https://images.unsplash.com/photo-1517963628607-235ccdd5476c?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
#background_image_url = "https://images.unsplash.com/photo-1504805572947-34fad45aed93?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
#background_image_url = "https://images.unsplash.com/photo-1685633224330-d2bd56d7adf1?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
background_image_url = "https://images.unsplash.com/photo-1685633225090-6b93b9b739b6?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"  # Replace with your image URL



set_background(background_image_url)



# Authentication form
auth_mode = st.sidebar.selectbox('Choose Authentication Mode', ['Login', 'Register'])

username = st.sidebar.text_input('Username')
password = st.sidebar.text_input('Password', type='password')

if auth_mode == 'Login':
    if st.sidebar.button('Login'):
        user = authenticate_user(username, password)
        if user:
            st.session_state['user_id'] = user.id
            st.session_state['data'] = load_user_data(user.id)
            st.success('Logged in successfully!')
        else:
            st.error('Invalid username or password')
else:
    if st.sidebar.button('Register'):
        register_user(username, password)
        st.success('Registered successfully! Please log in.')

# Initialize state variables if not already done
if 'selected_method' not in st.session_state:
    st.session_state['selected_method'] = None

if 'vrt_displayed' not in st.session_state:
    st.session_state['vrt_displayed'] = False

if 'eccentric_displayed' not in st.session_state:
    st.session_state['eccentric_displayed'] = False

# Check if user is authenticated
if 'user_id' in st.session_state:
    st.write(f"Welcome, {username}!")

    # Initialize data storage if not already initialized
    if 'data' not in st.session_state:
        st.session_state['data'] = load_user_data(st.session_state['user_id'])

    # Create columns for layout
    col1, col2 = st.columns([1, 1])

    # User input form in the first column
    with col1:
        with st.form(key='lift_form'):
            lift_type = st.selectbox('Lift Type', ['Squat', 'Bench Press', 'Deadlift', 'Row', 'Overhead Press', 'Pull-up', 'Dip'])
            weight = st.number_input('Weight (kg)', min_value=0.0)
            reps = st.number_input('Reps', min_value=1)
            time = st.number_input('Time (s)', min_value=0.0)
            submit_button = st.form_submit_button(label='Submit')

    # Add new data to database and session state
    if submit_button:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = pd.DataFrame({'Lift': [lift_type], 'Weight': [weight], 'Reps': [reps], 'Time': [time], 'Timestamp': [timestamp]})
        st.session_state['data'] = pd.concat([st.session_state['data'], new_data], ignore_index=True)
        
        db = SessionLocal()
        lift = Lift(user_id=st.session_state['user_id'], lift_type=lift_type, weight=weight, reps=reps, time=time, timestamp=timestamp)
        db.add(lift)
        db.commit()
        db.close()
        
        st.success('Data added!')

    # Display data
    st.write(st.session_state['data'])

    # Export data in the first column
    with col1:
        csv_data = convert_df_to_csv(st.session_state['data'])
        st.download_button(
            label="Download data as CSV",
            data=csv_data,
            file_name=f'{username}_lift_data.csv',
            mime='text/csv',
        )

        #excel_data = convert_df_to_excel(st.session_state['data'])
        #if excel_data:
        #    st.download_button(
        #        label="Download data as Excel",
        #        data=excel_data,
        #        file_name=f'{username}_lift_data.xlsx',
        #        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        #    )

        # Display 1RM estimations
        if not st.session_state['data'].empty:
            st.write('1RM Estimations:')
            st.session_state['data']['1RM'] = st.session_state['data'].apply(lambda row: calculate_1rm(row['Weight'], row['Reps']), axis=1)
            st.write(st.session_state['data'][['Lift', 'Weight', 'Reps', '1RM']])


    # Function to plot all data points for a specific exercise
    def plot_data_points(data, lift_type):
        exercise_data = data[data['Lift'] == lift_type]
        if exercise_data.empty:
            st.write(f'No data available for {lift_type}')
            return

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

        # Plot Load vs. Index
        ax1.scatter(exercise_data.index, exercise_data['Weight'], color='blue', label='Data Points')
        ax1.plot(exercise_data.index, exercise_data['Weight'], color='red', label='Trend Line')
        ax1.set_title(f'{lift_type} - Load vs. Index')
        ax1.set_xlabel('Index')
        ax1.set_ylabel('Weight (kg)')
        ax1.legend()

        # Calculate Volume (Load * Reps)
        exercise_data['Volume'] = exercise_data['Weight'] * exercise_data['Reps']

        # Plot Volume vs. Index
        ax2.scatter(exercise_data.index, exercise_data['Volume'], color='green', label='Data Points')
        ax2.plot(exercise_data.index, exercise_data['Volume'], color='purple', label='Trend Line')
        ax2.set_title(f'{lift_type} - Volume vs. Index')
        ax2.set_xlabel('Index')
        ax2.set_ylabel('Volume (kg * reps)')
        ax2.legend()

        st.pyplot(fig)

        # Charts in the second column
    with col2:
        # Allow user to select an exercise to view stats
        selected_exercise = st.selectbox('Select Exercise to View Stats', st.session_state['data']['Lift'].unique())
        plot_button = st.button('Plot Stats')

        if plot_button:
            plot_data_points(st.session_state['data'], selected_exercise)

        # Plot Donut Chart of Lift Distribution
        if not st.session_state['data'].empty:
            st.write("### Lift Distribution")
            plot_donut_chart(st.session_state['data'])

    # Advanced Training Methods
    st.write("## Advanced Training Methods")

    # Use buttons to select the training method
    if st.button("Variable Resistance Training"):
        st.session_state['selected_method'] = 'vrt'
        st.session_state['eccentric_displayed'] = False  # Ensure eccentric recommendations are not shown

    if st.button("Eccentric Training"):
        st.session_state['selected_method'] = 'eccentric'
        st.session_state['vrt_displayed'] = False  # Ensure VRT recommendations are not shown

    # Display the appropriate recommendations based on the selected method
    if st.session_state['selected_method'] == 'vrt':
        if not st.session_state['data'].empty:
            if '1RM' in st.session_state['data'].columns:
                estimated_1rm = st.session_state['data']['1RM'].max()
                vrt_recommendations(estimated_1rm)
            else:
                st.write("Please add some lift data to estimate the 1RM.")
        else:
            st.write("No data available. Please add your lifts to get recommendations.")
        st.session_state['vrt_displayed'] = True

    if st.session_state['selected_method'] == 'eccentric':
        if not st.session_state['data'].empty:
            if '1RM' in st.session_state['data'].columns:
                estimated_1rm = st.session_state['data']['1RM'].max()
                eccentric_recommendations(estimated_1rm)
            else:
                st.write("Please add some lift data to estimate the 1RM.")
        else:
            st.write("No data available. Please add your lifts to get recommendations.")
        st.session_state['eccentric_displayed'] = True
else:
    st.write("Please log in or register to access the app.")
