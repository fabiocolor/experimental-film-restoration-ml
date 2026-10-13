# Faded colour recovery for pre-balanced scans

This is the route I use now for faded film that has already been balanced (black is black, white is white, and the colour has collapsed). It works on one shot at a time, at reduced resolution (768 × 576 for the video model).

I checked every step here against a shot I approved, and each step's output matches mine to within a colour difference you can't see. The average difference (ΔE) was 0.61 for the palette still, 1.34 for the MiniMax H3 step, 1.20 for the adapter, and the respect step gave identical pixels.

## What you need

- ComfyUI, recent enough to have the MiniMax H3 nodes. Every node in these graphs is a built-in ComfyUI node; no custom nodes.
- Python 3.10+ with `opencv-python`, `numpy` and `pillow`, and `ffmpeg`/`ffprobe` on your path. The adapter step also needs PyTorch with an NVIDIA GPU.
- Models (put them in the usual ComfyUI folders):
  - Palette still: `qwen_image_edit_2511_fp8mixed.safetensors`, `qwen_2.5_vl_7b_fp8_scaled.safetensors`, `qwen_image_vae.safetensors`, `Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors`.
  - Shot: `minimax_h3_ref2va_int8_convrot.safetensors`, `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`, `minimax_h3_video_vae_fp16.safetensors`, `minimax_h3_audio_vae_fp32.safetensors`, and `MiniMax-H3-Fun-Controlnet-Union.safetensors` from alibaba-pai.

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

## Comfy Cloud

The palette still needs the same fp8mixed model I used. I tried the bf16 model as a Cloud stand-in and the colour came out visibly different, so I don't offer it. On Comfy Cloud, import `qwen_image_edit_2511_fp8mixed.safetensors` from [Comfy-Org on Hugging Face](https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI) (importing your own models needs a Creator plan or higher) and use `1_palette_still_fp8mixed_local.json`. I haven't run it on Cloud yet. The H3 graph is for running locally.

## Licences

The code is mine, under the repository's licence. The models keep their own licences.
