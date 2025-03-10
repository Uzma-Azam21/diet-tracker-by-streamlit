import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Custom CSS for UI
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
        font-family: 'Arial', sans-serif;
    }
    .stHeader {
        color: #4a4a4a;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stSidebar {
        background-color: #2c3e50;
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .stSidebar .stTextInput, .stSidebar .stNumberInput, .stSidebar .stSelectbox {
        background-color: #34495e;
        color: white;
        border-radius: 5px;
        padding: 10px;
    }
    .form-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
    .form-header {
        font-size: 24px;
        font-weight: bold;
        color: #4a4a4a;
        margin-bottom: 20px;
    }
    .form-label {
        font-size: 16px;
        font-weight: bold;
        color: #4a4a4a;
    }
    .form-input {
        margin-bottom: 15px;
    }
    .recommendation {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #4CAF50;
    }
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# App Title
st.title("🍏 NutriTrack - Your Personal Diet and Nutrition Tracker")

# Sidebar for User Input
st.sidebar.header("👤 User Profile")
user_name = st.sidebar.text_input("Enter your name:")
user_weight = st.sidebar.number_input("Enter your weight (kg):", min_value=30.0, max_value=200.0, value=70.0)
user_height = st.sidebar.number_input("Enter your height (cm):", min_value=100.0, max_value=250.0, value=170.0)
user_age = st.sidebar.number_input("Enter your age:", min_value=10, max_value=100, value=25)
user_activity_level = st.sidebar.selectbox("Select your activity level:", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"])

# Calculate Daily Calorie Needs (Harris-Benedict Equation)
def calculate_calories(weight, height, age, activity_level):
    bmr = 10 * weight + 6.25 * height - 5 * age + 5  # For males
    activity_multiplier = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    calories = bmr * activity_multiplier[activity_level]
    return calories

# Main App
st.header("🍽️ Track Your Daily Meals")

# Meal Input Form
with st.form("meal_form"):
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<div class="form-header">➕ Add a Meal</div>', unsafe_allow_html=True)
    
    # Meal Name
    st.markdown('<div class="form-label">Meal Name (e.g., Breakfast, Lunch)</div>', unsafe_allow_html=True)
    meal_name = st.text_input("Meal Name", placeholder="Enter meal name", key="meal_name", label_visibility="hidden")
    
    # Calories
    st.markdown('<div class="form-label">Calories (kcal)</div>', unsafe_allow_html=True)
    calories = st.number_input("Calories", min_value=0, value=300, key="calories", label_visibility="hidden")
    
    # Protein
    st.markdown('<div class="form-label">Protein (g)</div>', unsafe_allow_html=True)
    protein = st.number_input("Protein", min_value=0, value=10, key="protein", label_visibility="hidden")
    
    # Carbs
    st.markdown('<div class="form-label">Carbs (g)</div>', unsafe_allow_html=True)
    carbs = st.number_input("Carbs", min_value=0, value=40, key="carbs", label_visibility="hidden")
    
    # Fats
    st.markdown('<div class="form-label">Fats (g)</div>', unsafe_allow_html=True)
    fats = st.number_input("Fats", min_value=0, value=10, key="fats", label_visibility="hidden")
    
    # Submit Button
    submitted = st.form_submit_button("Add Meal")
    st.markdown('</div>', unsafe_allow_html=True)

# Initialize DataFrame to Store Meals
if "meals" not in st.session_state:
    st.session_state.meals = pd.DataFrame(columns=["Meal", "Calories", "Protein", "Carbs", "Fats"])

# Add Meal to DataFrame
if submitted:
    new_meal = pd.DataFrame({
        "Meal": [meal_name],
        "Calories": [calories],
        "Protein": [protein],
        "Carbs": [carbs],
        "Fats": [fats]
    })
    st.session_state.meals = pd.concat([st.session_state.meals, new_meal], ignore_index=True)
    st.success("Meal added successfully!")

    # Calculate Totals
    total_calories = st.session_state.meals["Calories"].sum()
    total_protein = st.session_state.meals["Protein"].sum()
    total_carbs = st.session_state.meals["Carbs"].sum()
    total_fats = st.session_state.meals["Fats"].sum()

    # Display Totals
    st.subheader("📊 Daily Totals")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Calories", f"{total_calories} kcal")
    col2.metric("Total Protein", f"{total_protein} g")
    col3.metric("Total Carbs", f"{total_carbs} g")
    col4.metric("Total Fats", f"{total_fats} g")

    # Visualize Data
    st.subheader("📈 Nutrition Breakdown")
    fig = px.pie(
        names=["Protein", "Carbs", "Fats"],
        values=[total_protein, total_carbs, total_fats],
        title="Macronutrient Distribution"
    )
    st.plotly_chart(fig)

    # Nutrition Recommendations
    st.header("💡 Nutrition Tips and Recommendations")
    if user_weight < 50:
        st.markdown('<div class="recommendation">Your weight is below the healthy range. Consider increasing your calorie intake with nutrient-rich foods.</div>', unsafe_allow_html=True)
    elif user_weight > 100:
        st.markdown('<div class="recommendation">Your weight is above the healthy range. Consider a balanced diet and regular exercise.</div>', unsafe_allow_html=True)

    if total_protein < 50:
        st.markdown('<div class="recommendation">You are not consuming enough protein. Add more protein-rich foods like eggs, chicken, and beans.</div>', unsafe_allow_html=True)
    if total_carbs < 100:
        st.markdown('<div class="recommendation">You are not consuming enough carbs. Add more carb-rich foods like rice, bread, and fruits.</div>', unsafe_allow_html=True)
    if total_fats < 30:
        st.markdown('<div class="recommendation">You are not consuming enough fats. Add more healthy fats like nuts, avocados, and olive oil.</div>', unsafe_allow_html=True)

# Display Meals
if not st.session_state.meals.empty:
    st.subheader("🍴 Your Meals")
    st.dataframe(st.session_state.meals)

# Download Data
st.subheader("📥 Download Your Data")
if not st.session_state.meals.empty:
    # Add User Info to DataFrame
    user_info = pd.DataFrame({
        "Name": [user_name],
        "Weight (kg)": [user_weight],
        "Height (cm)": [user_height],
        "Age": [user_age]
    })
    combined_data = pd.concat([user_info, st.session_state.meals], axis=1)

    # CSV Download
    csv = combined_data.to_csv(index=False).encode()
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="nutritrack_data.csv",
        mime="text/csv"
    )

    # Excel Download
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        combined_data.to_excel(writer, index=False)
    st.download_button(
        label="Download as Excel",
        data=excel_buffer.getvalue(),
        file_name="nutritrack_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )




