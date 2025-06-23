# app.py
import streamlit as st
import numpy as np
import pandas as pd
import requests
from io import BytesIO

st.set_page_config(page_title="Transaction Scoring", layout="centered")
st.title("📊 Transaction Scoring App")

uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])

if uploaded_file:
    st.subheader("Preview of Uploaded Data")
    df = pd.read_excel(uploaded_file)
    st.dataframe(df.head())

    if st.button("Submit for Scoring"):
        with st.spinner("Sending file ..."):
            uploaded_file.seek(0)
            response = requests.post(
                "https://b322-182-176-168-81.ngrok-free.app/score",
                files={"file": (uploaded_file.name, uploaded_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            )

            if response.status_code == 200:
                result = pd.DataFrame(response.json())
                

                st.success("✅ Scoring complete!")
                st.subheader("🔍 Scored Data")
                st.dataframe(result)

                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    result.to_excel(writer, index=False, sheet_name='ScoredData')

                st.download_button(
                    label="📥 Download Scored Excel",
                    data=output.getvalue(),
                    file_name="scored_output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")
