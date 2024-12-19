import subprocess
import os
import streamlit as st
from config.settings import TESSERACT_CONFIG

def verify_tesseract_installation():
    """Verify Tesseract installation and language files."""
    try:
        # Check if tesseract is installed
        subprocess.run(['tesseract', '--version'], capture_output=True, check=True)
        
        # Get tessdata path
        tessdata_path = os.getenv('TESSDATA_PREFIX')
        if not tessdata_path:
            # Try to get it from brew on macOS
            try:
                tessdata_path = subprocess.run(
                    ['brew', '--prefix'], 
                    capture_output=True, 
                    text=True, 
                    check=True
                ).stdout.strip() + '/share/tessdata'
                os.environ['TESSDATA_PREFIX'] = tessdata_path
            except:
                st.error("Could not determine TESSDATA_PREFIX. Please set it manually.")
                return False
        
        # Check for required language files
        required_langs = ['hin', 'san']
        missing_langs = []
        for lang in required_langs:
            if not os.path.exists(f"{tessdata_path}/{lang}.traineddata"):
                missing_langs.append(lang)
        
        if missing_langs:
            st.error(f"Missing language files: {', '.join(missing_langs)}")
            st.info("""
            To install missing languages on macOS:
            1. Run: brew install tesseract-lang
            2. Add to ~/.zshrc: export TESSDATA_PREFIX="$(brew --prefix)/share/tessdata/"
            3. Restart your terminal or run: source ~/.zshrc
            """)
            return False
        
        return True
    except subprocess.CalledProcessError:
        st.error("Tesseract is not installed properly.")
        return False