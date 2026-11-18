
import fitz
from pathlib import Path


def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file using PyMuPDF.

    Supports:
    1. Local PDF file paths
    2. Streamlit UploadedFile objects

    Args:
        pdf_file: PDF file path or uploaded PDF object.

    Returns:
        Dictionary containing:
        - filename
        - total_pages
        - pages
        - full_text
    """

    document = None

    try:
        # ----------------------------------
        # STEP 1: Open the PDF file
        # ----------------------------------

        if hasattr(pdf_file, "read"):

            # Handle Streamlit uploaded PDF
            pdf_bytes = pdf_file.getvalue()

            document = fitz.open(
                stream=pdf_bytes,
                filetype="pdf"
            )

            filename = pdf_file.name

        else:

            # Handle normal local PDF file
            document = fitz.open(pdf_file)

            filename = Path(pdf_file).name

        # ----------------------------------
        # STEP 2: Extract text page by page
        # ----------------------------------

        extracted_pages = []

        for page_number, page in enumerate(
            document,
            start=1
        ):

            page_text = page.get_text("text")

            extracted_pages.append({
                "page_number": page_number,
                "text": page_text.strip()
            })

        # ----------------------------------
        # STEP 3: Combine extracted text
        # ----------------------------------

        full_text = "\n\n".join(
            f"[PAGE {page['page_number']}]\n{page['text']}"
            for page in extracted_pages
        )

        # ----------------------------------
        # STEP 4: Prepare final result
        # ----------------------------------

        result = {
            "filename": filename,
            "total_pages": len(document),
            "pages": extracted_pages,
            "full_text": full_text,
            "is_empty": not full_text.strip()
        }

        return result

    except Exception as error:

        raise ValueError(
            f"Error extracting PDF '{getattr(pdf_file, 'name', str(pdf_file))}': {error}"
        ) from error

    finally:

        if document is not None:
            document.close()


# --------------------------------------
# STEP 5: Test using a local PDF file
# --------------------------------------

if __name__ == "__main__":

    pdf_path = "data/sample_papers/sample.pdf"

    if Path(pdf_path).exists():

        try:

            result = extract_text_from_pdf(pdf_path)

            print("\nPDF EXTRACTION SUCCESSFUL")
            print("-------------------------")

            print("Filename:", result["filename"])
            print("Total Pages:", result["total_pages"])

            if result["is_empty"]:
                print("Warning: No extractable text found.")
            else:
                print("\nEXTRACTED TEXT:")
                print("-------------------------")
                print(result["full_text"][:3000])

        except ValueError as error:

            print("Extraction failed:", error)

    else:

        print("Please provide a PDF file to test extraction.")
