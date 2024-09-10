# Strength and Power App


![image_2024_08_06T10_26_17_394Z](https://github.com/user-attachments/assets/c4750419-5fca-426b-97d5-83bc6cde80c1)



![VRT](https://github.com/user-attachments/assets/4c9b343c-99bf-4c24-a92b-43033f387175)

This Streamlit application allows users to track and analyze their strength training progress, providing insights and recommendations for advanced training methods.

## Features

- User authentication (login/register)
- Data input for various lift types
- 1RM (One Rep Max) estimation
- Data visualization (load and volume trends, lift distribution)
- Advanced training method recommendations (Variable Resistance Training and Eccentric Training)
- Data export (CSV)

## Dependencies

- streamlit
- pandas
- numpy
- matplotlib
- sqlalchemy
- base64
- datetime

## Main Components

1. **Authentication**: Users can register and log in to access their personal data.

2. **Data Input**: Users can input their lift data, including lift type, weight, reps, and time.

3. **Data Storage**: Lift data is stored in a database and loaded into the app's session state.

4. **Data Visualization**:
   - Load vs. Index plot
   - Volume vs. Index plot
   - Donut chart for lift distribution

5. **1RM Estimation**: Calculates and displays estimated 1RM for each lift.

6. **Advanced Training Methods**:
   - Variable Resistance Training (VRT) recommendations
   - Eccentric Training recommendations

7. **Data Export**: Users can download their data as a CSV file.

## Usage

1. Run the Streamlit app:
   ```
   streamlit run strength_app.py
   ```
2. Register or log in to access the app.
3. Input your lift data using the form.
4. View your data, charts, and 1RM estimations.
5. Explore advanced training method recommendations.
6. Export your data as needed.

## Note

This app requires additional files (`strength_functions.py` and `strength_auth.py`) for full functionality. Ensure these files are present in the same directory as the main app file.
