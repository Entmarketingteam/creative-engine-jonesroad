"""
Replicate provider — image generation and video generation via Replicate's HTTP API.

Image models (cheapest to most capable):
- FLUX.1 Schnell ($0.003) — fast drafts, no reference image support
- FLUX.1 Dev ($0.01) — better quality drafts, no reference image support
- Ideogram 3.0 Turbo ($0.03) — best text rendering, style reference support (up to 3)
- FLUX Kontext Pro (~$0.05) — reference image support, keeps product identity

Video models:
- LTX Video ($0.04) — ultra-budget, image-to-video
- Minimax Video-01 ($0.10) — mid-tier, image-to-video

All generation is ASYNCHRONOUS (submit prediction → poll for result).

Replicate API: https://replicate.com/docs/reference/http
- POST /v1/models/{owner}/{name}/predictions → create prediction
- GET  /v1/predictions/{id} → get prediction status + output
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

from .. import config
from ..utils import (
    print_status,
    submit_replicate_prediction,
    poll_replicate_prediction,
)

# Provider sync flags — Replicate is always async
image_IS_SYNC = False
video_IS_SYNC = False

# --- Replicate image model identifiers (owner/name format) ---
_IMAGE_MODELS = {
    "flux-schnell": "black-forest-labs/flux-schnell",
    "flux-dev": "black-forest-labs/flux-dev",
    "ideogram": "ideogram-ai/ideogram-v3-turbo",
    "flux-kontext": "black-forest-labs/flux-kontext-pro",
}

# --- Replicate video model identifiers ---
_VIDEO_MODELS = {
    "minimax-video": "minimax/video-01",
    "ltx-video": "lightricks/ltx-video",
}

# --- Aspect ratio mapping for FLUX (width x height) ---
_FLUX_SIZES = {
    "9:16": {"width": 768, "height": 1344},
    "2:3":  {"width": 768, "height": 1152},
    "16:9": {"width": 1344, "height": 768},
    "3:2":  {"width": 1152, "height": 768},
    "1:1":  {"width": 1024, "height": 1024},
    "4:5":  {"width": 896, "height": 1120},
    "5:4":  {"width": 1120, "height": 896},
    "3:4":  {"width": 896, "height": 1152},
    "4:3":  {"width": 1152, "height": 896},
}


# ---------------------------------------------------------------------------
# Image Generation
# ---------------------------------------------------------------------------

def submit_image(prompt, reference_urls=None, reference_paths=None,
                 aspect_ratio="9:16", resolution="1K",
                 model="flux-schnell", **kwargs):
    """
    Submit an image generation prediction to Replicate.

    Args:
        prompt: Image prompt text
        reference_urls: Hosted reference image URLs
            - Ignored by flux-schnell and flux-dev (no reference support)
            - Used as style_reference_images by ideogram (up to 3)
            - First URL used as image_url by flux-kontext
        reference_paths: Ignored (Replicate needs URLs, not local paths)
        aspect_ratio: Aspect ratio string (e.g., "9:16")
        resolution: Ignored for Replicate models
        model: "flux-schnell", "flux-dev", "ideogram", or "flux-kontext"

    Returns:
        str: prediction_id for polling
    """
    replicate_model = _IMAGE_MODELS.get(model)
    if not replicate_model:
        raise ValueError(f"Replicate doesn't support image model: '{model}'. "
                         f"Available: {list(_IMAGE_MODELS.keys())}")

    # --- FLUX Schnell ---
    if model == "flux-schnell":
        input_data = {
            "prompt": prompt,
            "num_outputs": 1,
            "output_format": "png",
            "go_fast": True,
        }
        if aspect_ratio:
            input_data["aspect_ratio"] = aspect_ratio

    # --- FLUX Dev ---
    elif model == "flux-dev":
        input_data = {
            "prompt": prompt,
            "num_outputs": 1,
            "output_format": "png",
            "guidance": 3.5,
            "num_inference_steps": 28,
        }
        if aspect_ratio:
            input_data["aspect_ratio"] = aspect_ratio

    # --- Ideogram 3.0 Turbo ---
    elif model == "ideogram":
        input_data = {
            "prompt": prompt,
        }
        if aspect_ratio:
            input_data["aspect_ratio"] = aspect_ratio
        # Ideogram supports up to 3 style reference images
        if reference_urls:
            input_data["style_reference_images"] = list(reference_urls[:3])

    # --- FLUX Kontext Pro ---
    elif model == "flux-kontext":
        input_data = {
            "prompt": prompt,
        }
        if aspect_ratio:
            input_data["aspect_ratio"] = aspect_ratio
        # Kontext takes a single reference image to preserve product identity
        if reference_urls:
            input_data["image_url"] = reference_urls[0]

    else:
        raise ValueError(f"No payload builder for model: {model}")

    result = submit_replicate_prediction(replicate_model, input_data)
    return result["prediction_id"]


def poll_image(prediction_id, max_wait=120, poll_interval=3, quiet=False):
    """
    Poll a Replicate image prediction. Returns GenerationResult dict.

    Args:
        prediction_id: The prediction ID from submit_image
        max_wait: Maximum seconds to wait (FLUX is fast — 120s is generous)
        poll_interval: Seconds between checks
        quiet: Suppress status messages

    Returns:
        dict: GenerationResult with status, result_url, task_id
    """
    return poll_replicate_prediction(
        prediction_id, max_wait=max_wait,
        poll_interval=poll_interval, quiet=quiet
    )


# ---------------------------------------------------------------------------
# Video Generation
# ---------------------------------------------------------------------------

def submit_video(prompt, image_url=None, model="minimax-video",
                 duration="5", aspect_ratio="9:16", mode="pro", **kwargs):
    """
    Submit a video generation prediction to Replicate.

    Args:
        prompt: Video prompt text
        image_url: Source image URL (start frame for image-to-video)
        model: "minimax-video" or "ltx-video"
        duration: Video duration in seconds (model-dependent)
        aspect_ratio: Aspect ratio string
        mode: Ignored for Replicate video models

    Returns:
        str: prediction_id for polling
    """
    replicate_model = _VIDEO_MODELS.get(model)
    if not replicate_model:
        raise ValueError(f"Replicate doesn't support video model: '{model}'. "
                         f"Available: {list(_VIDEO_MODELS.keys())}")

    if model == "minimax-video":
        input_data = {
            "prompt": prompt,
            "prompt_optimizer": True,
        }
        if image_url:
            input_data["first_frame_image"] = image_url

    elif model == "ltx-video":
        input_data = {
            "prompt": prompt,
        }
        if image_url:
            input_data["image"] = image_url
        # LTX Video uses width/height for aspect ratio
        size = _FLUX_SIZES.get(aspect_ratio, _FLUX_SIZES["9:16"])
        input_data["width"] = size["width"]
        input_data["height"] = size["height"]

    else:
        raise ValueError(f"No payload builder for model: {model}")

    result = submit_replicate_prediction(replicate_model, input_data)
    return result["prediction_id"]


def poll_video(prediction_id, max_wait=600, poll_interval=10, quiet=False):
    """
    Poll a Replicate video prediction. Returns GenerationResult dict.

    Args:
        prediction_id: The prediction ID from submit_video
        max_wait: Maximum seconds to wait
        poll_interval: Seconds between checks
        quiet: Suppress status messages

    Returns:
        dict: GenerationResult with status, result_url, task_id
    """
    return poll_replicate_prediction(
        prediction_id, max_wait=max_wait,
        poll_interval=poll_interval, quiet=quiet
    )


# ---------------------------------------------------------------------------
# Parallel Polling
# ---------------------------------------------------------------------------

def poll_tasks_parallel(prediction_ids, max_wait=600, poll_interval=5):
    """
    Poll multiple Replicate predictions concurrently.

    Args:
        prediction_ids: List of prediction ID strings
        max_wait: Max seconds to wait per prediction
        poll_interval: Seconds between checks

    Returns:
        dict: prediction_id -> GenerationResult
    """
    if not prediction_ids:
        return {}

    total = len(prediction_ids)
    completed = []
    results = {}

    def _poll_one(pid):
        result = poll_replicate_prediction(
            pid, max_wait=max_wait,
            poll_interval=poll_interval, quiet=True
        )
        completed.append(pid)
        print_status(f"Prediction {pid[:12]}... done ({len(completed)}/{total})", "OK")
        return result

    max_workers = min(total, 20)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_poll_one, pid): pid
            for pid in prediction_ids
        }
        for future in as_completed(futures):
            pid = futures[future]
            try:
                results[pid] = future.result()
            except Exception as e:
                completed.append(pid)
                print_status(f"Prediction {pid[:12]}... failed: {e}", "XX")
                results[pid] = {
                    "status": "error",
                    "task_id": pid,
                    "error": str(e),
                }

    return results
