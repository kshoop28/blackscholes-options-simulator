import streamlit as st

# 1. Create selection mode
sidebar_mode = st.sidebar.radio("Select Settings Panel", ["Data Filters", "Model Hyperparameters"])

# 2. Dynamically swap the layout based on selection
if sidebar_mode == "Data Filters":
    st.sidebar.subheader("📅 Data Filters")
    start_date = st.sidebar.date_input("Start Date")
    category = st.sidebar.selectbox("Category", ["All", "Electronics", "Clothing"])
    
elif sidebar_mode == "Model Hyperparameters":
    st.sidebar.subheader("⚙️ Model Settings")
    learning_rate = st.sidebar.slider("Learning Rate", 0.001, 0.1, 0.01)
    epochs = st.sidebar.number_input("Epochs", min_value=1, value=10)

# Main App Content
st.title("Dynamic Sidebar Application")
st.write("The sidebar widgets change depending on your selection above!")
