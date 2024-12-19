import multiprocessing
import os

# CPU Settings
NUM_CORES = max(1, multiprocessing.cpu_count() - 1)

# Processing Settings
DEFAULT_DPI = 200
DEFAULT_BATCH_SIZE = 10
MIN_DPI = 100
MAX_DPI = 300
MIN_BATCH_SIZE = 5
MAX_BATCH_SIZE = 50

# OCR Settings
TESSERACT_CONFIG = r'--oem 3 --psm 6 -l hin+san'

# Output Settings
OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
TEMP_DIR_PREFIX = 'devanagari_ocr_'