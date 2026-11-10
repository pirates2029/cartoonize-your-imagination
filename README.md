# 🎨 Cartoonize Your Imagination

An AI-powered text-to-image generator built with [Gradio](https://gradio.app/) and [Hugging Face](https://huggingface.co/). Type a prompt, pick an art style, and watch your imagination come to life as a cartoon, anime, cyberpunk, or watercolor masterpiece.

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-6.31+-orange?logo=gradio&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- **Text-to-Image Generation** — Describe anything and get an AI-generated image in seconds.
- **Multiple Art Styles** — Choose from:
  - 🎌 Anime
  - 🟡 Pop Art
  - 🌆 Cyberpunk
  - 🎨 Watercolor
  - 🏔️ Ghibli Style Art
- **Powered by FLUX.1-schnell** — Uses the `black-forest-labs/FLUX.1-schnell` model via the [fal-ai](https://fal.ai/) inference provider on Hugging Face.
- **One-Click Download** — Download your generated image as a PNG file.
- **Clean Web UI** — Responsive Gradio interface with the Citrus theme.

---

## 🖼️ How It Works

1. Enter a text prompt describing the image you want (e.g., _"Astronaut riding horse on Mars"_).
2. Select an AI model (currently FLUX.1-schnell).
3. Pick an art style to apply.
4. Click **Generate** and wait a few seconds.
5. View the result and download it if you like it!

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** — fast Python package manager (recommended)
- A **Hugging Face API token** with access to inference endpoints — [get one here](https://huggingface.co/settings/tokens)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/cartoonize-your-imagination.git
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
   pip install gradio huggingface-hub pillow
   ```

3. **Set your Hugging Face token**

   ```bash
   export HF_TOKEN="hf_your_token_here"
   ```

   On Windows (PowerShell):

   ```powershell
   $env:HF_TOKEN = "hf_your_token_here"
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

| Environment Variable | Required | Description                                      |
| -------------------- | -------- | ------------------------------------------------ |
| `HF_TOKEN`           | ✅ Yes    | Hugging Face API token for inference access       |

---

## 🛠️ Tech Stack

| Component       | Technology                                                                                       |
| --------------- | ------------------------------------------------------------------------------------------------ |
| **UI**          | [Gradio](https://gradio.app/) 6.31+                                                             |
| **AI Model**    | [FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell) by Black Forest Labs  |
| **Inference**   | [Hugging Face Inference API](https://huggingface.co/docs/huggingface_hub/guides/inference) via fal-ai |
| **Language**    | Python 3.12+                                                                                     |
| **Packaging**   | [uv](https://docs.astral.sh/uv/)                                                                |

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
