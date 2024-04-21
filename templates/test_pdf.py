import pdfkit
from jinja2 import Environment, FileSystemLoader

if __name__ == '__main__':
    config = pdfkit.configuration(wkhtmltopdf=r'D:\wkhtmltopdf\bin\wkhtmltopdf.exe')

    with open('EnglishQuote.html', 'r', encoding='utf-8') as file:
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template("pdf_template.html")

        pdf_template = template.render()
        pdfkit.from_string(file.read(), 'out.pdf', configuration=config)