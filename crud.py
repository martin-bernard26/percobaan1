import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Setup koneksi Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
service_account_info = st.secrets["google_credentials"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(credentials)

# Akses Google Sheet
sheet = client.open("datanilai").sheet1  # pilih sheet pertama

# READ - tampilkan data
data = sheet.get_all_records()
df = pd.DataFrame(data)
st.dataframe(df)

# CREATE
with st.form("create"):
    nama = st.text_input("Nama")
    nilai = st.number_input("Nilai", 0, 100)
    submitted = st.form_submit_button("Tambah")
    if submitted:
        sheet.append_row([nama, nilai])
        st.success("Data berhasil ditambahkan!")

# UPDATE (contoh update baris pertama)
if st.button("Update baris pertama jadi Nama=Baru, Nilai=99"):
    sheet.update("A2", "Baru")
    sheet.update("B2", 99)
    st.success("Data berhasil diupdate.")

# DELETE (hapus baris ke-2)
if st.button("Hapus baris ke-2"):
    sheet.delete_rows(2)
    st.success("Baris ke-2 dihapus.")
