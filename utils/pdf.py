import pytesseract
from concurrent.futures import ThreadPoolExecutor, as_completed
import pdf2image
import tempfile
import multiprocessing
import os

# Number of CPU cores to use (leave one core free for system)
NUM_CORES = max(1, multiprocessing.cpu_count() - 1)
TESSERACT_CONFIG = r'--oem 3 --psm 6 -l hin+san'
TEMP_DIR_PREFIX = 'devanagari_ocr_'

def process_page(page, page_num):
    """Process a single page and return its text with page number."""
    try:
        text = pytesseract.image_to_string(page, config=TESSERACT_CONFIG)
        return f"\n=== Page {page_num + 1} ===\n{text}"
    except Exception as e:
        return f"\n=== Page {page_num + 1} ===\nError processing page: {str(e)}"

def process_batch(batch_data):
    """Process a batch of images and return their combined text."""
    batch_images, start_idx = batch_data
    return "\n".join(process_page(img, start_idx + i) for i, img in enumerate(batch_images))

def convert_to_unicode_parallel(*, images, progress_bar, progress_text, status_text, preview_only=False, preview_pages=3):
    """
    Extract text from images using parallel processing.
    
    Args:
        images: List of PIL Image objects
        progress_bar: Streamlit progress bar object
        progress_text: Streamlit text object for progress
        status_text: Streamlit text object for status
        preview_only: Boolean indicating if this is a preview run
        preview_pages: Number of pages to process in preview mode
    Returns:
        String containing extracted text with page numbers
    """
    if preview_only:
        status_text.text("Generating preview...")
        total_pages = min(preview_pages, len(images))
        images = images[:preview_pages]
    else:
        status_text.text("Processing full document...")
        total_pages = len(images)
    
    processed_pages = 0
    all_text = []
    
    # Create batches of images
    batch_size = min(10, max(1, len(images) // NUM_CORES))
    batches = []
    for i in range(0, len(images), batch_size):
        batch_images = images[i:i + batch_size]
        batches.append((batch_images, i))
    
    with ThreadPoolExecutor(max_workers=NUM_CORES) as executor:
        future_to_batch = {executor.submit(process_batch, batch_data): i 
                          for i, batch_data in enumerate(batches)}
        
        for future in as_completed(future_to_batch):
            batch_idx = future_to_batch[future]
            try:
                text = future.result()
                all_text.append(text)
                
                processed_pages += len(batches[batch_idx][0])
                current_progress = min(processed_pages / total_pages, 1.0)
                progress_bar.progress(current_progress)

                if preview_only:
                    progress_text.text(f'Preview: {processed_pages}/{total_pages} pages')
                else:
                    progress_text.text(f'Processing: {processed_pages}/{total_pages} pages')
                
            except Exception as e:
                raise Exception(f"Error processing batch {batch_idx}: {str(e)}")
    
    if preview_only:
        return "\n".join(all_text) + f"\n\n... Preview limited to first {preview_pages} pages ..."
    return "\n".join(all_text)

def convert_pdf_to_images(pdf_file, dpi=200):
    """
    Convert PDF to images with memory optimization.
    
    Args:
        pdf_file: Streamlit uploaded file object
        dpi: DPI for image conversion (default: 200)
    Returns:
        List of PIL Image objects
    """
    with tempfile.TemporaryDirectory(prefix=TEMP_DIR_PREFIX) as temp_dir:
        images = pdf2image.convert_from_bytes(
            pdf_file.read(),
            dpi=dpi,
            thread_count=NUM_CORES,
            output_folder=temp_dir
        )
        return images