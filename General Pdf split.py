
import os
from pypdf import PdfReader, PdfWriter

def split_any_pdf(input_pdf_path, output_folder, split_mode, parts=None):
    # Open the input PDF file
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)
    
    if split_mode == 'equal':
        # Split PDF into equal parts
        num_parts = int(parts)
        pages_per_part = total_pages // num_parts
        for i in range(num_parts):
            writer = PdfWriter()
            start_page = i * pages_per_part
            end_page = (i + 1) * pages_per_part if i < num_parts - 1 else total_pages
            
            for page in range(start_page, end_page):
                writer.add_page(reader.pages[page])
            
            output_pdf_path = os.path.join(output_folder, f"Part_{i+1}.pdf")
            with open(output_pdf_path, 'wb') as output_pdf:
                writer.write(output_pdf)
            
            print(f"Part {i+1} has been written to {output_pdf_path}")
    
    elif split_mode == 'manual':
        # Split PDF based on manually provided page ranges
        for i, (start_page, end_page) in enumerate(parts, start=1):
            writer = PdfWriter()
            
            for page in range(start_page - 1, end_page):
                writer.add_page(reader.pages[page])
            
            output_pdf_path = os.path.join(output_folder, f"Part_{i}.pdf")
            with open(output_pdf_path, 'wb') as output_pdf:
                writer.write(output_pdf)
            
            print(f"Part {i} (Pages {start_page}-{end_page}) has been written to {output_pdf_path}")
    
    else:
        print("Invalid split mode. Please choose 'equal' or 'manual'.")

def main():
    input_pdf_path = input("Enter the path to your input PDF file: ")
    output_folder = input("Enter the path to your output folder: ")
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    split_mode = input("Do you want to split the PDF into equal parts or specify page ranges? (Enter 'equal' or 'manual'): ").strip().lower()
    
    if split_mode == 'equal':
        num_parts = input("Enter the number of equal parts to split the PDF into: ")
        split_any_pdf(input_pdf_path, output_folder, split_mode, parts=num_parts)
    
    elif split_mode == 'manual':
        parts = []
        print("Enter the page ranges for each part (e.g., 1-12). Type 'done' when finished.")
        while True:
            page_range = input(f"Enter page range for part {len(parts) + 1}: ").strip()
            if page_range.lower() == 'done':
                break
            try:
                start_page, end_page = map(int, page_range.split('-'))
                parts.append((start_page, end_page))
            except ValueError:
                print("Invalid page range. Please enter the range as 'start-end' (e.g., 1-12).")
        
        split_any_pdf(input_pdf_path, output_folder, split_mode, parts=parts)

if __name__ == "__main__":
    main()
