# Receipts_parser
# 🧾 Receipt & Invoice Data Extractor using OCR

A mini full-stack application that allows users to upload grocery receipts or invoices (images or PDFs), extract structured data using OCR and Regex, store it into a MySQL database, and explore or analyze it using a user-friendly interface.

---

## 📌 Features

- ✅ Upload receipts/invoices in `.jpg`, `.png`, or `.pdf` format
- ✅ Extract:
  - Vendor Name
  - Purchase Date
  - Total Amount
  - Tax / GST
  - Individual Item Descriptions
- ✅ Store extracted data in **MySQL**
- ✅ View and filter receipts by vendor, date, or total amount
- ✅ Visual analytics of spending using **Plotly**
- ✅ Built with **Python + Streamlit** (frontend) and **MySQL** (backend)

---

## 🏗️ Architecture & Design

```plaintext
[User Uploads File] 
       ↓
[OCR using Tesseract]
       ↓
[Regex-based Data Extraction]
       ↓
[MySQL Database]
       ↓
[Streamlit UI: List View, Filtering, Analytics]
```

**Key Components:**

| Component        | Tool/Library                  |
|------------------|-------------------------------|
| OCR Engine        | `pytesseract` + `Tesseract-OCR` |
| UI & Dashboard    | `Streamlit`, `Plotly`         |
| Image Processing  | `Pillow`, `OpenCV`            |
| PDF Extraction    | `PyMuPDF` (fitz)              |
| DB Connectivity   | `mysql-connector-python`      |

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/receipt-ocr-analyzer.git
cd receipt-ocr-analyzer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract-OCR

- Download from: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
- Windows Path (example): `C:\Program Files\Tesseract-OCR\tesseract.exe`

In `app.py`, update:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### 4. Configure MySQL

Create a database and tables:

```sql
CREATE DATABASE receipt_db;

USE receipt_db;

CREATE TABLE receipts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor VARCHAR(255),
    purchase_date DATE,
    total_amount FLOAT,
    tax_amount FLOAT
);

CREATE TABLE receipt_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    receipt_id INT,
    item_line TEXT,
    FOREIGN KEY (receipt_id) REFERENCES receipts(id) ON DELETE CASCADE
);
```

Update MySQL credentials in the code:

```python
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="receipt_db"
)
```

### 5. Run the App

```bash
streamlit run app.py
```

---

## 📊 Sample Output

| Vendor     | Date       | Total  | Tax   |
|------------|------------|--------|-------|
| Big Bazaar | 2025-07-15 | ₹245.0 | ₹12.0 |

Item Lines:
- 1x Milk 500ml ₹40
- 1x Sugar 1kg ₹60
- ...

---

## 📌 Limitations

- 🔍 OCR accuracy may drop on low-quality images or skewed text.
- 🧾 Vendor and item parsing depends on standard receipt formats.
- 🧠 Regex parsing can't handle completely unstructured data.
- 🗂 PDF parsing is limited to text-based (not scanned) PDFs unless OCR is applied.

---

## 💡 Future Enhancements

- ✅ Support for more complex item extraction (name, qty, price split)
- ✅ Use AI/LLM (like Gemini/Ollama) for better semantic extraction
- ✅ Add authentication/user login
- ✅ Export data to Excel/CSV

---

## 🙋‍♂️ Assumptions

- Vendor name is always the topmost line.
- Total amount and tax are labeled or follow common monetary patterns.
- Items are line-separated and contain some price or quantity hints.
- Tesseract is installed and available on system PATH or configured properly.

---

## 🧠 Example Technologies

| Stack Layer     | Tech Used                |
|------------------|--------------------------|
| OCR              | Tesseract                |
| Backend (ETL)    | Python                   |
| UI & Logic       | Streamlit                |
| DB               | MySQL                    |
| Visualization    | Plotly                   |
| Parsing          | Regex, NLP optional      |

---

## 🤝 Contributors

- 👨‍💻 [Sanjay Murugan](https://github.com/SanjayMurugan0910)
- 🧪 Tester: You!
