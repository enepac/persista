from fpdf import FPDF
from PIL import Image

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Hello, PDF!", ln=True, align="C")
pdf.output("test.pdf")
print("PDF created successfully as 'test.pdf'")

img = Image.new('RGB', (200, 100), color='white')
img.save("test_image.png")
print("Image created successfully as 'test_image.png'")