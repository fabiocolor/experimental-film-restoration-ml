# Qwen Image Edit colour recovery

A ComfyUI workflow that rescues the colour of a single faded film frame. The scan keeps its own brightness and detail, and Qwen Image Edit only proposes the colour that faded away. It saves two images: the model's colour proposal and a final composite with that colour on the scan's own brightness. Compare both with the original.

This is research in progress, so the workflow and settings will change. Check the website for the latest version.

## What's in the package

- `workflows/faded-qwen-2511-still-composite-app.json`: the full workflow for your own computer. It uses the small helper node in `custom_nodes/`.
- `workflows/faded-qwen-2511-cloud-composite-app.json`: the same workflow using only built-in nodes, so it also runs on ComfyUI Cloud.
- `workflows/*.png`: the same two workflows as images. Drag one onto ComfyUI and the graph opens.
- `custom_nodes/faded_color_recovery/`: the helper node for the local workflow.
- `assets/demo_unbalanced_source_frame.jpg`: a faded frame to test with.
- `assets/faded-color-reference-palette.png`: the colour reference the workflow uses.
- `assets/Belak_Color_Patch_Chart_softblur_32.png`: the colour chart I used in the *Counter Attack* example.
- `examples/counter-attack-waterfront/`: the *Counter Attack* waterfront example from my talks, with its workflow (JSON and PNG) and its three inputs: source, reference chart and edge map.
- `THIRD_PARTY_NOTICES.md`: credits and licences for the models and software.

## Run it on your own computer

1. Install or update ComfyUI.
2. Download the four model files into these folders inside `ComfyUI/models/`:

| Folder | File | Link |
| --- | --- | --- |
| `diffusion_models/` | `qwen_image_edit_2511_bf16.safetensors` | https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_edit_2511_bf16.safetensors |
| `loras/` | `Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors` | https://huggingface.co/lightx2v/Qwen-Image-Edit-2511-Lightning/resolve/main/Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors |
| `text_encoders/` | `qwen_2.5_vl_7b_fp8_scaled.safetensors` | https://huggingface.co/Comfy-Org/HunyuanVideo_1.5_repackaged/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors |
| `vae/` | `qwen_image_vae.safetensors` | https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors |

3. Copy the `custom_nodes/faded_color_recovery` folder into `ComfyUI/custom_nodes/` and restart ComfyUI. You only need this for the still-composite workflow.
4. Copy `faded-color-reference-palette.png` and your faded frame into `ComfyUI/input/`.
5. Open a workflow by dragging its JSON or PNG onto ComfyUI.
6. Pick your frame in the `source frame` input and run it.
7. Save `Recovered color` and `Final composite`.

For the *Counter Attack* example, copy its three PNG inputs into `ComfyUI/input/` and open `counter-attack-waterfront-workflow.json`.

## ComfyUI Cloud

Tested on ComfyUI Cloud in October 2026: it loads with no missing nodes or models and runs on the free tier.

1. Sign in at https://cloud.comfy.org.
2. Drag in `faded-qwen-2511-cloud-composite-app.json` (or its PNG).
3. Upload your frame and `faded-color-reference-palette.png` to the two image inputs.
4. Run it.
5. Download `Recovered color` and `Final composite`.

## Review

Look for altered faces or objects, colour crossing edges, invented detail and odd overall casts. A good result on one frame doesn't mean a whole shot will stay consistent.

## Credits and rights

Read `THIRD_PARTY_NOTICES.md` before downloading the models or sharing the package. Credit doesn't give permission to reuse the film frames. The colour palette was made for this project and can be reused with the package.
