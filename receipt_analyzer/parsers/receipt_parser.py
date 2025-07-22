import pytesseract
from PIL import Image
import tempfile
import re
from datetime import datetime
import langdetect

def extract_data_from_file(file_path):
    # Open the image from the path (works for PNG, JPG, etc.)
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
    except Exception as e:
        print(f"Error reading image: {e}")
        return None

    # Extract vendor
    try:
        vendor = re.findall(r'(?:Store|Vendor|Shop)[:\s]*([A-Za-z0-9 &]+)', text, re.IGNORECASE)[0]
    except IndexError:
        vendor = 'Unknown'

    # Extract total amount
    try:
        amount = float(re.findall(r'Total(?: Amount)?[:\s\$₹]*([\d]+\.\d{2})', text, re.IGNORECASE)[0])
    except IndexError:
        amount = 0.0

    # Extract transaction date
    try:
        date_str = re.findall(r'(\d{2}[/-]\d{2}[/-]\d{4})', text)[0]
        transaction_date = datetime.strptime(date_str, '%d/%m/%Y').date()
    except:
        transaction_date = datetime.today().date()

    # Language detection
    language = langdetect.detect(text)

    return {
        'vendor': vendor.strip(),
        'transaction_date': transaction_date,
        'amount': amount,
        'currency': 'INR',
        'category': 'Groceries',
        'language': language,
        'raw_text': text
    }
