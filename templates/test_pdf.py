import pdfkit

config = pdfkit.configuration(wkhtmltopdf=r'D:\wkhtmltopdf\bin\wkhtmltopdf.exe')

with open('EnglishQuote.html', 'r', encoding='utf-8') as file:
    pdfkit.from_string(file.read(), 'out.pdf', configuration=config)
