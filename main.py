"""入口文件：读取 products.csv，按 SKU 批量生成图片。"""

from __future__ import annotations

import csv
from pathlib import Path

from config import CSV_FIELDS, INPUT_IMAGES_DIR, OUTPUT_DIR, PRODUCTS_CSV
from image_generator import ProductImageGenerator


def read_products(csv_path: Path) -> list[dict]:
    """读取 products.csv，并检查字段是否正确。"""
    if not csv_path.exists():
        raise FileNotFoundError(f"找不到 {csv_path}，请先创建 products.csv。")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != CSV_FIELDS:
            raise ValueError(
                "products.csv 字段不正确。\n"
                f"需要字段：{','.join(CSV_FIELDS)}\n"
                f"当前字段：{','.join(reader.fieldnames or [])}"
            )
        return [row for row in reader if row.get("sku", "").strip()]


def find_reference_image(product: dict) -> Path | None:
    """优先使用 image_path；如果为空，尝试按 SKU 在 input_images 中找图。"""
    image_path = product.get("image_path", "").strip()
    if image_path:
        path = Path(image_path)
        if not path.is_absolute():
            path = INPUT_IMAGES_DIR / path
        if path.exists():
            return path
        print(f"  警告：参考图不存在：{path}，将不带参考图生成。")
        return None

    sku = product["sku"].strip()
    for suffix in (".png", ".jpg", ".jpeg", ".webp"):
        path = INPUT_IMAGES_DIR / f"{sku}{suffix}"
        if path.exists():
            return path
    print(f"  警告：没有找到 SKU {sku} 的参考图，将不带参考图生成。")
    return None


def main() -> None:
    products = read_products(PRODUCTS_CSV)
    if not products:
        print("products.csv 里没有产品，请先添加产品信息。")
        return

    generator = ProductImageGenerator()

    for product in products:
        sku = product["sku"].strip()
        product["sku"] = sku
        print(f"\n开始处理 SKU：{sku}")

        reference_image = find_reference_image(product)
        sku_output_dir = OUTPUT_DIR / sku
        generator.generate_six_images(product, reference_image, sku_output_dir)

    print("\n全部完成。生成结果在 output 文件夹。")


if __name__ == "__main__":
    main()
