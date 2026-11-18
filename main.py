import base64
import io
import os
import tempfile
from typing import Literal, cast

import gradio as gr
import requests
from huggingface_hub import InferenceClient
from PIL import Image


# ── Provider → Model mapping ──────────────────────────────────────────────
# Cloudflare model IDs use the @cf/ prefix in the API URL.
# FLUX 2 models require multipart/form-data input instead of JSON.
CLOUDFLARE_MULTIPART_MODELS = {
    "@cf/black-forest-labs/flux-2-dev",
    "@cf/black-forest-labs/flux-2-klein-4b",
    "@cf/black-forest-labs/flux-2-klein-9b",
}

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
    "cloudflare": [
        "@cf/black-forest-labs/flux-1-schnell",
        "@cf/black-forest-labs/flux-2-dev",
        "@cf/black-forest-labs/flux-2-klein-4b",
        "@cf/black-forest-labs/flux-2-klein-9b",
    ],
}

PROVIDER_OPTIONS = list(PROVIDER_MODELS.keys())
DEFAULT_PROVIDER = PROVIDER_OPTIONS[3]
DEFAULT_MODELS = PROVIDER_MODELS[DEFAULT_PROVIDER]

STYLE_OPTIONS = [
    "Anime",
    "Pop Art",
    "Cyberpunk",
    "Watercolor",
    "Ghibli Style Art",
    "Realistic"
]

ProviderName = Literal[
    "wavespeed",
    "fal-ai",
    "hf-inference",
]


def generate_system_prompt(prompt: str, style: str = "Realistic") -> str:
    """Build a complete image-generation prompt for the requested style."""
    prompt = prompt.strip() if prompt else ""
    if not prompt:
        raise ValueError("An image prompt is required.")

    style = style.strip() if style else "Realistic"

    if style == "Realistic":
        final_prompt = (
            "Photorealistic, ultra-realistic real-world photography."
            "Depict the scene exactly as described, preserving the user's original intent and all important details."
            "Make it look like a genuine photograph captured with a professional DSLR or mirrorless camera."
            "Use realistic human anatomy, natural proportions, authentic textures, physically accurate lighting, natural shadows, realistic reflections, true-to-life colours, and environmental details."
            "Apply professional photographic composition, realistic camera perspective, natural depth of field, and accurate lens characteristics. Ensure every object and interaction follows real-world physics."
            "High detail, crisp focus, lifelike appearance, professional photography quality."
            "Avoid cartoon, illustration, painting, CGI, 3D-rendered appearance, artificial textures, exaggerated effects, distortions, and unnatural elements."
            "Here is the prompt to be used for image generation: " + prompt
        )
    else:
        final_prompt = (
            f"{prompt.strip()}, rendered in {style} style."
        )

    return final_prompt


# ── Authentication ─────────────────────────────────────────────────────────
hf_token = os.getenv("HF_TOKEN")
cloudflare_account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
cloudflare_api_token = os.getenv("CLOUDFLARE_API_TOKEN")

if not hf_token:
    raise RuntimeError("HF_TOKEN environment variable is not configured")


def _get_hf_client(provider: str) -> InferenceClient:
    """Return an InferenceClient configured for the given HF provider."""
    hf_provider = cast(ProviderName, provider)
    return InferenceClient(
        provider=hf_provider,
        api_key=hf_token,
    )


def _generate_cloudflare(prompt: str, model: str) -> Image.Image:
    """Call the Cloudflare Workers AI REST API and return a PIL Image.

    FLUX 1 models accept a JSON payload, while FLUX 2 models require
    multipart/form-data.
    """
    if not cloudflare_account_id or not cloudflare_api_token:
        raise RuntimeError(
            "CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN environment "
            "variables must be set to use the Cloudflare provider."
        )

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{cloudflare_account_id}/ai/run/{model}"
    )

    headers = {"Authorization": f"Bearer {cloudflare_api_token}"}

    if model in CLOUDFLARE_MULTIPART_MODELS:
        # FLUX 2 models require multipart/form-data
        response = requests.post(
            url,
            headers=headers,
            data={"prompt": prompt, "steps": "25"},
            timeout=120,
        )
    else:
        # FLUX 1 models use JSON
        response = requests.post(
            url,
            headers=headers,
            json={"prompt": prompt, "steps": 8},
            timeout=120,
        )

    response.raise_for_status()

    content_type = response.headers.get("content-type", "")

    # Cloudflare may return raw binary image data or a JSON envelope
    if "application/json" in content_type:
        data = response.json()

        # Check for API-level errors
        if not data.get("success", True):
            errors = data.get("errors", [])
            raise RuntimeError(
                f"Cloudflare API error: {errors or data}"
            )

        # The image is base64-encoded inside the result object
        result = data.get("result", {})
        image_b64 = result.get("image")
        if not image_b64:
            raise RuntimeError(
                f"Unexpected Cloudflare response (no image field): "
                f"{list(result.keys()) if isinstance(result, dict) else result}"
            )
        return Image.open(io.BytesIO(base64.b64decode(image_b64)))

    # Raw binary PNG / JPEG response
    return Image.open(io.BytesIO(response.content))


def on_provider_change(provider: str):
    """Update the model dropdown when the provider changes."""
    models = PROVIDER_MODELS.get(provider, [])
    return gr.update(choices=models, value=models[0] if models else None)


def generate_image(prompt: str, provider: str, model: str, style: str):
    """Generate an image with the selected provider, model and style."""

    if not prompt or not prompt.strip():
        raise gr.Error("Please enter an image prompt.")

    final_prompt = generate_system_prompt(prompt, style)

    try:
        if provider == "cloudflare":
            image = _generate_cloudflare(final_prompt, model)
        else:
            client = _get_hf_client(provider)
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


demo.launch(inbrowser=True, theme=theme)
