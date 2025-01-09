from PIL import Image
import pytesseract

# Set the Tesseract executable path if required
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

print("Testing pytesseract...")
img = Image.open("test_image.png").convert("L").resize((800, 800))
extracted_text = pytesseract.image_to_string(img)
print(f"Extracted Text: {extracted_text}")
print("Pytesseract Test Completed.")
