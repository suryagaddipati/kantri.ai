import contextlib
import io
import sys
import pdfplumber
from pathlib import Path
from typing import Optional


def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with contextlib.redirect_stderr(io.StringIO()):
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    return text


def extract_tables_from_pdf(pdf_path: str) -> list:
    tables = []
    with contextlib.redirect_stderr(io.StringIO()):
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_tables = page.extract_tables()
                if page_tables:
                    for table in page_tables:
                        tables.append({
                            'page': page_num + 1,
                            'data': table
                        })
    return tables


def main(pdf_path: Optional[str] = None):
    if not pdf_path:
        print("Usage: python main.py <path_to_pdf>")
        return

    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"Error: File '{pdf_path}' not found")
        return

    print(f"Extracting data from: {pdf_path}\n")

    text = extract_text_from_pdf(pdf_path)
    print("=== Extracted Text ===")
    print(text)

    tables = extract_tables_from_pdf(pdf_path)
    if tables:
        print(f"\n=== Extracted Tables ({len(tables)} found) ===")
        for i, table_info in enumerate(tables):
            print(f"\nTable {i+1} (Page {table_info['page']}):")
            for row in table_info['data']:
                print(row)
    else:
        print("\nNo tables found in PDF")


if __name__ == "__main__":
    import sys
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else None
    main(pdf_path)
