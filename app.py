import streamlit as st
import pandas as pd
import joblib
from PIL import Image
import numpy as np

# Load model and data
model = joblib.load('final_xgboost_model.pkl')
df = pd.read_csv('cleaned_car_dataset.csv')
car_image = Image.open('car.png')

# ------------- Styling Functions -------------
def get_color(light_color, dark_color):
    return light_color if st.session_state.get("mode", "Light") == "Light" else dark_color

# ------------- Global CSS for Styling -------------
def apply_global_css():
    light_background = "#F5F5F5"
    dark_background = "#1E1E1E"
    light_text = "#333333"
    dark_text = "#FFFFFF"
    light_title = "#FF9933"
    dark_title = "#FF5733"
    light_headings = "#222222"
    dark_headings = "#FFEB3B"
    
    # Safe get mode
    mode = st.session_state.get("mode", "Light")
    page_background = light_background if mode == "Light" else dark_background
    title_color = light_title if mode == "Light" else dark_title
    text_color = light_text if mode == "Light" else dark_text
    heading_color = light_headings if mode == "Light" else dark_headings
    
    st.markdown(f"""
    <style>
        /* Global Styles */
        .stApp {{
            background-color: {page_background};
        }}
        h1, h2, h3, h4 {{
            color: {title_color};
        }}
        h1 {{
            font-size: 3em;
        }}
        h2 {{
            font-size: 2em;
        }}
        h3 {{
            font-size: 1.5em;
        }}
        h4 {{
            font-size: 1.2em;
        }}
        p, li, span, label {{
            color: {text_color};
            font-size: 1.2em;
        }}
        .stSidebar {{
            background-color: {light_background};
        }}
        .stButton {{
            background-color: {title_color};
            color: {text_color};
        }}
        .stButton:hover {{
            background-color: #FF5722;
        }}
        .stSelectbox, .stRadio, .stSlider {{
            color: {text_color};
        }}
        .stNumberInput input {{
            color: {text_color};
        }}
        .stImage img {{
            border-radius: 15px;
            border: 2px solid {light_title};
        }}
        .stAlert {{
            background-color: #FFEB3B;
            color: {dark_text};
        }}
    </style>
    """, unsafe_allow_html=True)

# ------------- Sidebar for Mode Selection -------------
if "mode" not in st.session_state:
    st.session_state["mode"] = "Light"
st.sidebar.title("Theme Settings")
mode = st.sidebar.radio("Select Theme Mode:", ["Light", "Dark"])
st.session_state["mode"] = mode

# Apply custom global CSS after initializing mode
apply_global_css()

# ------------- Main Heading -------------
st.markdown(
    f"<h1 style='text-align:center; color:{get_color('#FF9933', 'red')};'>Used Car Price Predictor in Indian Cities</h1>",
    unsafe_allow_html=True
)
st.markdown(
    f"<h4 style='text-align:center; color:{get_color('black','red' )}; font-weight:normal;'>Just enter the car details, you will get car price</h4>",
    unsafe_allow_html=True
)
st.markdown("---")

# ------------- Layout: Left (Image) and Right (Inputs) -------------
left_column, right_column = st.columns(2)

# --- Left Side ---
with left_column:
    st.image(car_image, caption="Your Dream Car Awaits!", use_column_width=True)

# --- Right Side ---
with right_column:
    st.markdown(
        f"<h2 style='text-align:center; color:{get_color('#FF9933', 'red')};'>Enter Car Details</h2>",
        unsafe_allow_html=True
    )

    # 1. Location
    st.markdown(f"<h4 style='color:{get_color('black', 'white')};'>Location</h4>", unsafe_allow_html=True)
    location = st.selectbox('Select Location', sorted(df['Location'].unique()))

    # 2. Brand
    st.markdown(f"<h4 style='color:{get_color('black', 'white')};'>Car Brand</h4>", unsafe_allow_html=True)
    brand = st.selectbox('Select Car Brand', sorted(df['Brand'].unique()))

    # 3. Model
    st.markdown(f"<h4 style='color:{get_color('black', 'white')};'>Car Model</h4>", unsafe_allow_html=True)
    model_options = df[df['Brand'] == brand]['Model'].unique()
    car_model = st.selectbox('Select Car Model', sorted(model_options)) if len(model_options) > 0 else None

    # 4. Car Type
    st.markdown(f"<h4 style='color:{get_color('black', 'white')};'>Car Type</h4>", unsafe_allow_html=True)
    type_options = df[(df['Brand'] == brand) & (df['Model'] == car_model)]['Car Type'].unique()
    car_type = st.selectbox('Select Car Type', sorted(type_options)) if len(type_options) > 0 else None

    # 5. Car Color
    st.markdown(f"<h4 style='color:{get_color('black', 'white')};'>Car Color</h4>", unsafe_allow_html=True)
    color_options = df[(df['Brand'] == brand) & (df['Model'] == car_model) & (df['Car Type'] == car_type)]['Color'].unique()
    car_color = st.selectbox('Select Car Color', sorted(color_options)) if len(color_options) > 0 else None

    # Split Columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<h4 style='color:{get_color('black', 'white')};'>Odometer Reading (km)</h4>", unsafe_allow_html=True)
        kms_driven = st.number_input('Enter KMs Driven', min_value=5000, max_value=200000, step=1000)

        st.markdown(f"<h4 style='color:{get_color('black', 'white')};'>Number of Owners</h4>", unsafe_allow_html=True)
        owner = st.radio('Number of Owners', sorted(df['Number of Owners'].unique()))

    with col2:
        st.markdown(f"<h4 style='color:{get_color('black', 'white')};'>Fuel Type</h4>", unsafe_allow_html=True)
        fuel_type = st.radio('Select Fuel Type', sorted(df['Fuel Type'].unique()))

        st.markdown(f"<h4 style='color:{get_color('black', 'white')};'>Transmission Type</h4>", unsafe_allow_html=True)
        transmission = st.radio('Select Transmission', sorted(df['Transmission Type'].unique()))

    # Manufactured Year
    st.markdown(f"<h4 style='color:{get_color('black', 'white')};'>Manufactured Year</h4>", unsafe_allow_html=True)
    year = st.slider('Select Manufactured Year', 2000, 2024, step=1)

    # Engine Capacity
    st.markdown(f"<h4 style='color:{get_color('black', 'white')};'>Engine Capacity (Litres)</h4>", unsafe_allow_html=True)
    engine_capacity = st.slider('Select Engine Capacity', 1.0, 5.0, step=0.1)

    # Split again
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(f"<h4 style='color:{get_color('black', 'white')};'>Previous Accidents</h4>", unsafe_allow_html=True)
        accidents = st.radio('Accident History', sorted(df['Previous Accidents'].unique()))

        st.markdown(f"<h4 style='color:{get_color('black', 'white')};'>Service History</h4>", unsafe_allow_html=True)
        service = st.radio('Service History', sorted(df['Service History'].unique()))

    with col4:
        st.markdown(f"<h4 style='color:{get_color('black', 'white')};'>Insurance Type</h4>", unsafe_allow_html=True)
        insurance = st.radio('Insurance Type', sorted(df['Insurance Type'].unique()))

# ------------- Predict Button -------------
st.markdown("---")
st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)

predict_btn = st.button("🚗 Predict Car Price 🚗")

if predict_btn:
    if all([location, brand, car_model, car_type, car_color, kms_driven, owner, fuel_type, transmission, year, engine_capacity, accidents, service, insurance]):
        with st.spinner('Predicting the best price for you...'):
            # Prepare input DataFrame 
            input_df = pd.DataFrame({
                'Year': [year],
                'Odometer Reading (km)': [kms_driven],
                'Engine Capacity (L)': [engine_capacity],
                # ... additional one-hot encoded features ...
            })
            # Model Prediction
            price = model.predict(input_df)
            # Output
            st.subheader(f"Predicted Car Price: ₹{round(price[0], 2)}")
    else:
        st.warning("Please fill in all the details.")
