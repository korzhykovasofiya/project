import json
from pypdf import PdfReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

formats=("txt", "csv", "json", "pdf")
font_path="C:/Windows/Fonts/times.ttf"

class FileError(Exception):
    pass

def get_format(path):
    file_format = path.split(".")[-1].lower()
    if file_format not in formats:
        raise FileError(f"Формат {file_format} не підтримується")
    return file_format

def read_pdf(path):
    reader=PdfReader(path)
    text = ""
    for page in reader.pages:
        text = text + page.extract_text() + "\n"
    return text

def read_file(path):
    file_format = get_format(path)
    try:
        if file_format == "pdf":
            text = read_pdf(path)
        else:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
    except FileNotFoundError:
        raise FileError(f"Файл не знайдено: {path}")
    if text.strip() == "":
        raise FileError(f"Файл {path} порожній")
    return text

def write_pdf(text, path):
    pdfmetrics.registerFont(TTFont("TimesNewRoman", font_path))
    pdf = canvas.Canvas(path)
    pdf.setFont("TimesNewRoman", 14)

    lines = []
    for line in text.split("\n"):
                while len(line) > 70:
                    lines.append(line[:70])
                    line = line[70:]
                lines.append(line)

    y = 800
    for line in lines:
        if y < 50:
            pdf.showPage()
            pdf.setFont("TimesNewRoman", 14)
            y = 800
        pdf.drawString(50, y, line)
        y = y - 20
    pdf.save()

def write_file(text, path):
    file_format = get_format(path)
    if file_format == "pdf":
        write_pdf(text, path)
    elif file_format == "json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = {"text": text}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)