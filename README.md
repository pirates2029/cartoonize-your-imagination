# 🎨 Cartoonize Your Imagination

An AI-powered text-to-image generator built with [Gradio](https://gradio.app/) and multiple inference providers. Type a prompt, pick a provider, model, and art style — then watch your imagination come to life.

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-6.31+-orange?logo=gradio&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- **Text-to-Image Generation** — Describe anything and get an AI-generated image in seconds.
- **Multiple Inference Providers** — Switch between providers on the fly:
  | Provider | Models |
  | --- | --- |
  | **Cloudflare** (default) | `flux-1-schnell`, `flux-2-dev`, `flux-2-klein-4b`, `flux-2-klein-9b` |
  | **fal-ai** | `FLUX.1-dev`, `FLUX.1-schnell` |
  | **wavespeed** | `FLUX.1-dev` |
  | **hf-inference** | `stable-diffusion-3-medium-diffusers` |
- **6 Art Styles** — Anime · Pop Art · Cyberpunk · Watercolor · Ghibli Style Art · Realistic
- **Realistic Mode** — Generates photorealistic images with a detailed photography-focused prompt.
- **Dynamic Model Selection** — The model dropdown updates automatically when you switch providers.
- **One-Click Download** — Download your generated image as a PNG file.
- **Clean Web UI** — Responsive Gradio interface with the Citrus theme.

---

## 🖼️ How It Works

1. Enter a text prompt describing the image you want (e.g., _"Astronaut riding horse on Mars"_).
2. Select an inference **provider** (Cloudflare, fal-ai, wavespeed, or hf-inference).
3. Pick a **model** (choices update based on the selected provider).
4. Choose an **art style** to apply.
5. Click **Generate** and wait a few seconds.
6. View the result and download it if you like it!

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** — fast Python package manager (recommended)
- A **Hugging Face API token** — [get one here](https://huggingface.co/settings/tokens)
- _(Optional)_ A **Cloudflare Workers AI** account — required only for the Cloudflare provider

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/pirates2029/cartoonize-your-imagination.git
   cd cartoonize-your-imagination
   ```

2. **Create a virtual environment and install dependencies**

   Using **uv** (recommended):

   ```bash
   uv sync
   ```

   Or using **pip**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # On Windows: .venv\Scripts\activate
   pip install gradio huggingface-hub pillow requests
   ```

3. **Set your environment variables**

   ```bash
   export HF_TOKEN="hf_your_token_here"

   # Only needed for the Cloudflare provider:
   export CLOUDFLARE_ACCOUNT_ID="your_account_id"
   export CLOUDFLARE_API_TOKEN="your_api_token"
   ```

   On Windows (PowerShell):

   ```powershell
   $env:HF_TOKEN = "hf_your_token_here"
   $env:CLOUDFLARE_ACCOUNT_ID = "your_account_id"
   $env:CLOUDFLARE_API_TOKEN = "your_api_token"
   ```

   > **Tip:** You can also create a `.env` file (already in `.gitignore`) and use a tool like `direnv` or `python-dotenv` to load it automatically.

### Run the App

```bash
uv run python main.py
```

Or, if you activated the virtual environment manually:

```bash
python main.py
```

The app will automatically open in your default browser at **http://127.0.0.1:7860**.

---

## 📁 Project Structure

```
cartoonize-your-imagination/
├── main.py              # Application entry point & Gradio UI
├── pyproject.toml       # Project metadata & dependencies
├── uv.lock              # Locked dependency versions
├── .python-version      # Python version pin (3.12)
├── .gitignore           # Git ignore rules
└── README.md            # You are here
```

---

## 🔧 Configuration

| Environment Variable     | Required | Description                                                |
| ------------------------ | -------- | ---------------------------------------------------------- |
| `HF_TOKEN`               | ✅ Yes   | Hugging Face API token for inference access                |
| `CLOUDFLARE_ACCOUNT_ID`  | ⚡ Conditional | Cloudflare account ID (required for Cloudflare provider)  |
| `CLOUDFLARE_API_TOKEN`   | ⚡ Conditional | Cloudflare API token (required for Cloudflare provider)   |

---

## 🛠️ Tech Stack

| Component       | Technology                                                                                        |
| --------------- | ------------------------------------------------------------------------------------------------- |
| **UI**          | [Gradio](https://gradio.app/) 6.31+                                                              |
| **AI Models**   | [FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev), [FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell), [FLUX 2 Dev / Klein](https://developers.cloudflare.com/workers-ai/models/), [Stable Diffusion 3 Medium](https://huggingface.co/stabilityai/stable-diffusion-3-medium-diffusers) |
| **Inference**   | [Hugging Face Inference API](https://huggingface.co/docs/huggingface_hub/guides/inference), [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/) |
| **Language**    | Python 3.12+                                                                                      |
| **Packaging**   | [uv](https://docs.astral.sh/uv/)                                                                 |

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source. See the [LICENSE](LICENSE) file for details.
