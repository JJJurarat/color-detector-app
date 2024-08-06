import streamlit as st
from PIL import Image
import numpy as np
from st_clickable_images import clickable_images

# Function to extract RGB values
def extract_rgb(image):
    # Convert image to numpy array
    image_array = np.array(image)
    # Compute the average color of the image (ignoring alpha channel if present)
    if image_array.shape[2] == 4:  # Check if image has an alpha channel
        image_array = image_array[:, :, :3]
    avg_color_per_row = np.average(image_array, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    return avg_color.astype(int)

# Predefined colors and messages
predefined_colors = {
    "C7D7C9": "ปริมาณไอออนทองแดงในน้ำ มีความเข้มข้น 0.1M",
    "CED8CA": "ปริมาณไอออนทองแดงในน้ำ มีความเข้มข้น 0.01M",
    "C9D3C4": "ปริมาณไอออนทองแดงในน้ำ มีความเข้มข้น 0.05M",
    "B2BBA0": "ปริมาณไอออนทองแดงในน้ำ มีความเข้มข้น 0.005M",
    "B0B496": "ปริมาณไอออนทองแดงในน้ำ มีความเข้มข้น 0.001M",
    "CCCAB9": "ปริมาณไอออนทองแดงในน้ำ มีความเข้มข้น 0.00001M"
}

# Function to convert hex color code to RGB
def hex_to_rgb(hex_code):
    return np.array([int(hex_code[i:i+2], 16) for i in (0, 2, 4)])

# Function to get the closest color message
def get_color_message(detected_color, threshold=30):
    # Find the closest predefined color
    min_distance = float('inf')
    closest_message = "ไม่พบปริมาณไอออนทองแดงในน้ำ"
    for hex_code, message in predefined_colors.items():
        color_rgb = hex_to_rgb(hex_code)
        distance = np.linalg.norm(color_rgb - detected_color)
        if distance < min_distance:
            min_distance = distance
            closest_message = message
    # Check if the closest distance is within the threshold
    if min_distance > threshold:
        return "ไม่พบปริมาณไอออนทองแดงในน้ำ"
    return closest_message

# Streamlit app layout
st.set_page_config(page_title="Copper Detector", page_icon=":scientist:", layout="centered")

st.markdown(
    """
    <style>
    .main {
        background-color:  #f0deff  ;  /* light purple background */
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
    st.markdown("<h1 style='font-size: 30px;'>การตรวจจับอันตรายจากทองแดงที่ปนในน้ำ</h1>", unsafe_allow_html=True)
    st.markdown("---")
    with st.expander("อันตรายจากทองแดงที่ปนอยู่ในน้ำ"):
        st.markdown("<p style='font-size: 18px;'>ทองแดงเป็นธาตุที่พบได้ทั่วไปในธรรมชาติ ซึ่งทองแดงจะละลายออกมาในสภาวะเป็นกรด ปัจจุบันมีการกระจายของทองแดงในน้ำมากมายเช่น การปล่อยน้ำทิ้งของโรงงานอุตสาหกรรม การเติมคอปเปอร์ซัลเฟต(CuSO4)ลงสู่แหล่งน้ำเพื่อควบคุมการเจริญเติบโตของสาหร่ายในอ่างเก็บน้ำ การใช้สารเคมีกำจัดศัตรูพืช ยากำจัดเชื้อราในดิน รวมถึงน้ำดื่ม ทั้งนี้อย่างไรก็ตามหากพบมีทองแดงละลายป่นอยู่ในปริมาณที่สูงหรือมากเกินความต้องการของร่างกายเป็นเวลานาน ทองแดงอาจก่อความเป็นพิษเรื้อรัง ทำให้ตับและไตทำงานผิดปกติ ไม่สามารถขับทองแดงออกได้ จนทำให้เกิดโรคที่เรียกว่า‘‘โรควิลสัน’มา</p>", unsafe_allow_html=True)
    # for global use
    if not hasattr(st, 'counters'):
        st.counters = [0, 0]

    clicked = clickable_images(
        [
                "https://assets-global.website-files.com/62305b652c19ea5fafa8152f/63e1e2b6e07cdbf3b9db5047_%E0%B8%94%E0%B8%B5%E0%B9%84%E0%B8%8B%E0%B8%99%E0%B9%8C%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B9%84%E0%B8%A1%E0%B9%88%E0%B8%A1%E0%B8%B5%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%20(80).jpg?w=700",
                "https://assets-global.website-files.com/62305b652c19ea5fafa8152f/63e1e2ae2b23e2e793cbbb69_%E0%B8%94%E0%B8%B5%E0%B9%84%E0%B8%8B%E0%B8%99%E0%B9%8C%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B9%84%E0%B8%A1%E0%B9%88%E0%B8%A1%E0%B8%B5%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%20(78).jpg?w=700",
        ],
        titles=[f"Image #{str(i)}" for i in range(2)],
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "200px"},
    )


    with st.expander("วิธีการใช้กระดาษกรองเพื่อตรวจปริมาณทองแดงที่อยู่ในน้ำ"):
        st.markdown("""
    <ol style='font-size: 20px;'>
        <li>เตรียมกระดาษกรองที่อิ่มตัวจากสารสกัดแก้วมังกรและสารละลายบับเฟอร์ pH 7</li>
        <li>นำสารละลายตัวอย่าง ปริมาณ 1 หยด มาหยดลงบนกระดาษกรองที่อิ่มตัวจากสารสกัดแก้วมังกรและสารละลายบับเฟอร์ pH 7</li>
        <li>สังเกตการเปลี่ยนแปลงของสีเมื่อเวลาผ่านไป 1 นาที</li>
        <li>นำกระดาษกรองไปสแกนเข้าเว็บ <a href="https://copper-volum-by-color-detector.streamlit.app/" target="_blank">https://copper-volum-by-color-detector.streamlit.app/</a> เพื่อหาความเข้มข้นของคอปเปอร์ในสารละลายตัวอย่าง</li>
    </ol>
    """, unsafe_allow_html=True)


    st.markdown("---")
    st.markdown("<h2 style='font-size: 20px;'>สามารถถ่ายภาพหรืออัพโหลดผลการทดสอบที่ได้</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # Option to capture an image using the camera
    st.markdown("### ถ่ายภาพผลสีที่ได้ผ่านโทรศัพท์")
    
    uploaded_file_camera = st.camera_input("ถ่ายภาพ")

    # Option to upload an image from device
    st.markdown("### อัพโหลดรูปภาพผลที่ได้")
    uploaded_file = st.file_uploader("เลือกรูป...", type=["jpg", "jpeg", "png"])

    # Add a button to confirm the upload and change the page
    if uploaded_file_camera or uploaded_file:
        if st.button("ดูผลลัพธ์ที่ได้"):
            st.session_state.uploaded_file = uploaded_file_camera or uploaded_file
            st.session_state.page = "result"

def result_page():
    st.markdown("<h1 style='font-size: 26px;'>ผลลัพธ์ที่ได้จากการตรวจจับสีเพื่อทราบปริมาณทองแดง</h1>", unsafe_allow_html=True)
    st.markdown("---")

    uploaded_file = st.session_state.uploaded_file
    if uploaded_file is not None:
        # Convert the uploaded file to an image
        image = Image.open(uploaded_file)

        # Display the image
        st.image(image, caption='ภาพที่ประมวลผล', use_column_width=True)

        # Extract and display the RGB values
        rgb_values = extract_rgb(image)
        st.write(f"Dominant Color RGB: {rgb_values}")

        # Display the color
        st.markdown(
            f"<div class='color-box' style='background-color: rgb({rgb_values[0]}, {rgb_values[1]}, {rgb_values[2]});'></div>",
            unsafe_allow_html=True,
        )

        # Display the closest color message
        message = get_color_message(rgb_values)
        st.markdown(f"<h2 style='font-size: 24px; text-align: center;'>{message}</h2>", unsafe_allow_html=True)


         # If the color is predefined, show the warning message
        if message in predefined_colors.values():
            st.markdown(
                """
                <style>
                .danger-text {
                    color: red;
                    font-size: 20px;
                    font-weight: bold;
                    text-align: center;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown("<p class='danger-text'>อันตรายมาก!!</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 18px; color: #4a148c; text-align: center;'>เนื่องจากเกณฑ์กำหนดของการพบทองแดงในน้ำ</p>", unsafe_allow_html=True)
            message = get_color_message(rgb_values)
            st.markdown(f"<p style='font-size: 18px; color: #4a148c; text-align: center;'>{message}</h2>", unsafe_allow_html=True)


        st.markdown("---")
    if st.button("ถ่ายภาพใหม่หรืออัพโหลดรูปใหม่"):
        st.session_state.page = "home"

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# Display pages based on the state
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "result":
    result_page()
