import streamlit as st
import time
from pathlib import Path
import os
from utils.tesseract import verify_tesseract_installation
from utils.pdf import convert_pdf_to_images, convert_to_unicode_parallel
from utils.exporters import save_as_txt, save_as_docx, save_as_pdf, save_as_html

# Configuration
OUTPUT_DIR = "output"
DEFAULT_DPI = 200
DEFAULT_BATCH_SIZE = 10
MIN_DPI = 100
MAX_DPI = 300
MIN_BATCH_SIZE = 5
MAX_BATCH_SIZE = 50

def get_unique_filename(base_dir, base_name, extension):
    """Generate a unique filename by adding a number if file exists."""
    counter = 1
    file_path = os.path.join(base_dir, f"{base_name}.{extension}")
    while os.path.exists(file_path):
        file_path = os.path.join(base_dir, f"{base_name}_{counter}.{extension}")
        counter += 1
    return file_path

def get_base_filename(uploaded_files):
    """Get base filename from uploaded files."""
    if len(uploaded_files) == 1:
        # If single file, use its name without extension
        return Path(uploaded_files[0].name).stem
    else:
        # If multiple files, combine their names
        filenames = [Path(f.name).stem for f in uploaded_files]
        return f"combined_{'_'.join(filenames)}"

def main():
    st.set_page_config(
        page_title="Devanagari PDF to Unicode Converter",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("देवनागरी PDF to Unicode Converter")
    st.write("Upload PDF files containing Devanagari text (scanned or digital)")

    # Verify Tesseract installation
    if not verify_tesseract_installation():
        return

    # Initialize session state
    if 'full_text' not in st.session_state:
        st.session_state.full_text = []
    if 'converted' not in st.session_state:
        st.session_state.converted = False
    if 'export_format' not in st.session_state:
        st.session_state.export_format = "txt"
    if 'last_exported_file' not in st.session_state:
        st.session_state.last_exported_file = None

    # File uploader
    uploaded_files = st.file_uploader(
        "Choose PDF file(s)",
        type="pdf",
        accept_multiple_files=True,
        help="You can select multiple PDF files"
    )

    if uploaded_files:
        # Add processing options
        with st.expander("Processing Options"):
            dpi = st.slider(
                "DPI (lower = faster, higher = better quality)", 
                min_value=MIN_DPI,
                max_value=MAX_DPI, 
                value=DEFAULT_DPI,
                step=50,
                help="Lower DPI is faster but may reduce quality"
            )
            batch_size = st.slider(
                "Batch Size", 
                min_value=MIN_BATCH_SIZE,
                max_value=MAX_BATCH_SIZE, 
                value=DEFAULT_BATCH_SIZE,
                step=5,
                help="Number of pages to process at once"
            )

        # Convert button
        if st.button("Convert", type="primary"):
            st.session_state.full_text = []  # Clear previous results
            st.session_state.converted = True
            
            # Process each uploaded file
            for uploaded_file in uploaded_files:
                st.write(f"Processing: {uploaded_file.name}")
                
                # Create progress indicators
                preview_progress = st.progress(0)
                preview_status = st.empty()
                preview_text_status = st.empty()
                
                main_progress = st.progress(0)
                main_status = st.empty()
                main_text_status = st.empty()
                
                time_text = st.empty()
                
                try:
                    start_time = time.time()
                    
                    # Convert PDF to images
                    preview_text_status.text("Converting PDF to images...")
                    images = convert_pdf_to_images(uploaded_file, dpi)
                    total_pages = len(images)
                    preview_text_status.text(f"Total pages detected: {total_pages}")
                    
                    # Generate preview (first 3 pages)
                    preview_text = convert_to_unicode_parallel(
                        images=images,
                        progress_bar=preview_progress,
                        progress_text=preview_status,
                        status_text=preview_text_status,
                        preview_only=True,
                        preview_pages=3
                    )
                    
                    # Process full document
                    full_text = convert_to_unicode_parallel(
                        images=images,
                        progress_bar=main_progress,
                        progress_text=main_status,
                        status_text=main_text_status,
                        preview_only=False
                    )
                    
                    st.session_state.full_text.append(full_text)
                    
                    # Show processing time
                    elapsed_time = time.time() - start_time
                    time_text.text(f"Processing time: {elapsed_time:.2f} seconds")
                    
                    # Show preview
                    st.subheader(f"Text Preview for {uploaded_file.name} (First 3 Pages)")
                    st.text_area("", preview_text, height=200)
                    
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                    st.exception(e)  # This will show the full traceback
                    continue

        # Show export options only after conversion
        if st.session_state.converted and st.session_state.full_text:
            st.subheader("Export Options")
            
            # Set up columns for export options
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Export format selection
                st.session_state.export_format = st.selectbox(
                    "Choose export format",
                    ["txt", "docx", "pdf", "html"],
                    key="export_format_selector"
                )
                
                # Get default filename from uploaded files
                default_filename = get_base_filename(uploaded_files)
                
                # Custom filename input with default from original file
                custom_filename = st.text_input(
                    "Enter filename (without extension)",
                    value=default_filename,
                    key="custom_filename",
                    help="Default name is based on the uploaded file(s)"
                )

            with col2:
                # Export button
                if st.button("Export", key="export_button"):
                    try:
                        # Create output directory if it doesn't exist
                        output_dir = Path(OUTPUT_DIR)
                        output_dir.mkdir(exist_ok=True)
                        
                        # Generate unique filename
                        file_path = get_unique_filename(
                            output_dir,
                            custom_filename,
                            st.session_state.export_format
                        )
                        
                        combined_text = "\n".join(st.session_state.full_text)
                        
                        if st.session_state.export_format == "txt":
                            save_as_txt(combined_text, file_path)
                        elif st.session_state.export_format == "docx":
                            save_as_docx(combined_text, file_path)
                        elif st.session_state.export_format == "pdf":
                            save_as_pdf(combined_text, file_path)
                        elif st.session_state.export_format == "html":
                            save_as_html(combined_text, file_path)
                        
                        st.session_state.last_exported_file = file_path
                        st.success(f"Successfully exported to: {file_path}")
                        
                        # Download button for the exported file
                        with open(file_path, 'rb') as f:
                            st.download_button(
                                label=f"Download {st.session_state.export_format.upper()} file",
                                data=f,
                                file_name=os.path.basename(file_path),
                                mime=f"application/{st.session_state.export_format}"
                            )

                            # delete the file after download
                            os.remove(file_path)
                            
                    except Exception as e:
                        st.error(f"Error during export: {str(e)}")

if __name__ == "__main__":
    main()