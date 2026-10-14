---
layout: default
title: "Download: faded colour recovery kit"
parent: "Colour Recovery"
nav_order: 90
permalink: /downloads/faded-colour-recovery-t185/
---

# Faded colour recovery for pre-balanced scans

This is the route I use now for faded film that has already been balanced (black is black, white is white, and the colour has collapsed). It works on one shot at a time, at reduced resolution (768 × 576 for the video model).

I checked every step here against a shot I approved, and each step's output matches mine to within a colour difference you can't see. The average difference (ΔE) was 0.61 for the palette still, 1.34 for the MiniMax H3 step, 1.20 for the adapter, and the respect step gave identical pixels.

## What you need

- ComfyUI, recent enough to have the MiniMax H3 nodes. Every node in these graphs is a built-in ComfyUI node; no custom nodes.
- Python 3.10+ with `opencv-python`, `numpy` and `pillow`, and `ffmpeg`/`ffprobe` on your path. The adapter step also needs PyTorch with an NVIDIA GPU.
- Models (put them in the usual ComfyUI folders). These are the exact files I used, all public:
  - Palette still:
    - [`qwen_image_edit_2511_fp8mixed.safetensors`](https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/blob/main/split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors) (diffusion_models)
    - [`qwen_2.5_vl_7b_fp8_scaled.safetensors`](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/blob/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors) (text_encoders)
    - [`qwen_image_vae.safetensors`](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/blob/main/split_files/vae/qwen_image_vae.safetensors) (vae)
    - [`Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors`](https://huggingface.co/lightx2v/Qwen-Image-Edit-2511-Lightning/blob/main/Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors) (loras)
  - Shot:
    - [`minimax_h3_ref2va_int8_convrot.safetensors`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/diffusion_models/minimax_h3_ref2va_int8_convrot.safetensors) (diffusion_models)
    - [`qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors) (text_encoders)
    - [`minimax_h3_video_vae_fp16.safetensors`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/vae/minimax_h3_video_vae_fp16.safetensors) (vae)
    - [`minimax_h3_audio_vae_fp32.safetensors`](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/vae/minimax_h3_audio_vae_fp32.safetensors) (vae)
    - [`MiniMax-H3-Fun-Controlnet-Union.safetensors`](https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/blob/main/MiniMax-H3-Fun-Controlnet-Union.safetensors) (model_patches). Use this original release, not 2.0 or a pruned copy.
  - The NVFP4 text encoder needs an NVIDIA Blackwell GPU (RTX 50-series or newer). On older cards, use the [int8_convrot](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/text_encoders/qwen3vl_32b_minimax_h3_int8_convrot.safetensors) or [bf16](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/main/text_encoders/qwen3vl_32b_minimax_h3_bf16.safetensors) encoder from the same repo. I haven't checked those against my result, so compare yours with the example before relying on it.

## The steps

1. **Prepare the shot.** `python tools/run_step.py prepare --update-hashes --source shot.mkv --out out/prepare`
   Makes the grey carrier video (`context.mp4`), the edge video (`control.mp4`) and the palette frame. Edit `tools/steps/prepare/prep_spec.json` first for your shot's length, the frame to use for the palette and the start of the 124 frames the video model sees.
2. **Palette still.** `python tools/prepare_still_inputs.py out/prepare/palette_frame.png still`, then load `graphs/1_palette_still_fp8mixed_local.json` in ComfyUI, point the three Load Image nodes at `source_y.png`, `faded_frame.png` and `canny.png`, and run. Then `python tools/composite_still.py still/faded_frame.png <graph output>.png palette.png`. Look at it: this one still sets the colour of the whole shot, so only go on with one you'd approve.
3. **The shot with MiniMax H3.** Load `graphs/2_h3_fun_controlnet_local.json`, give it `context.mp4`, `control.mp4` and `palette.png` (all three reference images), and run.
4. **Preview.** `python tools/run_step.py preview --update-hashes --source shot.mkv --carrier out/prepare/context.mp4 --h3 <H3 output>.mp4 --out out/preview`
   Lines H3 up with the film and keeps the frames that pass a brightness check as teachers.
5. **Temporal CbCr adapter.** `python tools/run_step.py adapter --update-hashes --source shot.mkv --targets out/preview/teacher_targets.npz --report out/preview/registration_report.json --out out/adapter`
   Learns the colour of this shot from the teachers and colours every frame. List your shot's teacher frames and their hashes (from the preview report) in `tools/steps/adapter/adapter_spec.json`.
6. **Respect the surviving colour.** `python tools/run_step.py respect --update-hashes --source shot.mkv --recovered out/adapter/full_recovered.mp4 --out out/respect`
   The red-green colour that survived in the scan can be strengthened but never flipped or weakened. `respect.mp4` is the result.

Every final frame keeps the scan's own brightness; only the colour is new. The yellow-blue choices are still an interpretation, because yellow is mostly the dye that's lost.

## Example

`example/` has the shot I checked the kit against: a 1970s Folgers coffee commercial, 135 frames at 1024 × 768.

The larger example files are hosted outside the repository. Download them into `example/` before you start:

- [`faded_frame.png`](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/download/examples-2026-10/faded_frame.png)
- [`result_respect.mp4`](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/download/examples-2026-10/result_respect.mp4)
- [`source_shot.mkv`](https://github.com/fabiocolor/custom-machine-learning-for-film-restoration/releases/download/examples-2026-10/source_shot.mkv)

- `source_shot.mkv`: the balanced scan.
- `source_y.png`, `faded_frame.png`, `canny.png`: the three inputs for the palette graph.
- `palette.png`: the palette still I approved.
- `result_respect.mp4`: the result I approved.

Run the steps on `source_shot.mkv` and compare your result with `result_respect.mp4`. Expect small differences, not identical files: the models don't give byte-identical output from run to run.

## Comfy Cloud (palette still only)

The palette still runs on Comfy Cloud with the same graph and the same model I used. I haven't run it there yet.

1. Import `qwen_image_edit_2511_fp8mixed.safetensors` from [Comfy-Org on Hugging Face](https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/blob/main/split_files/diffusion_models/qwen_image_edit_2511_fp8mixed.safetensors). Importing your own models needs a Creator plan or higher. If Cloud is missing the text encoder, the VAE or the Lightning LoRA listed above, import those the same way.
2. Open `graphs/1_palette_still_fp8mixed_local.json` in Cloud.
3. Upload `example/source_y.png`, `example/faded_frame.png` and `example/canny.png` into the three Load Image nodes, in that order, and run.
4. Put the colour on the frame's own brightness on your computer: `python tools/composite_still.py example/faded_frame.png <Cloud output>.png palette.png`, and compare with `example/palette.png`.

Don't swap in the bf16 model: I tried it, and the colour came out visibly different. The H3 step is for running locally.

## Licences

The code is mine, under the repository's licence. The models keep their own licences.
