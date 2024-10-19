from dotenv import load_dotenv
load_dotenv() # loading the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load gemini pro model
model=genai.GenerativeModel("gemini-1.5-pro")
def get_gemini_response(input, image, prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # read file into bytes
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type": uploaded_file.type, # get the mime type of uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# initialize streamlit app
st.set_page_config(page_title="Multilanguage Invoice Extractor")
st.header("Gemini Application")

input=st.text_input("Input Prompt: ", key="input")
uploaded_file=st.file_uploader("Choose an invoice...",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices. We will uploaded an invoice as image. You have to answer questions based on the invoice image.
"""

# if submit is clicked
if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is")
    st.write(response)

