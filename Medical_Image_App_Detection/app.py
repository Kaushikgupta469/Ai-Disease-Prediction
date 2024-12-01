import os
import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key  # Store your Gemini API key in `api_key.py`

# Configure the Gemini API with your key
genai.configure(api_key=api_key)

# Set up the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Define the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
)

# Define the prompt for medical image analysis
system_prompt = """
As a highly skilled practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Responsibilities:
1. Detailed Analysis: Document any observed anomalies or disease indicators.
2. Findings Report: Structure the findings clearly.
3. Recommendations and Next Steps: Suggest any further tests or treatments.
4. Treatment Suggestions: If applicable, recommend possible treatments.

Respond only if relevant to human health. Add Disclaimer "Consult with a Doctor before making any decisions."

Please provide me an output response with these 4 headings: Detailed Analysis, Findings Report, Recommendations and Next Steps, Treatment Suggestions.
"""

# Streamlit app setup
st.set_page_config(page_title="Medical Image Analytics", page_icon=":robot:")

# Display a logo and app title
st.image("logo.png", width=150)
st.title("👨‍⚕️ Vital💉Image📷 Analytics📊")
st.subheader("Application that helps to identify Disease based on images")

# Upload widget for the medical image
uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg", "jpeg"])

# Display the uploaded image immediately
if uploaded_file:
    st.image(
        uploaded_file,
        caption="Uploaded Medical Image",
        width=350,  # Adjust the width as needed
        output_format="JPEG",
    )

# Generate Analysis button triggers the processing of the image
if st.button("Generate The Analysis") and uploaded_file:
    # Save the uploaded image file temporarily for processing
    temp_file_path = Path("temp_image.jpg")
    temp_file_path.write_bytes(uploaded_file.getvalue())

    # Placeholder image description (in actual use, this should be updated with the image’s characteristics)
    image_description = "Image uploaded for analysis."

    # Generate the content based on the image description and prompt
    response = model.generate_content([
        image_description,
        system_prompt
    ])

    if response:
        st.title("Here is the analysis based in your image:")
        st.write(response.text)

    # Clean up by deleting the temporary file
    temp_file_path.unlink()
