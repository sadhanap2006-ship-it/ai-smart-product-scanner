import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import re


st.title("AI Smart Product Scanner")

reader = easyocr.Reader(['en'])

uploaded_file = st.file_uploader("Upload Product Image", type=["jpg", "png", "jpeg"])

def extract_info(text):
    expiry = re.findall(r'\b\d{2}/\d{2}/\d{4}\b', text)
    mrp = re.findall(r'MRP\s?[:\-]?\s?\d+', text, re.IGNORECASE)

    allergens = []
    allergy_keywords = ["peanut", "milk", "soy", "gluten", "nuts"]
    for word in allergy_keywords:
        if word in text.lower():
            allergens.append(word)

    return expiry, mrp, allergens



if uploaded_file:
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    result = reader.readtext(img_array, detail=0)
    full_text = " ".join(result)

    expiry, mrp, allergens = extract_info(full_text)

    st.subheader("Detected Information")

    st.write("Expiry Date:", expiry)
    st.write("MRP:", mrp)
    st.write("Allergens:", allergens)

    speech_text = f"Expiry {expiry}. MRP {mrp}. Allergens {allergens}"
   
