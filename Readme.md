# Devanagari PDF to Unicode Converter

A Streamlit application that converts PDF documents containing Devanagari text (both scanned and digital) into various Unicode formats (TXT, DOCX, PDF, HTML). The application supports multiple PDF files, multipage processing, and provides real-time conversion progress tracking.

## Features

- 📄 Support for multiple PDF files
- 📚 Multipage PDF processing
- 🔄 Real-time progress tracking
- 👀 Preview of extracted text
- 💾 Multiple export formats:
  - Text files (.txt)
  - Word documents (.docx)
  - PDF files (.pdf)
  - HTML files (.html)
- 🔡 Full Unicode support for Devanagari text
- 💻 Cross-platform compatibility (Windows, macOS, Linux)

## Prerequisites

### MacOS

1. Install Homebrew if not already installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install Tesseract with language support:
```bash
brew install tesseract
brew install tesseract-lang
```

3. Install poppler for PDF processing:
```bash
brew install poppler
```

4. Install required system dependencies for WeasyPrint:
```bash
brew install pango
brew install cairo
```

### Windows

1. Install Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. Install Tesseract:
   - Download installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - During installation:
     - Check boxes for additional languages (Hindi and Sanskrit)
     - Note the installation path (default: `C:\Program Files\Tesseract-OCR`)
   - Add Tesseract to your system PATH:
     - Open System Properties → Advanced → Environment Variables
     - Add the installation path to the Path variable

3. Install poppler:
   - Download from [poppler releases](https://github.com/oschwartz10612/poppler-windows/releases/)
   - Extract the downloaded file
   - Add the `bin` directory to your system PATH

4. Install GTK3 for WeasyPrint:
   - Download the GTK3 installer from [GTK3 Runtime](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
   - Run the installer
   - Ensure the installation directory is in your system PATH

### Linux (Ubuntu/Debian)

1. Install required system packages:
```bash
sudo apt-get update
sudo apt-get install -y python3-pip
sudo apt-get install -y tesseract-ocr
sudo apt-get install -y tesseract-ocr-hin
sudo apt-get install -y tesseract-ocr-san
sudo apt-get install -y poppler-utils
sudo apt-get install -y python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd devanagari-pdf-converter
```

2. Create and activate a virtual environment:

For MacOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

For Windows:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Upload PDF files:
   - Click "Browse files" or drag and drop PDF files
   - Multiple files can be selected
   - Both scanned and digital PDFs are supported

4. Processing:
   - The app will process each page of each PDF
   - Progress bar shows conversion status
   - Preview extracted text in real-time

5. Export:
   - Select desired output format (TXT, DOCX, PDF, HTML)
   - Click "Export" button
   - Files are saved in the `output` directory

## Environment Variables

For Windows, you might need to set these environment variables:

```
TESSDATA_PREFIX=C:\Program Files\Tesseract-OCR\tessdata
POPPLER_PATH=C:\path\to\poppler\bin
```

## Troubleshooting

### Tesseract Issues

1. **"Tesseract not found" error:**
   ```python
   # Add to the top of app.py:
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust path as needed
   ```

2. **Poor recognition quality:**
   - Ensure PDF scan quality is good
   - Check if correct language files are installed
   - Try adjusting image preprocessing (contact maintainers)

### PDF Processing Issues

1. **PDF import fails:**
   - Verify poppler installation
   - Check if poppler is in PATH
   - Try with a different PDF to rule out file corruption

2. **Memory errors with large PDFs:**
   - Try processing fewer pages at once
   - Ensure sufficient system memory is available
   - Close other memory-intensive applications

### Export Issues

1. **Unicode characters missing in output:**
   - Verify file is opened with UTF-8 encoding
   - Check if appropriate fonts are installed
   - Try a different text editor

2. **WeasyPrint PDF generation fails:**
   - Verify all WeasyPrint dependencies are installed
   - Check system font availability
   - Try updating WeasyPrint to the latest version

## Limitations

- Very large PDFs (>100MB) may require additional memory
- Recognition quality depends on input scan quality
- Processing time varies based on PDF complexity and system specifications

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
```bash
# Install development dependencies
pip install black flake8

# Format code
black .

# Check style
flake8
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Project Link: [https://github.com/yourusername/devanagari-pdf-converter](https://github.com/yourusername/devanagari-pdf-converter)

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Streamlit](https://streamlit.io/)
- [WeasyPrint](https://weasyprint.org/)
- [pdf2image](https://github.com/Belval/pdf2image)