# ecommerce_system
"""
Update DBMS236_Assignment_Report.docx:
- Replace "FREEPDB1" with "XEPDB1"
- Replace "3rd September 2026" with "4th September 2026"
Saves result as DBMS236_Assignment_Report_Updated.docx
"""

from docx import Document

INPUT_FILE = "DBMS236_Assignment_Report.docx"
OUTPUT_FILE = "DBMS236_Assignment_Report_Updated.docx"

REPLACEMENTS = {
    "FREEPDB1": "XEPDB1",
    "3rd September 2026": "4th September 2026",
}


def replace_in_paragraph(paragraph):
    """Replace text within a paragraph, run by run."""
    for run in paragraph.runs:
        for old, new in REPLACEMENTS.items():
            if old in run.text:
                run.text = run.text.replace(old, new)


def replace_in_document(doc):
    # Paragraphs in the main body
    for paragraph in doc.paragraphs:
        replace_in_paragraph(paragraph)

    # Paragraphs inside tables (including nested tables)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    replace_in_paragraph(paragraph)


def main():
    doc = Document(INPUT_FILE)
    replace_in_document(doc)
    doc.save(OUTPUT_FILE)
    print(f"Saved updated file as {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
