import PyPDF2

print("Testing PyPDF2...")
with open("test.pdf", "rb") as f:
    reader = PyPDF2.PdfReader(f)
    for i, page in enumerate(reader.pages):
        print(f"Page {i + 1} Text: {page.extract_text()}")
print("PyPDF2 Test Completed.")
