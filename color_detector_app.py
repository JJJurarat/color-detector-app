import streamlit as st
import cv2
from PIL import Image
import numpy as np

# Function to extract RGB values
def extract_rgb(image):
    # Convert image to numpy array
    image_array = np.array(image)
    # Compute the average color of the image
    avg_color_per_row = np.average(image_array, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    return avg_color.astype(int)

# Streamlit app layout
st.set_page_config(page_title="Color Detector", page_icon=":art:", layout="centered")

st.markdown(
    """
    <style>
    .main {
        background-color: #f3e5f5;  /* light purple background */
        color: #4a148c;  /* deep purple text */
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #ba68c8;  /* medium purple button */
        color: #ffffff;  /* white text on button */
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #8e24aa;  /* darker purple on hover */
    }
    .stCameraInput label, .stFileUploader label {
        background-color: #ec407a;  /* pink background */
        color: #ffffff;  /* white text */
        border-radius: 8px;
        padding: 10px;
        cursor: pointer;
    }
    .stCameraInput input, .stFileUploader input {
        display: none;
    }
    .stImage>div {
        border: 2px solid #4a148c;  /* deep purple border */
        border-radius: 8px;
        padding: 10px;
    }
    .stMarkdown div {
        text-align: center;
    }
    .color-box {
        display: inline-block;
        width: 100px;
        height: 100px;
        margin: 10px;
        border-radius: 8px;
        border: 2px solid #4a148c;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Define the pages
def home_page():
    st.title("Color Detector")
    st.markdown("## Capture an image and get the dominant color in RGB")
    st.markdown("---")

    # Option to capture an image using the camera
    st.markdown("### Capture an image using the camera")
    uploaded_file_camera = st.camera_input("Take a picture")

    # Option to upload an image from device
    st.markdown("### Or upload an image from your device")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    # Add a button to confirm the upload and change the page
    if uploaded_file_camera or uploaded_file:
        if st.button("Process Image"):
            st.session_state.uploaded_file = uploaded_file_camera or uploaded_file
            st.session_state.page = "result"

def result_page():
    st.title("Color Detector Results")
    st.markdown("---")

    uploaded_file = st.session_state.uploaded_file
    if uploaded_file is not None:
        # Convert the uploaded file to an image
        image = Image.open(uploaded_file)

        # Display the image
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Extract and display the RGB values
        rgb_values = extract_rgb(image)
        st.write(f"Dominant Color RGB: {rgb_values}")

        # Display the color
        st.markdown(
            f"<div class='color-box' style='background-color:rgb({rgb_values[0]},{rgb_values[1]},{rgb_values[2]});'></div>",
            unsafe_allow_html=True,
        )

    if st.button("Back to Home"):
        st.session_state.page = "home"

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Render the appropriate page
if st.session_state.page == "home":
    home_page()
else:
    result_page()
