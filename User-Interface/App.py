import streamlit as st
import pandas as pd

# Load datasets
algorithm_data_path = 'algorithmdata_Data_Final.csv'
occupational_data_path = 'Occupational_Data_DF and DQ and Algorithm Function.csv'

occupational_df = pd.read_csv(occupational_data_path)
algorithm_df = pd.read_csv(algorithm_data_path)

# Clean and normalize Occupational Data
occupational_df['Algorithm Function'] = (
    occupational_df['Algorithm Function']
    .str.strip("[]")
    .str.replace("'", "", regex=False)
)
occupational_df = occupational_df.assign(
    Algorithm_Function=occupational_df['Algorithm Function'].str.split(',')
).explode('Algorithm_Function')
occupational_df['Algorithm_Function'] = occupational_df['Algorithm_Function'].str.strip()

# Clean and normalize Algorithm Data
algorithm_df['Algorithm Function'] = (
    algorithm_df['Algorithm Function']
    .str.strip("[]")
    .str.replace("'", "", regex=False)
)
algorithm_df = algorithm_df.assign(
    Algorithm_Function=algorithm_df['Algorithm Function'].str.split(',')
).explode('Algorithm_Function')
algorithm_df['Algorithm_Function'] = algorithm_df['Algorithm_Function'].str.strip()

# Convert numeric columns in Algorithm Data to numeric types
for col in [
    'Max Observations on One CPU',
    'Max Variables on One CPU',
    'max no of observations on one GPU ',
    ' Max no of variables on on GPU '
]:
    algorithm_df[col] = pd.to_numeric(algorithm_df[col].str.extract(r'(\d+)', expand=False), errors='coerce')

# Merge datasets
merged_data = pd.merge(
    algorithm_df, 
    occupational_df, 
    left_on='Algorithm_Function', 
    right_on='Algorithm_Function', 
    how='inner'
)

# Streamlit App
st.set_page_config(page_title="Algorithm Recommendation", layout="wide")

# Adding background GIF
def set_background(gif_path):
    with open(gif_path, "rb") as f:
        data = f.read()
    b64 = f"data:image/gif;base64,{data.hex()}"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url({b64});
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set your GIF path
gif_path = "Background.gif"  # Replace with the actual path to your GIF
set_background(gif_path)

# Dropdown Menus for Inputs
st.sidebar.header("Choose Your Requirements")
data_format = st.sidebar.selectbox(
    "Data Format",
    options=[""] + merged_data['Data Format'].dropna().unique().tolist()
)
data_quality = st.sidebar.selectbox(
    "Data Quality",
    options=[""] + merged_data['Data Quality'].dropna().unique().tolist()
)
data_type = st.sidebar.selectbox(
    "Data Type",
    options=[""] + merged_data['Data Type'].dropna().unique().tolist()
)
human_in_the_loop = st.sidebar.selectbox(
    "Human in the Loop",
    options=[""] + merged_data['Human-In-The-Loop'].dropna().unique().tolist()
)
algorithm_function = st.sidebar.selectbox(
    "Algorithm Function",
    options=[""] + merged_data['Algorithm_Function'].dropna().unique().tolist()
)

# Numeric Inputs
max_obs_cpu = st.sidebar.number_input("Max Observations on One CPU:", min_value=0, step=1)
max_vars_cpu = st.sidebar.number_input("Max Variables on One CPU:", min_value=0, step=1)
max_obs_gpu = st.sidebar.number_input("Max Observations on One GPU:", min_value=0, step=1)
max_vars_gpu = st.sidebar.number_input("Max Variables on One GPU:", min_value=0, step=1)
number_of_obs = st.sidebar.number_input("Number of Observations:", min_value=0, step=1)

# Filter Data
filtered_data = merged_data.copy()

if data_format:
    filtered_data = filtered_data[filtered_data['Data Format'].str.contains(data_format, case=False, na=False)]
if data_quality:
    filtered_data = filtered_data[filtered_data['Data Quality'].str.contains(data_quality, case=False, na=False)]
if data_type:
    filtered_data = filtered_data[filtered_data['Data Type'].str.contains(data_type, case=False, na=False)]
if human_in_the_loop:
    filtered_data = filtered_data[filtered_data['Human-In-The-Loop'].str.contains(human_in_the_loop, case=False, na=False)]
if algorithm_function:
    filtered_data = filtered_data[filtered_data['Algorithm_Function'].str.contains(algorithm_function, case=False, na=False)]
if max_obs_cpu > 0:
    filtered_data = filtered_data[filtered_data['Max Observations on One CPU'] <= max_obs_cpu]
if max_vars_cpu > 0:
    filtered_data = filtered_data[filtered_data['Max Variables on One CPU'] <= max_vars_cpu]
if max_obs_gpu > 0:
    filtered_data = filtered_data[filtered_data['max no of observations on one GPU '] <= max_obs_gpu]
if max_vars_gpu > 0:
    filtered_data = filtered_data[filtered_data[' Max no of variables on on GPU '] <= max_vars_gpu]
if number_of_obs > 0:
    filtered_data = filtered_data[filtered_data['Number of observations'].str.extract(r'(\d+)', expand=False).astype(float) <= number_of_obs]

# Get Distinct Algorithms
distinct_algorithms = filtered_data[['Algorithm ', 'Description']].drop_duplicates()

# Display Results
if not distinct_algorithms.empty:
    st.subheader("Algorithms Best Suited For Your Requirements")
    st.table(distinct_algorithms.reset_index(drop=True))  # Exclude index while displaying
else:
    st.subheader("No matching algorithms found. Please adjust your Requirements.")

