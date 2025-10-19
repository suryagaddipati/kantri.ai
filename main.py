import contextlib
import io
import json
import sys
import pdfplumber
from pathlib import Path
from typing import Any, Optional


def sanitize_for_json(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(item) for item in obj]
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    else:
        return str(obj)


def extract_raw_data(pdf_path: str, page_number: Optional[int] = None) -> dict:
    data: dict = {"pages": []}
    with contextlib.redirect_stderr(io.StringIO()):
        with pdfplumber.open(pdf_path) as pdf:
            pages = [pdf.pages[page_number - 1]] if page_number else pdf.pages
            for page in pages:
                page_data = {
                    "page_number": page.page_number,
                    "width": page.width,
                    "height": page.height,
                    "chars": sanitize_for_json(page.chars),
                    "lines": sanitize_for_json(page.lines),
                    "rects": sanitize_for_json(page.rects),
                    "curves": sanitize_for_json(page.curves),
                    "images": sanitize_for_json(page.images),
                    "annots": sanitize_for_json(page.annots),
                    "hyperlinks": sanitize_for_json(page.hyperlinks),
                }
                data["pages"].append(page_data)
    return data


def main(pdf_path: Optional[str] = None, page_number: Optional[int] = None):
    if not pdf_path:
        print("Usage: python main.py <path_to_pdf> [page_number]")
        return

    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"Error: File '{pdf_path}' not found")
        return

    data = extract_raw_data(pdf_path, page_number)
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    import sys
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else None
    page_number = int(sys.argv[2]) if len(sys.argv) > 2 else None
    main(pdf_path, page_number)
