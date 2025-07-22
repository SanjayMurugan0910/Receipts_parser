import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import os
import tempfile
import re

# --- Streamlit Setup ---
st.set_page_config(page_title="🧾 Grocery Receipt Analyzer", layout="wide")
st.title("🛒 Grocery Receipt Analyzer Dashboard")

# --- MySQL Connection ---
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sanjay@2003",
    database="receipts_db"
)
cursor = conn.cursor(dictionary=True)

# --- Parsing Logic ---
def parse_receipt_data(text):
    vendor = text.split('\n')[0].strip()[:100] if text else "Unknown"

    amount_match = re.search(r'\₹?\$?\s?(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)', text)
    amount = amount_match.group(1).replace(',', '') if amount_match else "0.00"

    date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text)
    if date_match:
        for fmt in ("%d/%m/%Y", "%d-%m-%Y"):
            try:
                date = datetime.strptime(date_match.group(1), fmt).date()
                break
            except:
                date = None
    else:
        date = None

    return vendor, float(amount), date

# --- Upload and Extract ---
st.sidebar.header("📤 Upload Receipt")
uploaded_file = st.sidebar.file_uploader("Upload JPG, PNG or PDF", type=["jpg", "png", "pdf", "jpeg"])

if uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        extracted_text = ""

        if uploaded_file.type == "application/pdf":
            with fitz.open(file_path) as doc:
                for page in doc:
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    extracted_text += pytesseract.image_to_string(img)
        else:
            with Image.open(file_path) as img:
                extracted_text = pytesseract.image_to_string(img)

        # --- Display OCR Output ---
        st.subheader("📝 Extracted Text")
        st.text_area("OCR Output", extracted_text, height=250)

        # --- Parse Text ---
        vendor, amount, date = parse_receipt_data(extracted_text)

        st.subheader("📊 Extracted Data")
        st.write(f"**Vendor:** {vendor}")
        st.write(f"**Date:** {date if date else 'Not Found'}")
        st.write(f"**Amount:** ₹{amount:.2f}")

        # --- Save to DB ---
        if st.button("✅ Save to Database"):
            if vendor and amount and date:
                cursor.execute(
                    "INSERT INTO receipts (vendor, amount, transaction_date, created_at) VALUES (%s, %s, %s, NOW())",
                    (vendor, amount, date)
                )
                conn.commit()
                st.success("✅ Receipt saved successfully!")
                st.rerun()

            else:
                st.error("⚠️ Missing vendor, amount, or date. Please check the extracted data.")

# --- Dashboard Section ---
cursor.execute("SELECT * FROM receipts ORDER BY created_at DESC")
records = cursor.fetchall()
df = pd.DataFrame(records)

if df.empty:
    st.info("No receipts uploaded yet.")
else:
    st.subheader("📄 Uploaded Receipts")
    st.dataframe(df)

    st.subheader("💰 Total Spend by Vendor")
    vendor_chart = df.groupby("vendor")["amount"].sum()
    st.bar_chart(vendor_chart)

    st.subheader("📈 Monthly Spending Trend")
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    trend = df.groupby(df['transaction_date'].dt.to_period('M'))['amount'].sum()
    st.line_chart(trend)

    st.subheader("🔍 Search Receipts")
    vendor_filter = st.text_input("Vendor name contains:")
    if vendor_filter:
        filtered = df[df['vendor'].str.contains(vendor_filter, case=False)]
        st.dataframe(filtered)
