"""调用 OpenAI 图片生成 API，为每个 SKU 生成 6 张产品图。"""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Callable

from openai import OpenAI

from config import IMAGE_QUALITY, IMAGE_SIZE, OPENAI_API_KEY, OPENAI_IMAGE_MODEL
from prompt_templates import (
    build_prompt,
    detail_prompt,
    display_prompt,
    hero_prompt,
    mood_prompt,
    size_prompt,
)

ImagePrompt = Callable[[dict], str]

IMAGE_JOBS: list[tuple[str, ImagePrompt, str]] = [
    ("01_Hero.png", hero_prompt, "主图 / Hero image"),
    ("02_ProductSize.png", size_prompt, "尺寸图 / Product size image"),
    ("03_DetailDisplay.png", detail_prompt, "细节展示图 / Detail display image"),
    ("04_BuildExperience.png", build_prompt, "拼搭体验图 / Build experience image"),
    ("05_MoodShot.png", mood_prompt, "氛围图 / Mood shot"),
    ("06_DisplayLife.png", display_prompt, "生活展示图 / Display life image"),
]


class ProductImageGenerator:
    """简单封装：输入产品信息和参考图，输出 PNG 文件。"""

    def __init__(self) -> None:
        if not OPENAI_API_KEY:
            raise ValueError("没有找到 OPENAI_API_KEY，请先复制 .env.example 为 .env 并填写 Key。")
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_six_images(self, product: dict, reference_image: Path | None, output_dir: Path) -> None:
        """为单个产品生成 6 张图片。"""
        output_dir.mkdir(parents=True, exist_ok=True)

        for file_name, prompt_func, image_type in IMAGE_JOBS:
            output_path = output_dir / file_name
            prompt = prompt_func(product).strip() or self._fallback_prompt(product, image_type)

            print(f"  正在生成：{output_path.name}")
            image_bytes = self._create_image(prompt, reference_image)
            output_path.write_bytes(image_bytes)
            print(f"  已保存：{output_path}")

    def _create_image(self, prompt: str, reference_image: Path | None) -> bytes:
        """有参考图就走 images.edit；没有参考图就走 images.generate。"""
        if reference_image and reference_image.exists():
            with reference_image.open("rb") as image_file:
                response = self.client.images.edit(
                    model=OPENAI_IMAGE_MODEL,
                    image=image_file,
                    prompt=prompt,
                    size=IMAGE_SIZE,
                    quality=IMAGE_QUALITY,
                    n=1,
                )
        else:
            response = self.client.images.generate(
                model=OPENAI_IMAGE_MODEL,
                prompt=prompt,
                size=IMAGE_SIZE,
                quality=IMAGE_QUALITY,
                n=1,
            )

        b64_image = response.data[0].b64_json
        if not b64_image:
            raise RuntimeError("OpenAI 没有返回图片数据，请检查账号权限、模型和参数。")
        return base64.b64decode(b64_image)

    def _fallback_prompt(self, product: dict, image_type: str) -> str:
        """当 prompt_templates.py 暂时为空时使用的基础提示词。"""
        return (
            f"Create a professional e-commerce product image for a building block set.\n"
            f"Image type: {image_type}.\n"
            f"SKU: {product['sku']}.\n"
            f"Product name: {product['product_name']}.\n"
            f"Pieces: {product['pcs']} pcs.\n"
            f"Product size: {product['length']} x {product['width']} x {product['height']} cm.\n"
            "Use the reference image as the exact product appearance when provided. "
            "Keep the product accurate, clean, sharp, commercial, and suitable for an online store. "
            "Do not add wrong text, logos, watermarks, or extra accessories that are not in the product."
        )
