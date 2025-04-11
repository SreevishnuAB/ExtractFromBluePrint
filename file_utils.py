import os
from typing import List
from pypdf import PdfReader, PdfWriter

def split_pdf_into_pages(input_pdf_path: str, output_folder: str)-> None:
    """
    Splits a PDF file into individual pages and saves them as separate PDF files.

    Args:
        input_pdf_path (str): Path to the input PDF file.
        output_folder (str): Path to the folder where the split pages will be saved.
    """
    reader = PdfReader(input_pdf_path)
    for page_number in range(len(reader.pages)):
        writer = PdfWriter()
        writer.add_page(reader.pages[page_number])
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        output_pdf_path = f"{output_folder}/page_{page_number + 1}.pdf"
        with open(output_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)

def get_files_from_directory(directory: str) -> List[str]:
    """
    Returns a list of files in the specified directory.

    Args:
        directory (str): Path to the directory.

    Returns:
        list: List of file paths in the directory.
    """
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

if __name__ == "__main__":
    input_pdf_path = "M&P mark-up against shop systems piping.pdf"  # Replace with your input PDF path
    output_folder = "M&P mark-up against shop systems piping"  # Replace with your output folder path
    # split_pdf_into_pages(input_pdf_path, output_folder)
    print(get_files_from_directory(output_folder))