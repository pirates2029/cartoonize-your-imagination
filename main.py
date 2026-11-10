
import os
import tempfile

import gradio as gr
from huggingface_hub import InferenceClient


MODEL_OPTIONS = [
    "black-forest-labs/FLUX.1-schnell"
]

STYLE_OPTIONS = [
    "Anime",
    "Pop Art",
    "Cyberpunk",
    "Watercolor",
    "Ghibli Style Art"
]


# Initialise Hugging Face client
hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise RuntimeError("HF_TOKEN environment variable is not configured")

client = InferenceClient(
    provider="fal-ai",
    api_key=hf_token,
)


def generate_image(prompt: str, model: str, style: str):

    if not prompt or not prompt.strip():
        raise gr.Error("Please enter an image prompt.")

    final_prompt = f"{prompt.strip()}, rendered in {style} style"

    try:
        # Generate image using Hugging Face InferenceClient
        image = client.text_to_image(
            final_prompt,
            model=model,
        )

        # Save image to temporary file for download
        temp_file = tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False
        )

        image.save(temp_file.name)
        temp_file.close()

        return image, temp_file.name

    except Exception as e:
        raise gr.Error(f"Generation failed: {str(e)}")


theme = gr.themes.Citrus()

with gr.Blocks(
    title="Free Image Generator",
    theme=theme
) as demo:

    gr.Markdown("# 🎨 AI Image Generator")

    prompt = gr.Textbox(
        label="Prompt",
        placeholder="Astronaut riding horse on Mars..."
    )

    with gr.Row():

        model = gr.Dropdown(
            MODEL_OPTIONS,
            label="Model",
            value=MODEL_OPTIONS[0]
        )

        style = gr.Dropdown(
            STYLE_OPTIONS,
            label="Style",
            value="Anime"
        )

    generate_btn = gr.Button("Generate")

    output_image = gr.Image(
        type="pil",
        height=500,
        label="Generated Image"
    )

    download_file = gr.File(
        label="Download Image"
    )

    generate_btn.click(
        fn=generate_image,
        inputs=[prompt, model, style],
        outputs=[output_image, download_file]
    )


demo.launch(inbrowser=True)
