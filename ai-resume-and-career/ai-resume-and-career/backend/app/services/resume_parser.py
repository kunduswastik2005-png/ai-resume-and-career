import fitz
from docx import Document
from io import BytesIO


def extract_text(file_content: bytes, file_type: str) -> str:

    if file_type == ".pdf":

        document = fitz.open(
            stream=file_content,
            filetype="pdf"
        )

        text = "\n".join(
            page.get_text() for page in document
        )

        document.close()

        return text.strip()

    elif file_type == ".docx":

        document = Document(BytesIO(file_content))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
        ]

        return "\n".join(paragraphs).strip()

    else:
        raise ValueError("Unsupported file format")