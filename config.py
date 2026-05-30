"""项目配置：从 .env 文件读取参数。"""

from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
PRODUCTS_CSV = BASE_DIR / "products.csv"
INPUT_IMAGES_DIR = BASE_DIR / "input_images"
OUTPUT_DIR = BASE_DIR / "output"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_IMAGE_MODEL = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")
IMAGE_SIZE = os.getenv("IMAGE_SIZE", "1536x1024")
IMAGE_QUALITY = os.getenv("IMAGE_QUALITY", "medium")

CSV_FIELDS = [
    "sku",
    "product_name",
    "pcs",
    "length",
    "width",
    "height",
    "image_path",
]
