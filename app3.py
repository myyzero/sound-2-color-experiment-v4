import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

# ---- 配置区域 ----
SERVICE_ACCOUNT_FILE = 'streamlitcolorapp-0a350e473431.json'  # 你的服务账号JSON文件名
SCOPES = ['https://www.googleapis.com/auth/drive.file']
FOLDER_ID = 'S2C_data'  # 替换成目标文件夹ID

# ---- Google Drive 上传函数 ----
@st.cache_resource
def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def upload_csv_to_drive(df: pd.DataFrame, filename: str, drive_service):
    csv_data = df.to_csv(index=False)
    media = MediaInMemoryUpload(csv_data.encode('utf-8'), mimetype='text/csv')
    file_metadata = {
        'name': filename,
        'parents': [FOLDER_ID]
    }
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    return file.get('id')

# ---- Streamlit 页面 ----
st.title("上传CSV到Google Drive示例")

# 生成测试数据
df = pd.DataFrame({
    '名字': ['Alice', 'Bob', 'Charlie'],
    '年龄': [25, 30, 35]
})
st.write("预览数据：")
st.dataframe(df)

if st.button("上传CSV到Google Drive"):
    try:
        drive_service = get_drive_service()
        file_id = upload_csv_to_drive(df, "测试上传.csv", drive_service)
        st.success(f"上传成功！文件ID: {file_id}")
    except Exception as e:
        st.error(f"上传失败：{e}")
