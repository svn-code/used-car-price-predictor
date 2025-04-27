import streamlit as st
import pandas as pd
import joblib
from PIL import Image

# Load model and data
model = joblib.load('final_xgboost_model.pkl')
df = pd.read_csv('cleaned_car_dataset.csv')
car_image = Image.open('car.png')

# ------------- Styling Functions -------------
def get_color(light_color, dark_color):
    return light_color if st.session_state.get("mode", "Light") == "Light" else dark_color

# ------------- Sidebar for Mode Selection -------------
if "mode" not in st.session_state:
    st.session_state["mode"] = "Light"
st.sidebar.title("Theme Settings")
mode = st.sidebar.radio("Select Theme Mode:", ["Light", "Dark"])
st.session_state["mode"] = mode

# ------------- Global CSS for Styling -------------
def apply_global_css():
    light_background = "#F5F5F5"
    dark_background = "#1E1E1E"
    light_text = "#333333"
    dark_text = "#FFFFFF"
    light_title = "#FF9933"
    dark_title = "#FF5733"
    light_headings = "#222222"
    dark_headings = "#FFD700"  # A lighter yellow for dark mode
    dark_sidebar_background = "#2B2B2B"  # Dark background for sidebar
    dark_input_fields = "#3A3A3A"  # Dark color for input fields in dark mode
    
    page_background = light_background if st.session_state.get("mode", "Light") == "Light" else dark_background
    title_color = light_title if st.session_state.get("mode", "Light") == "Light" else dark_title
    text_color = light_text if st.session_state.get("mode", "Light") == "Light" else dark_text
    heading_color = light_headings if st.session_state.get("mode", "Light") == "Light" else dark_headings
    
    st.markdown(f"""
    <style>
        .stApp {{ background-color: {page_background}; }}
        h1, h2, h3, h4 {{ color: {heading_color}; }}
        h1 {{ font-size: 3em; }}
        h2 {{ font-size: 2em; }}
        h3 {{ font-size: 1.5em; }}
        h4 {{ font-size: 1.2em; }}
        p, li, span, label {{ color: {text_color}; font-size: 1.2em; }}
        .stSidebar {{ background-color: {dark_sidebar_background}; }}
        .stButton {{ background-color: {title_color}; color: {text_color}; }}
        .stButton:hover {{ background-color: #FF5722; }}
        .stSelectbox, .stRadio, .stSlider {{ color: {text_color}; }}
        .stNumberInput input {{ color: {text_color}; }}
        .stImage img {{ border-radius: 15px; border: 2px solid {light_title}; }}
        .stAlert {{ background-color: #FFEB3B; color: {dark_text}; }}
        .stSelectbox, .stRadio, .stButton, .stNumberInput input {{ background-color: {dark_input_fields}; color: {text_color}; }}
        .stSelectbox option, .stRadio input, .stButton {{ color: {text_color}; }}
    </style>
    """, unsafe_allow_html=True)

# Apply custom global CSS (after mode init)
apply_global_css()

# ------------- Main Heading -------------
st.markdown(
    f"<h1 style='text-align:center; color:{get_color('#FF9933', '#FF5733')};'>Used Car Price Predictor in Indian Cities</h1>",
    unsafe_allow_html=True
)
st.markdown(
    f"<h4 style='text-align:center; color:{get_color('black','white')}; font-weight:normal;'>Just enter the car details, you will get car price</h4>",
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
        f"<h2 style='text-align:center; color:{get_color('#FF9933', '#FF5733')};'>Enter Car Details</h2>",
        unsafe_allow_html=True
    )

    # 1. Location
    st.markdown(f"<h4 style='color:{get_color('black','white')};'>Location</h4>", unsafe_allow_html=True)
    location = st.selectbox('Select Location', sorted(df['Location'].unique()))

    # 2. Brand
    st.markdown(f"<h4 style='color:{get_color('black','white')};'>Car Brand</h4>", unsafe_allow_html=True)
    brand = st.selectbox('Select Car Brand', sorted(df['Brand'].unique()))

    # 3. Model
    st.markdown(f"<h4 style='color:{get_color('black','white')};'>Car Model</h4>", unsafe_allow_html=True)
    model_options = df[df['Brand'] == brand]['Model'].unique()
    car_model = st.selectbox('Select Car Model', sorted(model_options)) if len(model_options) > 0 else None

    # 4. Car Type
    st.markdown(f"<h4 style='color:{get_color('black','white')};'>Car Type</h4>", unsafe_allow_html=True)
    type_options = df[(df['Brand'] == brand) & (df['Model'] == car_model)]['Car Type'].unique()
    car_type = st.selectbox('Select Car Type', sorted(type_options)) if len(type_options) > 0 else None

    # 5. Car Color
    st.markdown(f"<h4 style='color:{get_color('black','white')};'>Car Color</h4>", unsafe_allow_html=True)
    color_options = df[(df['Brand'] == brand) & (df['Model'] == car_model) & (df['Car Type'] == car_type)]['Color'].unique()
    car_color = st.selectbox('Select Car Color', sorted(color_options)) if len(color_options) > 0 else None

    # Split Columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<h4 style='color:{get_color('black','white')};'>Odometer Reading (km)</h4>", unsafe_allow_html=True)
        kms_driven = st.number_input('Enter KMs Driven', min_value=5000, max_value=200000, step=1000)

        st.markdown(f"<h4 style='color:{get_color('black','white')};'>Number of Owners</h4>", unsafe_allow_html=True)
        owner = st.radio('Number of Owners', sorted(df['Number of Owners'].unique()))

    with col2:
        st.markdown(f"<h4 style='color:{get_color('black','white')};'>Fuel Type</h4>", unsafe_allow_html=True)
        fuel_type = st.radio('Select Fuel Type', sorted(df['Fuel Type'].unique()))

        st.markdown(f"<h4 style='color:{get_color('black','white')};'>Transmission Type</h4>", unsafe_allow_html=True)
        transmission = st.radio('Select Transmission', sorted(df['Transmission Type'].unique()))

    # Manufactured Year
    st.markdown(f"<h4 style='color:{get_color('black','white')};'>Manufactured Year</h4>", unsafe_allow_html=True)
    year = st.slider('Select Manufactured Year', 2000, 2024, step=1)

    # Engine Capacity
    st.markdown(f"<h4 style='color:{get_color('black','white')};'>Engine Capacity (Litres)</h4>", unsafe_allow_html=True)
    engine_capacity = st.slider('Select Engine Capacity', 1.0, 5.0, step=0.1)

    # Split again
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(f"<h4 style='color:{get_color('black','white')};'>Previous Accidents</h4>", unsafe_allow_html=True)
        accidents = st.radio('Accident History', sorted(df['Previous Accidents'].unique()))

        st.markdown(f"<h4 style='color:{get_color('black','white')};'>Service History</h4>", unsafe_allow_html=True)
        service = st.radio('Service History', sorted(df['Service History'].unique()))

    with col4:
        st.markdown(f"<h4 style='color:{get_color('black','white')};'>Insurance Type</h4>", unsafe_allow_html=True)
        insurance = st.radio('Insurance Type', sorted(df['Insurance Type'].unique()))

# ------------- Predict Button -------------
st.markdown("---")
st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)

predict_btn = st.button("🚗 Predict Car Price 🚗")

if predict_btn:
    if all([location, brand, car_model, car_type, car_color, kms_driven, owner, fuel_type, transmission, year, engine_capacity, accidents, service, insurance]):
        with st.spinner('Predicting the best price for you...'):
            input_df = pd.DataFrame({
                'Year': [year],
                'Odometer Reading (km)': [kms_driven],
                'Engine Capacity (L)': [engine_capacity],
                # Brands
                'Brand_BMW': [1 if brand == 'BMW' else 0],
                'Brand_Ford': [1 if brand == 'Ford' else 0],
                'Brand_Honda': [1 if brand == 'Honda' else 0],
                'Brand_Hyundai': [1 if brand == 'Hyundai' else 0],
                'Brand_Maruti Suzuki': [1 if brand == 'Maruti Suzuki' else 0],
                'Brand_Mercedes': [1 if brand == 'Mercedes' else 0],
                'Brand_Nissan': [1 if brand == 'Nissan' else 0],
                'Brand_Tata': [1 if brand == 'Tata' else 0],
                'Brand_Toyota': [1 if brand == 'Toyota' else 0],
                
                # Models
                'Model_A4': [1 if car_model == 'A4' else 0],
                'Model_A6': [1 if car_model == 'A6' else 0],
                'Model_Altroz': [1 if car_model == 'Altroz' else 0],
                'Model_C-Class': [1 if car_model == 'C-Class' else 0],
                'Model_City': [1 if car_model== 'City' else 0],
                'Model_Civic': [1 if car_model== 'Civic' else 0],
                'Model_Corolla': [1 if car_model== 'Corolla' else 0],
                'Model_Creta': [1 if car_model== 'Creta' else 0],
                'Model_Dzire': [1 if car_model== 'Dzire' else 0],
                'Model_E-Class': [1 if car_model== 'E-Class' else 0],
                'Model_EcoSport': [1 if car_model== 'EcoSport' else 0],
                'Model_Elantra': [1 if car_model== 'Elantra' else 0],
                'Model_Endeavour': [1 if car_model== 'Endeavour' else 0],
                'Model_Fiesta': [1 if car_model== 'Fiesta' else 0],
                'Model_Fortuner': [1 if car_model== 'Fortuner' else 0],
                'Model_Harrier': [1 if car_model== 'Harrier' else 0],
                'Model_Innova': [1 if car_model== 'Innova' else 0],
                'Model_Jazz': [1 if car_model== 'Jazz' else 0],
                'Model_Kicks': [1 if car_model== 'Kicks' else 0],
                'Model_M3': [1 if car_model== 'M3' else 0],
                'Model_Magnite': [1 if car_model == 'Magnite' else 0],
                'Model_Nexon': [1 if car_model== 'Nexon' else 0],
                'Model_Q5': [1 if car_model== 'Q5' else 0],
                'Model_S-Class': [1 if car_model== 'S-Class' else 0],
                'Model_Swift': [1 if car_model == 'Swift' else 0],
                'Model_Tiago': [1 if car_model == 'Tiago' else 0],
                'Model_Tiguan': [1 if car_model == 'Tiguan' else 0],
                'Model_Tucson': [1 if car_model == 'Tucson' else 0],
                'Model_Vento': [1 if car_model== 'Vento' else 0],
                'Model_X5': [1 if car_model == 'X5' else 0],
                
                # Features
                'Car Type_Sedan': [1 if car_type == 'Sedan' else 0],
                'Car Type_SUV': [1 if car_type == 'SUV' else 0],
                'Car Type_Hatchback': [1 if car_type == 'Hatchback' else 0],
                'Fuel Type_Petrol': [1 if fuel_type == 'Petrol' else 0],
                'Fuel Type_Diesel': [1 if fuel_type == 'Diesel' else 0],
                'Transmission Type_Automatic': [1 if transmission == 'Automatic' else 0],
                'Transmission Type_Manual': [1 if transmission == 'Manual' else 0],
                'Accident History_Yes': [1 if accidents == 'Yes' else 0],
                'Accident History_No': [1 if accidents == 'No' else 0],
                'Service History_Yes': [1 if service == 'Yes' else 0],
                'Service History_No': [1 if service == 'No' else 0],
                'Insurance Type_Comprehensive': [1 if insurance == 'Comprehensive' else 0],
                'Insurance Type_Liability': [1 if insurance == 'Liability' else 0],
            })
            
            # Predict and display result
            predicted_price = model.predict(input_df)
            st.write(f"**Predicted Car Price: ₹{predicted_price[0]:,.0f}**")
    else:
        st.warning("Please fill all the details before prediction!")
