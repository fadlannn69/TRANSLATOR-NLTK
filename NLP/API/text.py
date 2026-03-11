import fitz
from pdf2image import convert_from_path
import pytesseract
from multiprocessing import Pool , cpu_count




def extract_page(page):
    text = page.get_text()
    return text.strip() if text.strip() else None

def ocr_image(image):
    return pytesseract.image_to_string(image,lang="eng+ind")


def extract_pdf(paths):
    doc = fitz.open(paths)

    def extract_text(doc):
        for page in doc:
            text = extract_page(page)
            yield text
    result = list(filter(None,extract_text(doc)))
    if len(result) == len(doc):
        return "\n".join(result)

    ocr_pages = [i  for i ,text in enumerate(result) if text is None]

    if ocr_pages:
        images = convert_from_path(
            paths,dpi=150,
            first_page=ocr_pages[0],
            last_page=ocr_pages[-1],
            thread_count=cpu_count()
        )


        with Pool(min(cpu_count(),len(images))) as pool:
            ocr_texts = pool.map(ocr_image,images)

        for idx, text in zip(ocr_pages,ocr_texts):
            result.insert(idx -1 , text.strip())
        
    return "\n".join(result)
