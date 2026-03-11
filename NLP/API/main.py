from nltk.tokenize import sent_tokenize
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet , ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.enums import TA_JUSTIFY
from config import dbi,fsi
from text import extract_pdf
from split import long

paths = "/path/to/file"

word = extract_pdf(paths)
token = sent_tokenize(" ".join(word)if isinstance(word,list)else word)

def main():
    text_eng = token
    texts = long(text_eng)

    def centered(texts,filename):
        doc = SimpleDocTemplate(filename , pagesize=A4)
        styles = getSampleStyleSheet()
        center = ParagraphStyle(
            "Justified",
            parent=styles["Normal"],
            fontSize=12,
            fontName="Times-Roman",
            alignment=TA_JUSTIFY
        )
        format = "<br />".join(texts.strip().split("\n"))
        content = Paragraph(format,center)
        doc.build([content])
    centered(texts,paths)
    # masukin ke db 
    with open(paths , "rb") as file:
        files_id = fsi.put(file,filenames="lann.pdf")
    # masukin ke db 
main()