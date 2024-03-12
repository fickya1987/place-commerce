from dotenv import load_dotenv
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import streamlit as st
from PIL import Image


load_dotenv()


genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

def detect_images(prompt, uploaded_img):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content ([prompt, uploaded_img[0]], 
                                       safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE 
        }
        )
    return response.text

    # except ValueError:
    #     # If the response doesn't contain text, check if the prompt was blocked.
    #     print(response.prompt_feedback)
    #     # Also check the finish reason to see if the response was blocked.
    #     print(response.candidates[0].finish_reason)
    #     # If the finish reason was SAFETY, the safety ratings have more details.
    #     print(response.candidates[0].safety_ratings)

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        
        image_parts = [
            {
                
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")


st.title("See, Snap, Learn !")
st.header(":orange[Upload Images of Historical Places]")
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg', 'webp'])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)  
        st.image(image, caption="Uploaded Image", use_column_width=True)
    except Exception as e:  
        st.error(f"Error processing image: {e}")



submit=st.button("Please Find More,Bro!🔎", type="primary")
prompt = """You are a business expert who is able to explain to people about Small Medium Enterprises (SMEs) in Asia Pacific (APAC) Region. Provide five until ten small medium enterprises (SMEs) which located nearby the place (according to the chosen image). Provide detail information about those small medium enterprises (SMEs) located in the place. place in bullet points(Such as business information, potential economic sector, regional government policy, potential money cna be generated in the place etc). 
Give a brief detail names of the small medium enterprises (SMEs) in the place. Provide the significance of business core in the place. Each section should have a heading."""


if submit:
    if uploaded_file is None:
        st.error("Please upload an image before submitting.")
    else:
        image_data = input_image_setup(uploaded_file)
        # with st.spinner('Just a moment...'):
        #     time.sleep(25)
        response = detect_images(prompt, image_data)
        
        st.subheader("Here's what we found 👀")
        st.write(response)
        st.info('Information provided may be inaccurate. Kindly double-check its responses', icon="ℹ")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

footer="""<style>
a:link , a:visited{
color: #8EA8C3;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: #7AE7C7;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
# background-color:#071013;
# color: #8EA8C3;
background: rgba(7, 16, 19, 0.24);
box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
backdrop-filter: blur(6.6px);
-webkit-backdrop-filter: blur(6.6px);
border: 1px solid rgba(7, 16, 19, 0.44);
text-align: center;
}
</style>
<div class="footer">
<p>Developed by Place2Joy Gaman - Ficky Alkarim</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
