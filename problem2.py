"""Generate the 10 image conditions used in a VLM robustness study.

For one input image, this script saves:
- 1 clean copy
- 3 single distortions
- 6 sequential two-step distortion combinations

Distortions:
1. JPEG compression
2. Gaussian blur
3. Gaussian noise

Usage:
    python problem2.py path/to/image output_folder
"""

from __future__ import annotations

import io
import sys
from itertools import permutations
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


def apply_jpeg_compression(img: Image.Image, quality: int = 15) -> Image.Image:
    """Apply JPEG compression and return the decoded image."""
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)
    return Image.open(buffer).convert("RGB")


def apply_gaussian_blur(img: Image.Image, radius: float = 2.0) -> Image.Image:
    """Apply Gaussian blur."""
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def apply_gaussian_noise(img: Image.Image, sigma: float = 25.0) -> Image.Image:
    """Apply Gaussian noise."""
    array = np.asarray(img).astype(np.float32)
    noise = np.random.normal(0, sigma, array.shape)
    noisy = np.clip(array + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy)


DISTORTIONS = {
    "jpeg": apply_jpeg_compression,
    "blur": apply_gaussian_blur,
    "noise": apply_gaussian_noise,
}


def save_image(img: Image.Image, output_dir: Path, name: str) -> None:
    output_path = output_dir / f"{name}.png"
    img.save(output_path)
    print(f"Saved {output_path}")


def generate_conditions(input_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    original = Image.open(input_path).convert("RGB")
    save_image(original, output_dir, "clean")

    for name, distortion in DISTORTIONS.items():
        save_image(distortion(original), output_dir, name)

    for first_name, second_name in permutations(DISTORTIONS, 2):
        first = DISTORTIONS[first_name](original)
        second = DISTORTIONS[second_name](first)
        save_image(second, output_dir, f"{first_name}_then_{second_name}")


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python problem2.py path/to/image output_folder")
        return 1

    input_path = Path(sys.argv[1]).expanduser().resolve()
    output_dir = Path(sys.argv[2]).expanduser().resolve()

    if not input_path.is_file():
        print(f"Input image not found: {input_path}")
        return 1

    generate_conditions(input_path, output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
