---
layout: default
title: "Download: Single-Frame Kit"
parent: "Faded Colour Recovery"
nav_order: 0
permalink: /downloads/colour-recovery-single-frame/
---

<span class="kicker">Download kit · ComfyUI, local or Comfy Cloud</span>

# Faded colour recovery for a single frame

One faded frame in, one colour frame out, with the frame's own brightness kept. This is the first step of every shot on the [faded colour recovery]({{ '/colour-recovery/' | relative_url }}) page: the frame that, once it passes review, guides the rest of the shot.

The graph is the "Clara" recipe from the SEAPAVAA 2026 prompt study, on an unbalanced scan: Qwen Image Edit 2511, the Lightning 4-step LoRA, cfg 0.9, seed 0, an edge map of the frame as control and a softly blurred colour chart as the only colour guide. Every node is a built-in ComfyUI node; there are no custom nodes and no Python to run. The composite (colour on the source's brightness, with a shadow gate) is made inside the graph.

<div class="stage-strip" aria-label="Counter Attack waterfront test frame: source, model output, composite">
  <figure>
    <img src="{{ '/images_kebab/examples/counter-attack-waterfront-f007-source.jpg' | relative_url }}" alt="The test frame: Counter Attack, waterfront, faded to magenta-red" loading="lazy">
    <figcaption><strong>Source</strong><code>source.png</code>, 1920 × 1440.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/examples/counter-attack-waterfront-f007-model.jpg' | relative_url }}" alt="The published model output for the test frame, 1184 × 880" loading="lazy">
    <figcaption><strong>Model output</strong>The published still, 1184 × 880. Your run should come close to this.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/examples/counter-attack-waterfront-f007-result.jpg' | relative_url }}" alt="The composite: the model's colour on the scan's own brightness" loading="lazy">
    <figcaption><strong>Composite</strong>Its colour on the scan's brightness, at 1920 × 1440.</figcaption>
  </figure>
</div>

<p class="experiment-credit"><em>Counter Attack</em> (1976), waterfront, frame 000007 of the shot's frame dump. The published still is the one the whole-shot route on the colour recovery page started from. <a href="{{ '/records/counter-attack-waterfront/' | relative_url }}">Record</a>.</p>

## Files

<ul class="downloads">
  <li><a href="{{ '/downloads/colour-recovery-single-frame/graphs/colour-recovery-single-frame-fp8mixed.json' | relative_url }}">colour-recovery-single-frame-fp8mixed.json</a><span class="size">graph · 37 KB</span><span class="what">The published recipe, with the fp8mixed model. For a local ComfyUI, or Comfy Cloud with the model imported (Creator plan or higher).</span></li>
  <li><a href="{{ '/downloads/colour-recovery-single-frame/graphs/colour-recovery-single-frame-bf16-cloud.json' | relative_url }}">colour-recovery-single-frame-bf16-cloud.json</a><span class="size">graph · 37 KB</span><span class="what">The same graph with the bf16 model, which is in Comfy Cloud's own library, so it runs without importing anything. Its colour differs slightly from the published still (see below).</span></li>
  <li><a href="{{ '/images_kebab/seapavaa2026/originals/fanji_waterfront_workflow/01_source.png' | relative_url }}">source.png</a><span class="size">PNG · 1920 × 1440 · 2.9 MB</span><span class="what">The test frame. Upload it to <em>1 · Source frame</em>.</span></li>
  <li><a href="{{ '/downloads/colour-recovery-single-frame/example/chart.png' | relative_url }}">chart.png</a><span class="size">PNG · 333 × 238 · 45 KB</span><span class="what">The softly blurred colour chart. Upload it to <em>2 · Colour chart</em>. Keep using it for your own frames.</span></li>
  <li><a href="{{ '/downloads/colour-recovery-single-frame/example/control.png' | relative_url }}">control.png</a><span class="size">PNG · 1920 × 1440 · 18 KB</span><span class="what">The edge map of the test frame (OpenCV Canny 80/160). Upload it to <em>3 · Edge map</em>.</span></li>
  <li><a href="{{ '/images_kebab/seapavaa2026/originals/fanji_waterfront_top3/04_clara_anchor.png' | relative_url }}">model_output.png</a><span class="size">PNG · 1184 × 880 · 1.1 MB</span><span class="what">The published still, to compare your model output with.</span></li>
  <li><a href="{{ '/downloads/colour-recovery-single-frame/graphs/colour-recovery-single-frame-fp8mixed_api.json' | relative_url }}">…_api.json</a><span class="size">API format · 8 KB</span><span class="what">The same graphs as API-format prompts, for scripting ComfyUI directly. One per model variant.</span></li>
</ul>

## Models

All public, from the ComfyUI repackaging on Hugging Face. Put them in the usual ComfyUI folders.

| File | Folder | Size |
| --- | --- | --- |
| [`qwen_image_edit_2511_fp8mixed.safetensors`](https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/blob/main/split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors) (published recipe) or `qwen_image_edit_2511_bf16.safetensors` (Cloud library) | `diffusion_models` | 20.5 GB / 40.9 GB |
| [`qwen_2.5_vl_7b_fp8_scaled.safetensors`](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/blob/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors) | `text_encoders` | 9.4 GB |
| [`qwen_image_vae.safetensors`](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/blob/main/split_files/vae/qwen_image_vae.safetensors) | `vae` | 254 MB |
| [`Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors`](https://huggingface.co/lightx2v/Qwen-Image-Edit-2511-Lightning/blob/main/Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors) | `loras` | 850 MB |

## Run it in Comfy Cloud

1. Open [Comfy Cloud](https://cloud.comfy.org/) and import `colour-recovery-single-frame-bf16-cloud.json` (Workflow → Open). The text encoder, the VAE and the Lightning LoRA are in Cloud's library; the bf16 model is too.
2. Upload `source.png`, `chart.png` and `control.png` into the three *Load Image* nodes on the left, in that order.
3. Run. Two images are saved: `model_output` (the raw proposal, 1184 × 880) and `composite` (the colour on the source's brightness, 1920 × 1440).
4. To reproduce the published still exactly, import `qwen_image_edit_2511_fp8mixed.safetensors` from Hugging Face into your Cloud library (Creator plan or higher) and open the fp8mixed graph instead.

Comfy Cloud may need an active plan and credits to run; the graph can be opened and read without running it.

## Run it on your own computer

1. Install or update ComfyUI (the graph needs the Qwen Image Edit Plus and the MiniMax-era image nodes, all built in since autumn 2026).
2. Download the four model files above into your ComfyUI model folders.
3. Open `colour-recovery-single-frame-fp8mixed.json`, point the three *Load Image* nodes at `source.png`, `chart.png` and `control.png`, and run.

An NVIDIA GPU with 8 GB of VRAM or more runs the fp8mixed model, with ComfyUI keeping the rest in system RAM (32 GB of RAM or more makes that painless; 16 GB or more of VRAM keeps the model on the card). On a Mac with Apple Silicon the bf16 model runs and the fp8 one does not; the 41 GB file needs a machine with 64 GB of unified memory. A frame takes under a minute on a recent card at 4 steps.

## Your own frames

Upload your frame as the source. Keep the chart. For the edge map, either make one with OpenCV (`cv2.Canny(grey, 80, 160)`) and upload it, or use the *Detect edges* node already in the graph: drag its output into *Scale edge map* in place of the uploaded edge map. ComfyUI's edge detector is close to OpenCV's but not identical, so results differ a little from this test; for your own frames that does not matter.

Frames from the model are an interpretation. Compare the composite with the source at full size: altered faces, invented objects, colour crossing an edge, clipped highlights and changes in grain are the usual failures. Nothing in the frame proves what the original colour was.

## What is reproduced, and how closely

| Check | Result |
| --- | --- |
| The graph's sampler, models and settings against the research graph that made the published still | Identical node for node (switch nodes for the optional 40-step path removed; the Lightning path is fixed). |
| The fp8mixed recipe, core nodes only, run again against the published still | Mean ΔE76 1.89 to the published still, 95th percentile 4.13. Above the 1.5 bar used for the other kits, visually very close; the model is not deterministic across machines. |
| The bf16 model (Cloud library) | Not measured on this frame. On the balanced-source palette still it differed from the published result by a mean ΔE of 2.67, a visible difference on some surfaces. Use it to try the route, not to reproduce the still. |
| The in-graph composite against the kit's reference composite (`composite_still.py` in the balanced-source kit) | Mean ΔE76 1.39, 95th percentile 3.1. The in-graph version scales plainly instead of inverting the Kontext crop and uses a linear instead of a smoothstep shadow gate. |

## Provenance in the graph

The graph is a complete record of a run: model file names, LoRA, prompt, seed, steps, cfg, sampler, scheduler, shift and the three input images. ComfyUI embeds the whole graph in every saved PNG, so each output carries its own settings. For a controlled study, keep the seed fixed, change one widget at a time, and keep the model file hashes (shown on each Hugging Face page) with your notes. See [Provenance & Metadata]({{ '/provenance-metadata/' | relative_url }}).

## Licences

The graphs and example files on this page may be used freely with attribution. The models keep their own licences (Apache-2.0 for Qwen Image Edit and the Lightning LoRA). The test frame is from a film copy of *Counter Attack* (1976) used for research; it belongs to its rights holders and is shown here as a workflow demonstration.
