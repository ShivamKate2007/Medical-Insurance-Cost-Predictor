import streamlit as st
import pickle
import pandas as pd
import os
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Medical Insurance Cost Predictor",
    page_icon="🩺",
    layout="wide"  # Using a wider layout
)

# --- Model Loading ---
@st.cache_resource
def load_model():
    """Loads the pickled machine learning model."""
    file_path = os.path.join(os.path.dirname(__file__), 'Medical.pickle')
    with open(file_path, 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model()

# --- Sidebar Content ---
with st.sidebar:
    st.image("https://www.freeiconspng.com/thumbs/health-icon-png/health-icon-png-25.png", width=100)
    st.title("About Medical Insurance Cost Predictor")
    st.info(
        "This app uses machine learning to predict annual medical insurance costs. "
        "The goal is to help individuals understand potential healthcare expenses."
    )
    # Using an expander for a cleaner look
    with st.expander("How it Works"):
        st.markdown("""
            The prediction is based on these key features:
            - **Age & Sex:** Demographics of the beneficiary.
            - **BMI:** Body Mass Index, a key indicator of health.
            - **Children:** Number of dependents.
            - **Smoker:** Smoking status has a high impact on cost.
            - **Region:** The beneficiary's residential area in the US.
        """)
    st.write("---")
    st.markdown("Thanks For Reading!")


# --- Main Page UI ---
st.title("🩺 Medical Insurance Cost Predictor",anchor = False)
st.markdown("Fill in your details, and our model will estimate your insurance cost.")

# --- Creative Addition: Interactive BMI Calculator ---
st.markdown("### First, let's calculate your BMI")
height = st.slider("Your Height (cm)", 140, 220, 175)
weight = st.slider("Your Weight (kg)", 40, 150, 70)
bmi_calculated = round(weight / ((height / 100) ** 2), 2)
st.metric(label="Your Calculated BMI", value=bmi_calculated)

st.markdown("### Now, provide the rest of the details")

# --- Input Form in Columns ---
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", 18, 100, 30)
    sex = st.selectbox("Sex", ("Male", "Female"))
    children = st.number_input("Number of Children", 0, 10, 0)

with col2:
    smoker = st.selectbox("Are you a smoker?", ("Yes", "No"))
    region = st.selectbox("Your Region", ("Southwest", "Southeast", "Northwest", "Northeast"))
    # The BMI input is now read-only, showing the calculated value
    bmi = st.number_input("Body Mass Index (BMI)", value=bmi_calculated, disabled=True)


# --- Prediction Logic ---
if st.button("✨ Predict My Cost!", type="primary", use_container_width=True):
    # Convert inputs to the numerical format the model expects
    sex_num = 0 if sex == "Female" else 1
    smoker_num = 0 if smoker == "No" else 1
    region_map = {"southwest": 0, "southeast": 1, "northwest": 2, "northeast": 3}
    region_num = region_map[region.lower()]

    input_data = pd.DataFrame({
        'age': [age], 'sex': [sex_num], 'bmi': [bmi],
        'children': [children], 'smoker': [smoker_num], 'region': [region_num]
    })
    
    # Show a progress bar for a better user experience
    with st.spinner('Calculating...'):
        time.sleep(1) # Simulate a short delay
        prediction = model.predict(input_data)
        st.balloons() # Creative Addition: Celebrate a successful prediction!

    st.divider()
    st.subheader("📊 Prediction Result")
    
    # --- Creative Addition: Dynamic Result Display ---
    cost = prediction[0]
    st.metric(label="Estimated Annual Cost", value=f"${cost:,.2f}")

    if cost < 5000:
        st.info("This is a relatively low estimated cost. This could be due to a healthy BMI, non-smoking status, or younger age.", icon="✅")
    elif 5000 <= cost < 15000:
        st.warning("This is a moderate estimated cost. Factors like age or having dependents might be influencing this.", icon="⚠️")
    else:
        st.error("This is a high estimated cost. This is often linked to factors like smoking status or a higher BMI.", icon="🚨")


# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: grey;'>
        <p>© 2025 Shivam Kate / Medical Insurance Cost Predictor. All Rights Reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)