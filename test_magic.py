import magic

print("Testing magic...")
try:
    mime_type = magic.Magic(mime=True).from_file("test.pdf")
    print(f"MIME Type: {mime_type}")
    print("Magic Test Completed.")
except Exception as e:
    print(f"Error: {e}")
