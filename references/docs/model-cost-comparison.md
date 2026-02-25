# Model & Cost Comparison — AI Image + Video Generation

A complete breakdown of cloud and local options for DTC ad content generation. Updated February 2026.

---

## Current Stack (Creative Content Engine)

| Model | Type | Cost/Unit | Provider | Quality | Speed |
|-------|------|-----------|----------|---------|-------|
| Nano Banana Pro | Image | $0.13 | Google AI Studio | Excellent | ~10s |
| Nano Banana | Image | $0.04 | Google AI Studio | Very Good | ~8s |
| GPT Image 1.5 | Image | ~$0.08 | WaveSpeed AI | Excellent | ~12s |
| Veo 3.1 | Video | $0.50 | Google AI Studio | Excellent (native audio/dialogue) | ~45-90s |
| Kling 3.0 | Video | $0.30 | Kie AI / WaveSpeed | Excellent (cinematic) | ~2-4 min |
| Sora 2 Pro | Video | $0.30 | Kie AI / WaveSpeed | Excellent (long-form) | ~10-12 min |

---

## Cheaper Cloud Alternatives

### Images

| Model | Cost/Unit | Quality vs Nano Banana Pro | Reference Image Support | Provider | Notes |
|-------|-----------|---------------------------|------------------------|----------|-------|
| **Nano Banana** (not Pro) | **$0.04** | ~80% | Yes (native) | Google AI Studio | Already wired up. Best cheap option for iteration. |
| **FLUX.1 Schnell** | **$0.003** | ~70% | No (needs IP-Adapter) | Replicate / Together AI | Extremely cheap. Fast. Good for bulk UGC. |
| **FLUX.1 Dev** | **$0.01** | ~75% | No (needs IP-Adapter) | Replicate | Better quality than Schnell, still cheap. |
| **SDXL Lightning** | **$0.002** | ~60% | No (needs ControlNet) | Replicate | 4-step generation. Fastest and cheapest. Lower quality. |
| **SD 3.5 Large** | **$0.01** | ~70% | No (needs IP-Adapter) | Replicate | Good text rendering. Decent for product shots with text. |
| **Ideogram 2.0** | **$0.05** | ~85% | Yes (basic) | Ideogram API | Best text rendering of any model. Good for packaging accuracy. |
| **Recraft V3** | **$0.04** | ~80% | Yes (style reference) | Replicate | Strong photorealism. Good for editorial/lifestyle. |

### Videos

| Model | Cost/Unit | Quality vs Veo 3.1 | Image-to-Video | Audio | Provider | Notes |
|-------|-----------|---------------------|----------------|-------|----------|-------|
| **Kling 2.0** | **$0.10-0.15** | ~70% | Yes | No native | Various | Previous gen. Still decent for basic motion. |
| **Minimax Video** | **$0.10** | ~60% | Yes | No | Replicate | Cheap, short clips, decent quality. |
| **CogVideoX** | **$0.05-0.10** | ~55% | Yes | No | Replicate | Open source. Variable quality. Very cheap. |
| **LTX Video** | **$0.03-0.05** | ~50% | Yes | No | Replicate | Lightricks model. Fast and cheap. Lower quality. |
| **Wan 2.1** | **$0.08** | ~65% | Yes | No | Replicate | Alibaba model. Good motion, decent quality. |
| **Veo 2** | **Free tier** | ~65% | Limited | No | Google AI Studio | May still have free access. Lower quality than 3.1. |
| **Pika 2.0** | **$0.20** | ~70% | Yes | Sound effects | Pika API | Good lip sync. Native sound effects. Mid-tier price. |

---

## Batch Cost Projections

### 10-Ad Campaign (20 images + 20 videos)

| Tier | Image Model | Video Model | Image Cost | Video Cost | Total |
|------|-------------|-------------|------------|------------|-------|
| **Premium** | Nano Banana Pro ($0.13) | Veo 3.1 ($0.50) | $2.60 | $10.00 | **$12.60** |
| **Standard** | Nano Banana ($0.04) | Kling 3.0 ($0.30) | $0.80 | $6.00 | **$6.80** |
| **Budget** | FLUX.1 Schnell ($0.003) | Minimax ($0.10) | $0.06 | $2.00 | **$2.06** |
| **Ultra Budget** | FLUX.1 Schnell ($0.003) | LTX Video ($0.04) | $0.06 | $0.80 | **$0.86** |

### 50-Ad Campaign (100 images + 100 videos)

| Tier | Image Cost | Video Cost | Total |
|------|------------|------------|-------|
| **Premium** | $13.00 | $50.00 | **$63.00** |
| **Standard** | $4.00 | $30.00 | **$34.00** |
| **Budget** | $0.30 | $10.00 | **$10.30** |
| **Ultra Budget** | $0.30 | $4.00 | **$4.30** |

### 200-Ad Campaign at Scale (400 images + 400 videos)

| Tier | Image Cost | Video Cost | Total | Cost Per Ad |
|------|------------|------------|-------|-------------|
| **Premium** | $52.00 | $200.00 | **$252.00** | $1.26 |
| **Standard** | $16.00 | $120.00 | **$136.00** | $0.68 |
| **Budget** | $1.20 | $40.00 | **$41.20** | $0.21 |
| **Ultra Budget** | $1.20 | $16.00 | **$17.20** | $0.09 |

---

## Local Models (Free Per-Unit Cost)

### Hardware Requirements

| Machine | RAM | Image Gen | Video Gen | Verdict |
|---------|-----|-----------|-----------|---------|
| MacBook Air M1 (8GB) | 8GB | SDXL/FLUX quantized — slow but works | Barely viable — 15-20 min/video, low quality | Images only |
| MacBook Pro M2/M3 (16GB) | 16GB | FLUX.1 Dev full — good | CogVideoX/LTX — slow but usable | Both viable for small batches |
| MacBook Pro M3 Max (36-64GB) | 36-64GB | Everything runs well | Most models run — 3-8 min/video | Good for batch work |
| Desktop with RTX 4090 (24GB VRAM) | 24GB | Everything runs fast | Most models run fast — 1-3 min/video | Ideal local setup |

### Local Image Models

| Model | Min RAM | Quality | Speed (M1 8GB) | Speed (M3 16GB) | Reference Image Support |
|-------|---------|---------|-----------------|------------------|------------------------|
| **FLUX.1 Dev** | 12GB (8GB quantized) | Good | ~60-90s | ~20-30s | Via IP-Adapter (complex setup) |
| **FLUX.1 Schnell** | 12GB (8GB quantized) | Decent | ~30-45s | ~10-15s | Via IP-Adapter (complex setup) |
| **SDXL** | 8GB | Decent | ~20-40s | ~10-15s | Via IP-Adapter / ControlNet |
| **SD 3.5 Medium** | 8GB | Good | ~30-45s | ~15-20s | Via IP-Adapter |
| **Juggernaut XL** | 8GB | Very Good (photorealism) | ~25-40s | ~12-18s | Via IP-Adapter / ControlNet |

**Setup Options:**
- **Draw Things** (Mac App Store) — easiest, free, runs FLUX/SDXL locally with zero config
- **ComfyUI** — most flexible, node-based workflows, supports all models + IP-Adapter
- **Diffusers (Python)** — simplest code integration, pip install and go
- **Automatic1111 / Forge** — web UI, large community, many extensions

### Local Video Models

| Model | Min RAM | Quality | Speed (M1 8GB) | Speed (M3 16GB) | Image-to-Video |
|-------|---------|---------|-----------------|------------------|----------------|
| **LTX Video 0.9** | 12GB | Medium | ~8-15 min | ~3-5 min | Yes |
| **CogVideoX-5B** | 16GB+ | Decent | Not viable | ~5-10 min | Yes |
| **AnimateDiff** | 12GB | Medium | ~5-10 min | ~2-4 min | Yes (with adapter) |
| **Wan 2.1 (1.3B)** | 12GB | Decent | ~10-15 min | ~4-7 min | Yes |
| **Mochi 1** | 16GB+ | Decent | Not viable | ~8-12 min | Limited |

**Reality Check:**
- Local video gen on a MacBook Air M1 (8GB) is not practical for batch work
- Quality is noticeably lower than Veo 3.1 or Kling 3.0
- No native audio/dialogue generation — would need separate TTS pipeline
- Best use case: quick draft previews before spending on cloud generation

---

## Recommended Strategy by Use Case

### Iteration / Testing Prompts
```
Images: Nano Banana ($0.04) or local FLUX via Draw Things ($0)
Videos: Skip — test with images first, only generate video on approved images
```

### Standard DTC Campaign (10-20 ads)
```
Images: Nano Banana Pro ($0.13) — quality matters for start frames
Videos: Veo 3.1 ($0.50) for UGC with dialogue, Kling 3.0 ($0.30) for cinematic
Total: ~$6-13 per campaign
```

### Scale Production (50-200+ ads)
```
Images: Nano Banana ($0.04) for drafts → Nano Banana Pro ($0.13) for finals only
Videos: Mix models — Veo 3.1 for hero ads, Minimax ($0.10) for volume/testing
Total: $0.20-1.00 per ad depending on tier
```

### Maximum Budget Constraint
```
Images: FLUX.1 Schnell via Replicate ($0.003) or local Draw Things ($0)
Videos: LTX Video ($0.04) or Minimax ($0.10)
Total: Under $0.15 per ad
Tradeoff: No reference image support, lower quality, no dialogue in video
```

---

## Key Tradeoffs

| Feature | Premium Cloud | Budget Cloud | Local |
|---------|-------------|-------------|-------|
| Cost per image | $0.04-0.13 | $0.002-0.01 | $0 |
| Cost per video | $0.30-0.50 | $0.04-0.15 | $0 |
| Reference image support | Native | Requires IP-Adapter | Requires IP-Adapter |
| Product text accuracy | Very good | Variable | Variable |
| Video dialogue/audio | Native (Veo 3.1) | No | No |
| Speed (image) | 8-12s | 5-15s | 15-90s |
| Speed (video) | 45s-12min | 30s-5min | 3-20min |
| Batch processing | Excellent | Good | Slow |
| Quality ceiling | Highest | Medium-High | Medium |
| Offline capable | No | No | Yes |

---

## Adding New Providers to the Engine

The Creative Content Engine supports new providers via `tools/providers/`. To add a provider:

1. Create `tools/providers/newprovider.py` with `submit_image()`, `poll_image()`, `submit_video()`, `poll_video()` functions
2. Register in `tools/providers/__init__.py` under IMAGE_PROVIDERS / VIDEO_PROVIDERS
3. Set default or override: `generate_batch(records, provider="newprovider")`

**Candidates to wire up next:**
- **Replicate** — gives access to FLUX, SDXL, CogVideoX, LTX Video, Minimax, Wan 2.1 all through one API
- **Together AI** — cheapest FLUX inference ($0.003/image)
- **Ideogram** — best text rendering for product packaging
- **Pika** — mid-tier video with sound effects

Adding Replicate alone would unlock 10+ cheaper models through a single provider integration.
