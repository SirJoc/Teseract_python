from PIL import Image
import pytesseract

# Specify the path to the tesseract executable (if needed)
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Open an image and perform OCR
image_path = 'sample_image.png'
text = pytesseract.image_to_string(Image.open(image_path))
print(text)

