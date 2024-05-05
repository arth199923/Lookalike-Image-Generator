import streamlit as st
import requests
import base64
import random
import io
from PIL import Image

# Define your Segmind API key
SegmindAPIKey = "SG_4ec6a76090edb729"

# Define your OpenAI API key
OpenAIKey = "sk-proj-SjrP1D7dphvzMIL6C9oXT3BlbkFJbOfYgMozDALea6Gj9zRx"

# Define your functions here

def get_base64_image(uploaded_image):
    # Open the uploaded image
    image = Image.open(uploaded_image)
    
    # Convert image to JPEG format
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    
    # Encode image to base64
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def get_image_caption(image):
    return "Placeholder caption for the uploaded image."

def generate_images(base64image, imagecaption, count):
    url = "https://api.segmind.com/v1/ssd-img2img"
    generated_images = []

    for i in range(count):
        currentseed = random.randint(1000, 1000000)

        # Prepare the request payload
        data = {
            "image": base64image,
            "prompt": imagecaption + ", stock photo",
            # Add other parameters as required by the API
        }

        # Send a POST request to the API
        response = requests.post(url, json=data, headers={'x-api-key': SegmindAPIKey})

        if response.status_code == 200 and response.headers.get('content-type') == 'image/jpeg':
            # Convert the image data to a PIL image
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            generated_images.append(image)

    return generated_images

def process_image(uploaded_image, count):
    base64image = get_base64_image(uploaded_image)
    imagecaption = get_image_caption(uploaded_image)
    generated_images = generate_images(base64image, imagecaption, count)
    return imagecaption, generated_images

# Streamlit interface
def main():
    st.title("Discover Your Doppelgänger with AI, Crafted by Arth")
    st.markdown("📷 Upload your passport-style or similar photo to generate your look-alike")
    st.info("Please note: For faster results, upload a pic less than 500KB.")
    
    uploaded_image = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])

    if uploaded_image is not None:
        count = st.selectbox("Number of Images", options=[1, 2, 3])
        
        if st.button("Generate Images"):
            imagecaption, generated_images = process_image(uploaded_image, count)

            st.text("AI Generated Caption:")
            st.text(imagecaption)

            # Display each generated image with its caption
            for i, image in enumerate(generated_images):
                st.image(image, caption=f"Generated Image {i+1}", width=200)
                
if __name__ == "__main__":
    main()
