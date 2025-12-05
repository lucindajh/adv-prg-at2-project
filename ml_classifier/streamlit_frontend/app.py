import streamlit as streamlit
import requests

streamlit.set_page_config(
    page_title="Text Classifier",
    layout="centered"
)

streamlit.title("News Topic Classifier")
streamlit.write("Enter a sentence or upload a plain-text file to classify it into one of 20 news categories.")

# --- Input Form ---
text_input = streamlit.text_area("Text input", height=150)
uploaded_file = streamlit.file_uploader("Optional: Upload a .txt file", type=["txt"])

if streamlit.button("Predict"):
    text_clean = text_input.strip()
    file_bytes = uploaded_file.getvalue() if uploaded_file else b""

    if not text_clean and not file_bytes:
        streamlit.warning("Please provide text or upload a .txt file.")
    else:
        try:
            if file_bytes:
                files = {
                    "file": (
                        uploaded_file.name or "upload.txt",
                        file_bytes,
                        "text/plain",
                    )
                }
                response = requests.post(
                    "http://localhost:8000/api/predict/",
                    data={"text": text_clean},
                    files=files,
                )
            else:
                response = requests.post(
                    "http://localhost:8000/api/predict/",
                    json={"text": text_clean},
                )

            if response.status_code == 200:
                prediction = response.json().get("prediction")
                streamlit.success(f"Prediction: {prediction}")
            else:
                streamlit.error(f"API error {response.status_code}: {response.text}")
        except requests.exceptions.ConnectionError:
            streamlit.error("Could not connect to Django backend. Is the server running?")