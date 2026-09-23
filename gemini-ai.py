import os
import csv
import time
import random
from io import BytesIO

from PIL import Image
from google import genai
from google.genai import types



API_KEY = os.environ.get("GEMINI_API_KEY")

PROMPT_FILE = "prompt.txt"

MODEL_NAME = "gemini-2.5-flash-image"

ASPECT_RATIO = "16:9"

UPSCALE_FACTOR = 4

MAX_RETRIES = 3

INITIAL_RETRY_DELAY = 8

MAX_RETRY_DELAY = 60

SUCCESS_DELAY = 5



BASE_KEYWORDS = (
    "abstract, background, beautiful, beauty, bright, color, colorful, "
    "concept, creative, decoration, design, element, graphic, illustration, "
    "light, modern, nature, pattern, shape, space, style, texture, vibrant, "
    "wallpaper, art, digital, futuristic, glowing, gradient, geometric, "
    "layout, minimal, render, 3d, wave, dynamic, energy, flow, smooth"
)



if not API_KEY:
    print()
    print("❌ GEMINI_API_KEY environment variable is not set.")
    print()
    print("PowerShell:")
    print('  $env:GEMINI_API_KEY="YOUR_NEW_API_KEY"')
    print()
    raise SystemExit(1)


try:
    client = genai.Client(api_key=API_KEY)

    print("✅ Google Gen AI client initialized.")

except Exception as e:
    print()
    print("❌ Failed to initialize Google Gen AI client.")
    print()
    print(f"{type(e).__name__}: {e}")
    print()

    raise SystemExit(1)



def get_unique_filename(filepath):
    """
    If the file exists, append (2), (3), etc.

    Example:
        image.PNG
        image(2).PNG
        image(3).PNG
    """

    if not os.path.exists(filepath):
        return filepath

    base, ext = os.path.splitext(filepath)

    counter = 2

    while True:
        new_filename = f"{base}({counter}){ext}"

        if not os.path.exists(new_filename):
            return new_filename

        counter += 1



def read_prompts_from_file(filename):

    if not os.path.exists(filename):
        print()
        print(f"❌ Error: '{filename}' was not found.")
        print("Create prompt.txt and put one prompt per line.")
        print()
        return []

    try:

        with open(filename, "r", encoding="utf-8") as file:

            prompts = []

            for line in file:

                line = line.strip()

                if line:
                    prompts.append(line)

        return prompts

    except Exception as e:

        print(f"❌ Error reading {filename}: {e}")

        return []



def get_error_text(error):

    return str(error).lower()


def is_rate_limit_error(error):

    error_text = get_error_text(error)

    return (
        "429" in error_text
        or "resource_exhausted" in error_text
        or "resource exhausted" in error_text
        or "rate limit" in error_text
        or "rate_limit_exceeded" in error_text
        or "too_many_requests" in error_text
    )


def is_daily_quota_error(error):

    error_text = get_error_text(error)

    return (
        "quota_exceeded" in error_text
        or "daily quota" in error_text
        or "quota exceeded" in error_text
        or "per day" in error_text
        or "requests per day" in error_text
        or "rpd" in error_text
    )


def is_temporary_server_error(error):

    error_text = get_error_text(error)

    return (
        "503" in error_text
        or "unavailable" in error_text
        or "500" in error_text
        or "internal server error" in error_text
    )



def generate_image(prompt):

    """
    Generate one image.

    429 rate limits:
        Retry with exponential backoff.

    Daily quota:
        Stop immediately because retrying will not help.

    500/503:
        Retry because these are normally temporary server errors.
    """

    for attempt in range(1, MAX_RETRIES + 1):

        try:

            print(
                f"      API attempt "
                f"{attempt}/{MAX_RETRIES}..."
            )

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(
                        aspect_ratio=ASPECT_RATIO
                    ),
                ),
            )


            for part in response.parts:

                if part.inline_data:

                    image_bytes = part.inline_data.data

                    if image_bytes:
                        return image_bytes

            raise RuntimeError(
                "Google returned a response without image data."
            )

        except Exception as e:


            if is_daily_quota_error(e):

                print()
                print("      ❌ DAILY QUOTA EXCEEDED.")
                print()
                print(
                    "      Retrying will not fix this request."
                )
                print(
                    "      Check your Gemini API quota/billing."
                )
                print()

                raise RuntimeError(
                    "Gemini daily quota exceeded."
                ) from e


            if is_rate_limit_error(e):

                if attempt >= MAX_RETRIES:

                    print()
                    print(
                        "      ❌ Rate limit persists after "
                        f"{MAX_RETRIES} attempts."
                    )
                    print()

                    raise

                delay = min(
                    INITIAL_RETRY_DELAY * (2 ** (attempt - 1)),
                    MAX_RETRY_DELAY
                )

                jitter = random.uniform(0.5, 2.5)

                wait_time = delay + jitter

                print()
                print(
                    "      ⚠️ Google returned "
                    "429 RESOURCE_EXHAUSTED."
                )

                print(
                    f"      Waiting {wait_time:.1f} seconds..."
                )

                time.sleep(wait_time)

                continue


            if is_temporary_server_error(e):

                if attempt >= MAX_RETRIES:

                    print()
                    print(
                        "      ❌ Server error persists after "
                        f"{MAX_RETRIES} attempts."
                    )
                    print()

                    raise

                delay = min(
                    INITIAL_RETRY_DELAY * (2 ** (attempt - 1)),
                    MAX_RETRY_DELAY
                )

                jitter = random.uniform(0.5, 2.5)

                wait_time = delay + jitter

                print()
                print(
                    f"      ⚠️ Temporary Google server error."
                )

                print(
                    f"      Waiting {wait_time:.1f} seconds..."
                )

                time.sleep(wait_time)

                continue


            print()
            print(
                f"      ❌ API error: "
                f"{type(e).__name__}: {e}"
            )
            print()

            raise

    raise RuntimeError("Image generation failed.")



def upscale_image_4x(image_bytes):

    """
    Convert generated bytes to PIL image
    and enlarge 4x.
    """

    image = Image.open(BytesIO(image_bytes))

    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")

    original_width, original_height = image.size

    new_width = original_width * UPSCALE_FACTOR
    new_height = original_height * UPSCALE_FACTOR

    print(
        f"      Original size: "
        f"{original_width}x{original_height}"
    )

    print(
        f"      4x size: "
        f"{new_width}x{new_height}"
    )

    image = image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    return image



def save_image(image, filename):

    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")

    image.save(
        filename,
        "PNG",
        optimize=True
    )



def generate_images_from_prompts():

    adobe_data = []

    vecteezy_data = []

    dreamstime_data = []

    rf123_data = []

    prompts = read_prompts_from_file(PROMPT_FILE)

    total_images = len(prompts)

    if total_images == 0:

        print("❌ No prompts found.")

        return (
            [],
            [],
            [],
            []
        )

    print()
    print("=" * 70)
    print(
        f"Found {total_images} prompts "
        f"in {PROMPT_FILE}"
    )
    print(
        f"Model: {MODEL_NAME}"
    )
    print(
        f"Aspect Ratio: {ASPECT_RATIO}"
    )
    print(
        f"Upscale: {UPSCALE_FACTOR}x"
    )
    print(
        f"Max Retries: {MAX_RETRIES}"
    )
    print("=" * 70)
    print()


    for i, prompt in enumerate(
        prompts,
        start=1
    ):

        print()
        print("=" * 70)

        print(
            f"[{i}/{total_images}] Processing"
        )

        print("=" * 70)

        print()
        print("Prompt:")
        print(prompt)
        print()

        description = prompt.strip()

        if len(description) > 200:

            description = (
                description[:197] + "..."
            )

        base_filename = (
            f"generated_image_{i}.PNG"
        )

        final_filename = get_unique_filename(
            base_filename
        )

        try:


            print("🖼️ Generating image...")

            image_bytes = generate_image(prompt)

            print(
                "      ✅ Image generated."
            )


            print(
                "📐 Upscaling image 4x..."
            )

            image = upscale_image_4x(
                image_bytes
            )


            print(
                "💾 Saving PNG..."
            )

            save_image(
                image,
                final_filename
            )

            print(
                f"      ✅ Saved: "
                f"{final_filename}"
            )


            adobe_data.append({
                "Filename": final_filename,
                "Title": description,
                "Keywords": BASE_KEYWORDS,
                "Category": "4",
                "Releases": ""
            })


            vecteezy_data.append({
                "Filename": final_filename,
                "Title": description,
                "Keywords": BASE_KEYWORDS
            })


            dreamstime_data.append({
                "Filename": final_filename,
                "Title": description,
                "Description": description,
                "Keywords": BASE_KEYWORDS
            })


            rf123_data.append({
                "Filename": final_filename,
                "Description": description,
                "Keywords": BASE_KEYWORDS
            })

            print(
                "      ✅ Metadata added "
                "for all agencies."
            )

        except Exception as e:

            print()
            print(
                f"❌ Error generating image {i}:"
            )

            print(
                f"      {type(e).__name__}: {e}"
            )

            print()


            if (
                "quota" in str(e).lower()
                or "daily" in str(e).lower()
            ):

                print(
                    "🛑 Stopping because the "
                    "Gemini quota is exhausted."
                )

                break

            print(
                "      Skipping this prompt."
            )


        if i < total_images:

            print(
                f"      Waiting "
                f"{SUCCESS_DELAY}s..."
            )

            time.sleep(
                SUCCESS_DELAY
            )

    return (
        adobe_data,
        vecteezy_data,
        dreamstime_data,
        rf123_data
    )



def write_csv_file(
    data,
    agency_name,
    headers
):

    if not data:
        return

    filename = get_unique_filename(
        f"{agency_name}.csv"
    )

    try:

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=headers
            )

            writer.writeheader()

            writer.writerows(data)

        print(
            f"✅ {agency_name} CSV saved: "
            f"{filename}"
        )

    except Exception as e:

        print(
            f"❌ Failed to write "
            f"{agency_name} CSV: {e}"
        )



def write_adobe_csv(adobe_data):

    headers = [
        "Filename",
        "Title",
        "Keywords",
        "Category",
        "Releases"
    ]

    write_csv_file(
        adobe_data,
        "Adobe",
        headers
    )


def write_vecteezy_csv(vecteezy_data):

    headers = [
        "Filename",
        "Title",
        "Keywords"
    ]

    write_csv_file(
        vecteezy_data,
        "Vecteezy",
        headers
    )


def write_dreamstime_csv(dreamstime_data):

    headers = [
        "Filename",
        "Title",
        "Description",
        "Keywords"
    ]

    write_csv_file(
        dreamstime_data,
        "Dreamstime",
        headers
    )


def write_123rf_csv(rf123_data):

    headers = [
        "Filename",
        "Description",
        "Keywords"
    ]

    write_csv_file(
        rf123_data,
        "123RF",
        headers
    )



def main():

    print()
    print("=" * 70)
    print(
        "          GOOGLE AI IMAGE GENERATOR"
    )
    print("=" * 70)
    print()

    print(
        f"Model   : {MODEL_NAME}"
    )

    print(
        f"Ratio   : {ASPECT_RATIO}"
    )

    print(
        f"Upscale : {UPSCALE_FACTOR}x"
    )

    print()

    (
        adobe_data,
        vecteezy_data,
        dreamstime_data,
        rf123_data
    ) = generate_images_from_prompts()

    print()


    write_adobe_csv(
        adobe_data
    )

    write_vecteezy_csv(
        vecteezy_data
    )

    write_dreamstime_csv(
        dreamstime_data
    )

    write_123rf_csv(
        rf123_data
    )


    print()
    print("=" * 70)
    print(
        "                    COMPLETE"
    )
    print("=" * 70)
    print()

    print(
        f"Successful images: "
        f"{len(adobe_data)}"
    )

    print()

    print(
        "✅ Process finished."
    )

    print()



if __name__ == "__main__":
    main()
