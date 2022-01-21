try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    im1 = Image.open(filename)
    # UPLOAD_FOLDER = 'static/uploads/'
    text = pytesseract.image_to_string(im1)  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    # im1=im1.save(os.path.join(UPLOAD_FOLDER,filename.filename))
    return text
