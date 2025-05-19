import streamlit as st
import pandas as pd
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Sound-Color Association Experiment", layout="centered")
st.title("🎧 Sound and Color Association Experiment")

# Google Sheets authorization
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gcp_service_account"], scope
)
client = gspread.authorize(credentials)

# Open the target Google Sheet
sheet = client.open("Sound2ColorOutcome").sheet1

# 👤 Participant info
name = st.text_input("👤 Please enter your name")
age = st.number_input("🎂 Please enter your age", min_value=0, max_value=120, step=1)

sound_numbers = [1, 2, 3]
colors = []

for sound_num in sound_numbers:
    st.markdown(f"### 🎵 Listen to Sound {sound_num} and choose the color you associate with it")
    audio_file = open(f"your-audio-{sound_num}.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")

    color = st.color_picker(f"🎨 Pick a color for Sound {sound_num}", "#ffffff", key=f"color_{sound_num}")
    colors.append((sound_num, color))

if st.button("✅ Submit your responses"):
    if name.strip() == "":
        st.warning("Please enter your name before submitting.")
    else:
        for sound_num, color in colors:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)

            row = [
                datetime.datetime.now().isoformat(),
                name,
                age,
                sound_num,
                color,
                r,
                g,
                b
            ]
            sheet.append_row(row)

        st.success("✅ Your responses have been saved. Thank you for participating!")
