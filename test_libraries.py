import PyPDF2, magic, pytesseract
from PIL import Image

print("Starting library tests...")

try:
    # Test PyPDF2
    print("Testing PyPDF2...")
    with open("test.pdf", "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages):
            print(f"PyPDF2 Page {i+1}: {page.extract_text()}")

    # Test magic
    print("Testing magic...")
    mime_type = magic.Magic(mime=True).from_file("test.pdf")
    print(f"Magic MIME Type: {mime_type}")

    # Test pytesseract
    print("Testing pytesseract...")
    img = Image.open("test_image.png")
    extracted_text = pytesseract.image_to_string(img)
    print(f"Pytesseract Output: {extracted_text}")

except Exception as e:
    print(f"Error: {e}")

print("Library tests completed.")
