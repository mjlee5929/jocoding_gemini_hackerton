import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold, GenerationConfig
import streamlit as st
from PIL import Image

genai.configure(api_key=os.environ['API_KEY'])

st.markdown("<h1 style='text-align: center;'>Combat power meter for cuteness and prettiness</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color:#DB7093;'>AI evaluates and comments on the beauty and cuteness of your pet.</h5>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>The score is between 0 and 100, try scoring 0 or 100!</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose your `.jpg, .png` file", type=['png', 'jpg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    model = genai.GenerativeModel('gemini-1.5-flash')
    generation_config = GenerationConfig(
        temperature=0,
        top_p=0.1,
        top_k=1,
        max_output_tokens=1024,
    )

    prompt_inst = """
    Instruction
    please express how pretty or cute my pet with a number between 0 and 100 and tell me the reasons. the response must be in JSON. 

    ### Example ###
    response: {'score': 100, 'reason': 'ear and eyes is cute}
    response: {'score': 80, ''reason': 'fur is nice'}
    response: {'score': 60, 'reason' : 'Wrinkled and hairless'}
    response: {'score': 65, 'reason' : 'Too muscular and aggressive'}
    response: {'score': 75, 'reason' : 'white fluffy and small size'}
    response: {'score': 85, 'reason' : 'smiling and lovely'}
    response: {'score': 40, 'reason' : 'It looks like it's going to be violent and attack.'}
    """
    response = model.generate_content(
        contents=[prompt_inst, image],
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    st.markdown("<h2 style='text-align: center;'>AI says : </h2>", unsafe_allow_html=True)
    st.markdown(response.text)
else:
    st.markdown("<h2 style='text-align: center;'>This is an example output.</h2>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Let's Go!</h2>", unsafe_allow_html=True)
    image = Image.open("example.png")
    st.image(image, use_column_width=True)
    