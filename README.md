Perfect. Since the actual repository is **`annaqitty/image-generation-anna`**, I’d make the README look like a polished open-source project and include your PayPal support link prominently but professionally. The repository is public and currently contains `README.md`, `gemini-ai.py`, `prompt.txt`, and an MIT `LICENSE`. ([GitHub][1])

Here is the updated version you can use directly:

# 🤖 Google AI Stock Image Generator

<p align="center">
  <strong>Generate. Upscale. Prepare. Automate.</strong>
</p>

<p align="center">
  A powerful Python automation tool for generating AI images with Google Gemini,
  upscaling them to high resolution, and preparing stock-ready metadata.
</p>

<p align="center">
  <a href="https://github.com/annaqitty/image-generation-anna">
    <img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github" alt="GitHub Repository">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+">
  </a>
  <a href="https://ai.google.dev/">
    <img src="https://img.shields.io/badge/Gemini-2.5%20Flash%20Image-FF6F00?style=for-the-badge&logo=google&logoColor=white" alt="Gemini">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge" alt="MIT License">
  </a>
</p>

<p align="center">
  <a href="https://paypal.me/chuakerz">
    <img src="https://img.shields.io/badge/☕%20Support%20the%20Project-PayPal-0070BA?style=for-the-badge&logo=paypal&logoColor=white" alt="Support via PayPal">
  </a>
</p>

---

## ✨ Overview

**Google AI Stock Image Generator** is a Python-based automation tool built for creators, designers, and stock contributors who want to streamline their AI image production workflow.

The application uses **Google Gemini 2.5 Flash Image** to generate images from text prompts, automatically upscales generated images using high-quality Lanczos resampling, and prepares structured metadata CSV files for popular stock photography platforms.

Instead of manually generating, resizing, organizing, and preparing metadata for every image, you can simply provide your prompts and let the application handle the workflow.

### 🚀 Workflow

```text
                prompt.txt
                    │
                    ▼
        ┌──────────────────────┐
        │   Google Gemini AI   │
        │  2.5 Flash Image     │
        └──────────┬───────────┘
                   │
                   ▼
             AI Generated
                Image
                   │
                   ▼
        ┌──────────────────────┐
        │      4× Upscale      │
        │  Pillow + Lanczos    │
        └──────────┬───────────┘
                   │
                   ▼
          High Resolution
             Stock Image
                   │
          ┌────────┼────────┐
          ▼        ▼        ▼
       Adobe   Vecteezy  Dreamstime
          │
          ▼
        123RF
```

---

# 🌟 Features

## 🎨 AI Image Generation

Generate high-quality images automatically using Google's Gemini image-generation model.

* Gemini 2.5 Flash Image
* Text-to-image generation
* Batch prompt processing
* Multiple aspect ratios
* Automated file saving
* Simple `prompt.txt` workflow

---

## ⚡ Batch Processing

Generate multiple images from a single text file.

Create:

```text
prompt.txt
```

Then add one prompt per line:

```text
A futuristic cyberpunk city at night with neon lights and cinematic atmosphere

A peaceful mountain landscape with a crystal clear lake at sunrise

Abstract flowing liquid gold and black luxury background, elegant 3D render

Modern artificial intelligence data center with glowing servers and futuristic technology
```

The generator processes each prompt sequentially.

---

## 🔍 Automatic 4× Upscaling

Generated images can automatically be enlarged by **4×** using Pillow's high-quality Lanczos resampling.

```text
Generated Image
       │
       ▼
     1×
       │
       ▼
     4×
       │
       ▼
High Resolution Image
```

Configure the upscale factor:

```python
UPSCALE_FACTOR = 4
```

---

## 📊 Automated Stock Metadata

The application prepares CSV metadata for multiple stock platforms.

| Platform    | Metadata File    |
| ----------- | ---------------- |
| Adobe Stock | `Adobe.csv`      |
| Vecteezy    | `Vecteezy.csv`   |
| Dreamstime  | `Dreamstime.csv` |
| 123RF       | `123RF.csv`      |

This helps reduce repetitive metadata preparation when working with large batches.

---

## 🔄 Smart Rate-Limit Handling

The generator includes automatic retry handling for API rate limits.

Features include:

* Automatic retries
* Exponential backoff
* Randomized jitter
* HTTP `429` handling
* Configurable retry count
* Configurable delay between successful generations

Example:

```python
MAX_RETRIES = 6
SUCCESS_DELAY = 5
```

---

## 🛡️ Safe File Management

Existing files are never overwritten.

If a file already exists, the application automatically creates a new numbered filename.

Example:

```text
generated_image_1.PNG
generated_image_1(2).PNG
generated_image_1(3).PNG
```

The same system applies to CSV files:

```text
Adobe.csv
Adobe(2).csv
Adobe(3).csv
```

Your previous generated content remains safe.

---

# 🛠️ Requirements

Before running the project, make sure you have:

* **Python 3.8+**
* Google AI Studio API key
* Internet connection
* Pillow
* Google GenAI SDK

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/annaqitty/image-generation-anna.git
cd image-generation-anna
```

## 2. Install Dependencies

```bash
pip install google-genai pillow
```

Or:

```bash
pip install -r requirements.txt
```

if a `requirements.txt` file is provided.

---

# 🔑 API Key Setup

You need a Google Gemini API key.

Create one through:

**Google AI Studio**

[https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### Windows CMD

```cmd
set GEMINI_API_KEY=your_api_key_here
```

### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

### Linux / macOS

```bash
export GEMINI_API_KEY="your_api_key_here"
```

### 🔒 Security

Never publish your API key in your GitHub repository.

Avoid:

```python
API_KEY = "your-secret-api-key"
```

Use an environment variable instead:

```python
import os

API_KEY = os.getenv("GEMINI_API_KEY")
```

---

# ⚙️ Configuration

Open:

```text
gemini-ai.py
```

and adjust the configuration section.

Example:

```python
# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "gemini-2.5-flash-image"

ASPECT_RATIO = "16:9"

UPSCALE_FACTOR = 4

MAX_RETRIES = 6

SUCCESS_DELAY = 5
```

## Aspect Ratio

Common supported options include:

```text
1:1
16:9
9:16
3:4
4:3
```

For stock photography, choose the aspect ratio according to the type of content you are creating.

---

# 📝 Prompt Configuration

Create or edit:

```text
prompt.txt
```

Use **one prompt per line**.

Example:

```text
Futuristic smart city with autonomous electric vehicles, glowing buildings, clean streets, blue technology lighting, photorealistic commercial photography

Professional modern office interior with large windows, natural sunlight, minimalist architecture, clean composition, realistic stock photography

Artificial intelligence neural network visualization, glowing digital nodes, futuristic technology background, blue and cyan lighting, high detail

Luxury gold abstract background with flowing metallic liquid, elegant composition, premium 3D render, dramatic studio lighting
```

---

# ▶️ Run the Generator

Run:

```bash
python gemini-ai.py
```

The application will automatically:

```text
1. Load prompts
2. Initialize Gemini
3. Generate images
4. Save images
5. Upscale images
6. Generate metadata
7. Create CSV files
8. Handle rate limits
9. Protect existing files
```

---

# 📁 Project Structure

```text
image-generation-anna/
│
├── gemini-ai.py
├── prompt.txt
├── README.md
├── LICENSE
│
├── generated_image_1.PNG
├── generated_image_2.PNG
├── generated_image_3.PNG
│
├── Adobe.csv
├── Vecteezy.csv
├── Dreamstime.csv
└── 123RF.csv
```

---

# 🏷️ Stock Metadata

The generator can prepare metadata for:

* Adobe Stock
* Vecteezy
* Dreamstime
* 123RF

You can customize the base keyword collection to add common stock-related terms.

Example:

```python
BASE_KEYWORDS = [
    "AI generated",
    "artificial intelligence",
    "digital",
    "technology",
    "background",
    "illustration"
]
```

Always review automatically generated metadata before submitting your content.

---

# 🧠 Prompting Tips

For more consistent stock content, build prompts using:

```text
Subject
+
Environment
+
Composition
+
Lighting
+
Style
+
Quality
```

### Example

```text
A futuristic AI robot assistant,
inside a modern technology laboratory,
centered composition with copy space,
soft cinematic lighting,
photorealistic commercial photography,
high detail, clean professional stock image
```

This structure can help produce consistent results across large batches.

---

# ⚠️ Stock Contributor Disclaimer

This project automates image generation and metadata preparation.

You are responsible for reviewing and submitting your generated content according to the rules of each stock marketplace.

Before submitting an image:

* Review the generated image for artifacts.
* Verify that the title and keywords accurately describe the image.
* Follow the marketplace's current AI-content disclosure requirements.
* Avoid unauthorized copyrighted characters.
* Avoid trademarks and logos unless you have appropriate rights.
* Avoid recognizable real people unless you have the necessary rights/releases.
* Follow each platform's current contributor guidelines.

Stock agency requirements may change over time, so always check their latest official policies before submission.

---

# 🔒 Security Best Practices

Never commit sensitive information to GitHub.

Do not upload:

```text
❌ API keys
❌ Passwords
❌ Private credentials
❌ Secret configuration files
❌ Personal access tokens
```

Recommended `.gitignore` entries:

```gitignore
.env
*.key
secrets.json
__pycache__/
*.pyc
```

If an API key is accidentally exposed, revoke or rotate it immediately.

---

# 🐛 Troubleshooting

## `ModuleNotFoundError`

Install the required dependencies:

```bash
pip install google-genai pillow
```

---

## API Key Not Found

Check your environment variable.

### PowerShell

```powershell
echo $env:GEMINI_API_KEY
```

### Linux / macOS

```bash
echo $GEMINI_API_KEY
```

If no value is displayed, configure the API key again.

---

## HTTP 429 / Rate Limit

The application includes automatic retry handling.

If rate limits continue:

* Increase `SUCCESS_DELAY`.
* Reduce the number of prompts processed at once.
* Wait before starting another batch.
* Check your current Gemini API quota and limits.

---

# 📈 Complete Workflow

```text
┌───────────────────────┐
│      Write Prompts    │
│      prompt.txt       │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│    Run gemini-ai.py   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│   Gemini AI Generation│
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│      4× Upscaling     │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│   Metadata Generation │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│     CSV Preparation   │
└───────────┬───────────┘
            │
            ▼
       Stock Upload
```

---

# 🤝 Contributing

Contributions and improvements are welcome.

### Fork the repository

```bash
git clone https://github.com/annaqitty/image-generation-anna.git
```

Create a feature branch:

```bash
git checkout -b feature/my-feature
```

Commit your changes:

```bash
git add .
git commit -m "Add new feature"
```

Push your branch:

```bash
git push origin feature/my-feature
```

Then open a Pull Request.

---

# ⭐ Support the Project

If this project saves you time or helps with your AI stock workflow, you can support its continued development.

<p align="center">
  <a href="https://paypal.me/chuakerz">
    <img src="https://img.shields.io/badge/Donate%20with-PayPal-0070BA?style=for-the-badge&logo=paypal&logoColor=white" alt="Donate with PayPal">
  </a>
</p>

### ☕ Buy Me a Coffee

Your support helps with:

* Development
* Maintenance
* New features
* API testing
* Documentation
* Future automation improvements

**Thank you for supporting open-source development! ❤️**

---

# 📜 License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for the complete license text.

---

# 🔗 Project Links

**GitHub Repository**

[https://github.com/annaqitty/image-generation-anna](https://github.com/annaqitty/image-generation-anna)

**Support the Project**

[https://paypal.me/chuakerz](https://paypal.me/chuakerz)

---

<p align="center">
  <strong>Built with ❤️ for AI creators and stock contributors.</strong>
</p>

<p align="center">
  Python • Gemini AI • Pillow • Automation • Stock Metadata
</p>

This version also uses your **real repository name and `gemini-ai.py` filename**, rather than the placeholder `main.py`/`yourusername` from the earlier draft. The GitHub repository currently confirms those project files and the MIT license. ([GitHub][1])

[View the GitHub repository](https://github.com/annaqitty/image-generation-anna?utm_source=chatgpt.com) · [Support via PayPal](https://paypal.me/chuakerz?utm_source=chatgpt.com) 

[1]: https://github.com/annaqitty/image-generation-anna "GitHub - annaqitty/image-generation-anna · GitHub"
