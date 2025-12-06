import streamlit as streamlit
import requests
from PIL import Image

streamlit.set_page_config(
    page_title="Image Classifier",
    layout="centered"
)

streamlit.title("Image Classifier")
streamlit.write("Upload a jpeg file to classify it into one of the imagenet categories.")

# --- Input Form ---
uploaded_file = streamlit.file_uploader("Upload a .jpg file", type=["jpg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    streamlit.image(image, caption='Uploaded image.')

if streamlit.button("Predict"):

    if not uploaded_file:
        streamlit.warning("Please upload a .jpg file.")
    else:
        image = Image.open(uploaded_file)
        image_bytes = image.tobytes()
        try:
            files = {
                "file": (
                    'image_upload.jpg',
                    uploaded_file.getvalue(),
                    'image/jpeg'
                )
            }
            response = requests.post(
                "http://localhost:8000/api/predictions/",
                files=files,
            )

            if response.status_code == 200:
                prediction = response.json()
                streamlit.success(f"Class: {prediction['imagenet_class']}, Confidence: {prediction['probability']}")
            else:
                streamlit.error(f"API error {response.status_code}: {response.text}")
        except requests.exceptions.ConnectionError:
               streamlit.error("Could not connect to Django backend. Is the server running?")
