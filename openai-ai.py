import base64
import csv
import os
import re
from pathlib import Path

from openai import OpenAI
from PIL import Image


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "gpt-image-1-mini"

PROMPT_FILE = Path("prompt.txt")
OUTPUT_DIR = Path("generated")

MAX_IMAGES_PER_RUN = 5

IMAGE_SIZE = "1536x1024"
IMAGE_QUALITY = "low"

# This resizes the image; it does not generate additional detail.
UPSCALE_FACTOR = 4


# ============================================================
# PROMPTS AND METADATA
# ============================================================

def load_prompts():
    if not PROMPT_FILE.is_file():
        raise SystemExit(f"❌ Prompt file not found: {PROMPT_FILE}")

    with PROMPT_FILE.open("r", encoding="utf-8") as file:
        prompts = [
            line.strip()
            for line in file
            if line.strip()
        ]

    if not prompts:
        raise SystemExit("❌ prompt.txt contains no prompts.")

    return prompts


def clean_prompt(prompt):
    """Remove aspect-ratio instructions from metadata text."""
    text = re.sub(
        r"--ar\s+\d+:\d+",
        "",
        prompt,
        flags=re.IGNORECASE,
    )
    return " ".join(text.split()).strip(" ,.-")


def safe_filename(text, max_length=75):
    name = "".join(
        char
        for char in text
        if char.isalnum() or char in " _-"
    )

    name = " ".join(name.split()).strip()
    return (name or "generated-image")[:max_length].rstrip()


def draft_title(prompt):
    text = clean_prompt(prompt)

    # Take the main subject before a list of style instructions.
    title = text.split(",")[0].strip(" .:-")

    return (title or "AI generated image")[:180]


def draft_description(prompt):
    return clean_prompt(prompt)[:200]


def draft_keywords(prompt):
    skip_words = {
        "a", "an", "and", "as", "at", "by", "for", "from",
        "in", "into", "of", "on", "or", "the", "to", "with",
        "highly", "detailed", "photorealistic", "ultra",
        "realistic", "quality", "image", "photo", "8k", "4k",
    }

    words = re.findall(
        r"[A-Za-z][A-Za-z'-]*",
        clean_prompt(prompt).lower(),
    )

    keywords = []
    seen = set()

    for word in words:
        word = word.strip("'-")

        if len(word) < 3 or word in skip_words or word in seen:
            continue

        seen.add(word)
        keywords.append(word)

        if len(keywords) >= 49:
            break

    return ", ".join(keywords)


# ============================================================
# IMAGE PROCESSING
# ============================================================

def upscale_image(input_file, output_file):
    with Image.open(input_file) as image:
        original_width, original_height = image.size

        new_size = (
            original_width * UPSCALE_FACTOR,
            original_height * UPSCALE_FACTOR,
        )

        enlarged = image.resize(
            new_size,
            Image.Resampling.LANCZOS,
        )

        if enlarged.mode not in ("RGB", "RGBA"):
            enlarged = enlarged.convert("RGB")

        enlarged.save(
            output_file,
            format="PNG",
            optimize=True,
        )

        enlarged.close()

    print(
        f"✅ Enlarged: {output_file.name} "
        f"({new_size[0]}x{new_size[1]})"
    )


# ============================================================
# STOCK CSV FILES
# ============================================================

def write_csv_file(data, site_name, headers):
    output_file = OUTPUT_DIR / f"{site_name}.csv"

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=headers,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(data)

    print(f"✅ {site_name} CSV: {output_file.resolve()}")


def write_adobe_csv(adobe_data):
    headers = [
        "Filename",
        "Title",
        "Keywords",
        "Category",
        "Releases",
    ]

    write_csv_file(adobe_data, "Adobe", headers)


def write_vecteezy_csv(vecteezy_data):
    headers = [
        "Filename",
        "Title",
        "Keywords",
    ]

    write_csv_file(vecteezy_data, "Vecteezy", headers)


def write_dreamstime_csv(dreamstime_data):
    headers = [
        "Filename",
        "Title",
        "Description",
        "Keywords",
    ]

    write_csv_file(dreamstime_data, "Dreamstime", headers)


def write_123rf_csv(rf123_data):
    headers = [
        "Filename",
        "Description",
        "Keywords",
    ]

    write_csv_file(rf123_data, "123RF", headers)


# ============================================================
# MAIN
# ============================================================

def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            '❌ OPENAI_API_KEY is not set.\n\n'
            "In PowerShell, run:\n"
            '$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY"'
        )

    if MAX_IMAGES_PER_RUN < 1:
        raise SystemExit(
            "❌ MAX_IMAGES_PER_RUN must be at least 1."
        )

    prompts = load_prompts()
    selected_prompts = prompts[:MAX_IMAGES_PER_RUN]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Prevent the SDK from automatically making extra attempts.
    client = OpenAI(max_retries=0)

    print()
    print("=" * 70)
    print("             OPENAI STOCK IMAGE GENERATOR")
    print("=" * 70)
    print(f"Model          : {MODEL_NAME}")
    print(f"Prompts found  : {len(prompts)}")
    print(f"Images this run: {len(selected_prompts)}")
    print(f"Image size     : {IMAGE_SIZE}")
    print(f"Enlarge factor : {UPSCALE_FACTOR}x")
    print(f"Output folder  : {OUTPUT_DIR.resolve()}")

    stock_data = []

    for index, prompt in enumerate(selected_prompts, start=1):
        print()
        print("=" * 70)
        print(f"[{index}/{len(selected_prompts)}] {prompt}")
        print("=" * 70)

        filename_base = (
            f"{index:03d}_{safe_filename(prompt)}"
        )

        original_file = (
            OUTPUT_DIR / f"{filename_base}_original.png"
        )

        stock_file = (
            OUTPUT_DIR / f"{filename_base}_4x.png"
        )

        try:
            response = client.images.generate(
                model=MODEL_NAME,
                prompt=prompt,
                size=IMAGE_SIZE,
                quality=IMAGE_QUALITY,
            )

            if (
                not response.data
                or not response.data[0].b64_json
            ):
                raise RuntimeError(
                    "The API returned no image data."
                )

            image_bytes = base64.b64decode(
                response.data[0].b64_json
            )

            original_file.write_bytes(image_bytes)
            print(f"✅ Original: {original_file.name}")

        except Exception as error:
            print(f"❌ Image generation failed: {error}")
            print("Stopping the batch.")
            break

        try:
            upscale_image(original_file, stock_file)
            csv_filename = stock_file.name

        except Exception as error:
            print(f"⚠️ Enlargement failed: {error}")
            print("Using the original image in the CSV files.")
            csv_filename = original_file.name

        stock_data.append({
            "Filename": csv_filename,
            "Title": draft_title(prompt),
            "Description": draft_description(prompt),
            "Keywords": draft_keywords(prompt),
            "Category": "",
            "Releases": "",
        })

    if stock_data:
        print()
        print("Writing stock metadata CSV files...")

        write_adobe_csv(stock_data)
        write_vecteezy_csv(stock_data)
        write_dreamstime_csv(stock_data)
        write_123rf_csv(stock_data)

    print()
    print("=" * 70)
    print("                         SUMMARY")
    print("=" * 70)
    print(f"Prompts found    : {len(prompts)}")
    print(f"Images generated : {len(stock_data)}")
    print(f"Output folder    : {OUTPUT_DIR.resolve()}")
    print("=" * 70)


if __name__ == "__main__":
    main()
