import streamlit as st
import pandas as pd
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Sound-Color Association Experiment", layout="centered")
st.title("🎧 Sound and Color Association Experiment")

# Google Sheets 授权
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gcp_service_account"], scope
)
client = gspread.authorize(credentials)

# 打开你的表格（换成你自己的 Google Sheets 名称）
sheet = client.open("S2C_data").sheet1

sound_numbers = [1, 2, 3]
colors = []

for sound_num in sound_numbers:
    st.markdown(f"### Listen to Sound {sound_num} and select the color you associate with it 👇")
    audio_file = open(f"your-audio-{sound_num}.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")

    color = st.color_picker(f"🎨 Select color for Sound {sound_num}", "#ffffff", key=f"color_{sound_num}")
    colors.append((sound_num, color))

if st.button("✅ Submit your colors"):
    for sound_num, color in colors:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)

        row = [
            datetime.datetime.now().isoformat(),
            sound_num,
            color,
            r,
            g,
            b
        ]
        sheet.append_row(row)

    st.success("✅ Your colors have been saved to Google Sheets. Thank you for participating!")
