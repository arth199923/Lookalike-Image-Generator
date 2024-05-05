import streamlit as st
import requests
import base64
import random
import io
from PIL import Image

# Define your Segmind API key
SegmindAPIKey = "SG_5a02e89ab1a1ecb4"

# Define your OpenAI API key
OpenAIKey = "sk-proj-2F1kMo0s4M4KP3xhKgTPT3BlbkFJOM9v6A7B7fBgjWFdnbj5"

# Define your functions here

def get_base64_image(uploaded_image):
    # Open the uploaded image
    image = Image.open(uploaded_image)
    
    # Convert image to JPEG format
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    
    # Encode image to base64
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def get_image_caption(image, caption_type):
    if caption_type == "A person smiling in a passport-style photo":
        return "smiling"
    elif caption_type == "Placeholder caption for the uploaded image":
        return "normalpic"
    elif caption_type == "A person with a sad expression in the photo":
        return "sad"
    else:
        return "Invalid caption type selected."

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

def process_image(uploaded_image, count, caption_type):
    base64image = get_base64_image(uploaded_image)
    imagecaption = get_image_caption(uploaded_image, caption_type)
    generated_images = generate_images(base64image, imagecaption, count)
    return imagecaption, generated_images

# Streamlit interface
def main():
    st.title("Discover Your Doppelgänger with AI, Crafted by Arth")
    st.markdown("📷 Upload your passport-style or similar photo to generate your look-alike")
    st.info("Please note: For faster results, upload a pic less than 500KB.")
    
    uploaded_image = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])

    if uploaded_image is not None:
        count = st.selectbox("Number of Images", options=[1, 2, 3, 4, 5])
        
        caption_type = st.radio("Choose how you'd like your look-alike to appear:?", 
                                options=["smiling face", 
                                         "Normal face", 
                                         "Sad face"])
        
        if st.button("Generate Images"):
            imagecaption, generated_images = process_image(uploaded_image, count, caption_type)
            
            st.text("AI Generated Caption:")
            st.text(imagecaption)

            # Display each generated image with its caption
            for i, image in enumerate(generated_images):
                st.image(image, caption=f"Generated Image {i+1}", width=200)

if __name__ == "__main__":
    main()
