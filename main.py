
import os
import tempfile

import gradio as gr
from huggingface_hub import InferenceClient


# ── Provider → Model mapping ──────────────────────────────────────────────
PROVIDER_MODELS = {
    "wavespeed": [
        "black-forest-labs/FLUX.1-dev",
    ],
    "fal-ai": [
        "black-forest-labs/FLUX.1-dev",
        "black-forest-labs/FLUX.1-schnell",
    ],
    "hf-inference": [
        "stabilityai/stable-diffusion-3-medium-diffusers",
    ],
}

PROVIDER_OPTIONS = list(PROVIDER_MODELS.keys())
DEFAULT_PROVIDER = PROVIDER_OPTIONS[0]
DEFAULT_MODELS = PROVIDER_MODELS[DEFAULT_PROVIDER]

STYLE_OPTIONS = [
    "Anime",
    "Pop Art",
    "Cyberpunk",
    "Watercolor",
    "Ghibli Style Art",
]


# ── Hugging Face authentication ───────────────────────────────────────────
hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise RuntimeError("HF_TOKEN environment variable is not configured")


def _get_client(provider: str) -> InferenceClient:
    """Return an InferenceClient configured for the given provider."""
    return InferenceClient(
        provider=provider,
        api_key=hf_token,
    )


def on_provider_change(provider: str):
    """Update the model dropdown when the provider changes."""
    models = PROVIDER_MODELS.get(provider, [])
    return gr.update(choices=models, value=models[0] if models else None)


def generate_image(prompt: str, provider: str, model: str, style: str):
    """Generate an image with the selected provider, model and style."""

    if not prompt or not prompt.strip():
        raise gr.Error("Please enter an image prompt.")

    final_prompt = f"{prompt.strip()}, rendered in {style} style"

    try:
        client = _get_client(provider)

        # Generate image using Hugging Face InferenceClient
        image = client.text_to_image(
            final_prompt,
            model=model,
        )

        # Save image to temporary file for download
        temp_file = tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False,
        )

        image.save(temp_file.name)
        temp_file.close()

        return image, temp_file.name

    except Exception as e:
        raise gr.Error(f"Generation failed: {str(e)}")


# ── UI ─────────────────────────────────────────────────────────────────────
theme = gr.themes.Citrus()

with gr.Blocks(
    title="Free Image Generator",
    theme=theme,
) as demo:

    gr.Markdown("# 🎨 AI Image Generator")

    prompt = gr.Textbox(
        label="Prompt",
        placeholder="Astronaut riding horse on Mars...",
    )

    with gr.Row():

        provider = gr.Dropdown(
            PROVIDER_OPTIONS,
            label="Provider",
            value=DEFAULT_PROVIDER,
        )

        model = gr.Dropdown(
            DEFAULT_MODELS,
            label="Model",
            value=DEFAULT_MODELS[0],
        )

        style = gr.Dropdown(
            STYLE_OPTIONS,
            label="Style",
            value="Anime",
        )

    # Dynamically update models when the provider changes
    provider.change(
        fn=on_provider_change,
        inputs=[provider],
        outputs=[model],
    )

    generate_btn = gr.Button("Generate")

    output_image = gr.Image(
        type="pil",
        height=500,
        label="Generated Image",
    )

    download_file = gr.File(
        label="Download Image",
    )

    generate_btn.click(
        fn=generate_image,
        inputs=[prompt, provider, model, style],
        outputs=[output_image, download_file],
    )


demo.launch(inbrowser=True)
