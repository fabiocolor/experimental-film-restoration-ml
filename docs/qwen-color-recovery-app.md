---
layout: default
title: Qwen Image Edit Workflow
parent: Open-Weight Color Recovery
nav_order: 1
grand_parent: Colour Recovery
---


# Qwen Image Edit Colour Recovery Workflow

The aim is to rescue the colour of a faded frame, not to colorize it. The source keeps its own luminance, so fine detail, texture, damage and light stay as they were, and Qwen Image Edit only fills in the colour that faded away. This download is the single-frame route for scans with a strong cast. For pre-balanced scans, which is the usual case in a restoration, I now use a route that also keeps the red-green colour that survived in the scan; it isn't in this download yet (see [where the research stands]({{ '/research-status/' | relative_url }})).

The workflow runs in ComfyUI on your own computer. Try it on a test frame from your own footage before using preservation material.

> **Ongoing research:** this page and its downloads describe the current working version, not a final specification. Workflows, prompts, recommended settings, and conclusions will change as experiments continue. Review every result against the source and any historical evidence; a visually convincing image is not proof of original colour.

**Where this stands, October 2026.** This is the single-frame part of my research, shared as it is now, so expect it to change.

- **ComfyUI Cloud:** it runs there too, but I haven't tested it properly for restoration yet. Making the best workflows easy to use on ComfyUI Cloud is one of my next goals.
- **Hardware for a local install:** a modern NVIDIA GPU with 8 GB of VRAM or more for still frames. Video work needs 16 GB or more.
- **Settings:** as shipped, the "Enable 4steps LoRA?" switch is off, so the workflow runs Qwen's own defaults: 40 steps, CFG 4, with a random seed. The settings I use are the switch on (4 steps with the Lightning LoRA, CFG 1) and a fixed seed (0), with the source-derived edge map and the colour chart as guides.
- **The whole-shot routes** (TeleStyle, MiniMax H3 with the Fun ControlNet, and the Temporal CbCr adapter) aren't part of this download yet. A cleaner, self-contained ComfyUI version is in progress. See [where the research stands]({{ '/research-status/' | relative_url }}).

<div class="app-hero-strip" aria-label="Color recovery example">
  <figure>
    <img src="{{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/01_source_reptilicus_tlr_000025-40689881.jpg' | relative_url }}" alt="Faded frame from the Reptilicus trailer">
    <figcaption><strong>Source</strong><br>The faded frame given to the model.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/04_inference_frame_000000_seed_0_cfg_1.000_Belak-0c1f0329.png' | relative_url }}" alt="Qwen Image Edit colour proposal for the Reptilicus frame">
    <figcaption><strong>Colour proposal</strong><br>What Qwen Image Edit returns.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/05_final_composite_reptilicus_tlr_05_beach_woman_source-38de94d1.png' | relative_url }}" alt="Final composite: the proposed colour on the original brightness of the Reptilicus frame">
    <figcaption><strong>Final composite</strong><br>The proposed colour on the scan's own brightness and detail.</figcaption>
  </figure>
</div>

<p class="experiment-credit"><em>Reptilicus</em> (1961) trailer, from a 35mm trailer reel scan posted publicly on <a href="https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps">archive.org</a>. The trailer belongs to its rights holders; see <a href="{{ '/credits/' | relative_url }}">Credits &amp; Attribution</a>.</p>

<div class="app-download-panel">
  <a class="btn btn-primary" href="{{ '/downloads/qwen-color-recovery/workflows/faded-qwen-2511-still-composite-app.json' | relative_url }}">Download the workflow</a>
</div>

## Download options

| Download | What it is for |
| --- | --- |
| [`faded-qwen-color-recovery-app.zip`]({{ '/downloads/faded-qwen-color-recovery-app.zip' | relative_url }}) | Everything in one package: the workflows, a demo frame, the colour palette and the helper node. |
| [`faded-qwen-2511-cloud-composite-app.json`]({{ '/downloads/qwen-color-recovery/workflows/faded-qwen-2511-cloud-composite-app.json' | relative_url }}) | A version that uses only built-in nodes, for ComfyUI Cloud. |
| [`faded-qwen-2511-still-composite-app.json`]({{ '/downloads/qwen-color-recovery/workflows/faded-qwen-2511-still-composite-app.json' | relative_url }}) | The complete workflow for a local ComfyUI installation. |
| [`demo_unbalanced_source_frame.jpg`]({{ '/downloads/qwen-color-recovery/assets/demo_unbalanced_source_frame.jpg' | relative_url }}) | A faded frame from the *Candy Candy* 16mm print, for a quick test. |
| [`faded-color-reference-palette.png`]({{ '/downloads/qwen-color-recovery/assets/faded-color-reference-palette.png' | relative_url }}) | The colour reference the workflow uses. I made it for this project, and you can reuse it with the workflow. |
| [`faded_color_recovery/__init__.py`]({{ '/downloads/qwen-color-recovery/custom_nodes/faded_color_recovery/__init__.py' | relative_url }}) | The small helper node for the local workflow. It puts the recovered colour on the scan's own brightness. |
| [`THIRD_PARTY_NOTICES.md`]({{ '/downloads/qwen-color-recovery/THIRD_PARTY_NOTICES.md' | relative_url }}) | Model, software, and included-asset attribution. |

You can test with the demo frame, or with a frame from your own footage.

## Extract a frame from video

Use this tool when your source is a video. The file stays in your browser and is not uploaded by this page. Choose a frame, download it as an image, then use that image in ComfyUI.

<div class="frame-extractor" id="frame-extractor">
  <label class="frame-extractor-file">
    <span>Choose source video</span>
    <input id="frame-video-file" type="file" accept="video/*">
  </label>
  <video id="frame-video" controls playsinline muted></video>
  <div class="frame-controls">
    <button type="button" class="btn btn-outline" id="frame-step-back" disabled>Back</button>
    <input id="frame-scrub" type="range" min="0" max="0" value="0" step="0.001" disabled>
    <button type="button" class="btn btn-outline" id="frame-step-forward" disabled>Forward</button>
  </div>
  <div class="frame-actions">
    <span id="frame-time">No video selected</span>
    <button type="button" class="btn btn-primary" id="frame-capture" disabled>Download selected frame</button>
  </div>
  <canvas id="frame-canvas" hidden></canvas>
  <img id="frame-preview" alt="Selected frame preview" hidden>
</div>

If your browser cannot open the original video, make a temporary H.264 or HEVC copy and extract the frame from that.

## Run it on your own computer

1. Install or update ComfyUI.
2. Download the still workflow, the colour palette and the helper node from the table above.
3. Make a folder called `faded_color_recovery` inside `ComfyUI/custom_nodes/` and put `__init__.py` in it.
4. Restart ComfyUI.
5. Copy `faded-color-reference-palette.png` into `ComfyUI/input/`.
6. Import the workflow JSON.
7. If ComfyUI reports missing Qwen Image Edit 2511 files, use ComfyUI Manager or follow the paths shown in the missing-model message.

## Trying it on ComfyUI Cloud

It runs on ComfyUI Cloud too, but I haven't tested it properly for restoration yet, and Cloud may need an active plan and credits. Making the best workflows easy to use there is one of my next goals. If you'd like to try it now:

1. Import `faded-qwen-2511-cloud-composite-app.json`.
2. Upload your faded frame to the input labelled `source frame`.
3. If Cloud asks for the colour reference, upload `faded-color-reference-palette.png` from the table above.
4. Run it, and save `Final composite` (and `Recovered color` if you want to see the model's direct output).

## Review the result

The workflow creates two useful images: the direct colour proposal and the source-preserving composite. Compare both with the original at full resolution. Look especially for altered faces, shifted edges, invented objects, clipped highlights, colour bleeding, and changes in grain or damage.

For more examples, including matched references, visual atlases, tiled generation, sequence tests, and failure cases, visit the [SEAPAVAA 2026 companion]({{ '/seapavaa-2026-companion/' | relative_url }}).

Before redistributing the workflow or its examples, read [Credits & Attribution]({{ '/credits/' | relative_url }}) and the package's [Third-Party Notices]({{ '/downloads/qwen-color-recovery/THIRD_PARTY_NOTICES.md' | relative_url }}). Credit identifies a source; it does not grant permission to reuse third-party footage, models, or software.

<script>
(() => {
  const root = document.getElementById('frame-extractor');
  if (!root) return;

  const fileInput = root.querySelector('#frame-video-file');
  const video = root.querySelector('#frame-video');
  const scrub = root.querySelector('#frame-scrub');
  const back = root.querySelector('#frame-step-back');
  const forward = root.querySelector('#frame-step-forward');
  const capture = root.querySelector('#frame-capture');
  const canvas = root.querySelector('#frame-canvas');
  const preview = root.querySelector('#frame-preview');
  const timeLabel = root.querySelector('#frame-time');
  let objectUrl = null;
  let previewUrl = null;

  const setEnabled = (enabled) => {
    scrub.disabled = !enabled;
    back.disabled = !enabled;
    forward.disabled = !enabled;
    capture.disabled = !enabled;
  };

  const formatTime = (value) => {
    if (!Number.isFinite(value)) return '0:00.000';
    const minutes = Math.floor(value / 60);
    const seconds = value - minutes * 60;
    return `${minutes}:${seconds.toFixed(3).padStart(6, '0')}`;
  };

  const syncTime = () => {
    scrub.value = String(video.currentTime || 0);
    timeLabel.textContent = `${formatTime(video.currentTime || 0)} / ${formatTime(video.duration || 0)}`;
  };

  fileInput.addEventListener('change', () => {
    const file = fileInput.files && fileInput.files[0];
    if (!file) return;
    if (objectUrl) URL.revokeObjectURL(objectUrl);
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    previewUrl = null;
    objectUrl = URL.createObjectURL(file);
    video.src = objectUrl;
    preview.hidden = true;
    setEnabled(false);
    timeLabel.textContent = 'Loading video';
  });

  video.addEventListener('loadedmetadata', () => {
    scrub.max = String(video.duration || 0);
    scrub.value = '0';
    setEnabled(true);
    syncTime();
  });

  video.addEventListener('error', () => {
    setEnabled(false);
    timeLabel.textContent = 'This browser cannot open that video. Use an H.264 or HEVC proxy.';
  });

  video.addEventListener('timeupdate', syncTime);
  video.addEventListener('seeked', syncTime);

  scrub.addEventListener('input', () => {
    video.currentTime = Number(scrub.value);
  });

  const step = (direction) => {
    const frameStep = 1 / 24;
    const next = Math.min(Math.max((video.currentTime || 0) + direction * frameStep, 0), video.duration || 0);
    video.pause();
    video.currentTime = next;
  };

  back.addEventListener('click', () => step(-1));
  forward.addEventListener('click', () => step(1));

  capture.addEventListener('click', () => {
    if (!video.videoWidth || !video.videoHeight) return;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d', { alpha: false });
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob((blob) => {
      if (!blob) return;
      if (previewUrl) URL.revokeObjectURL(previewUrl);
      const url = URL.createObjectURL(blob);
      previewUrl = url;
      const link = document.createElement('a');
      link.href = url;
      link.download = `unbalanced_source_frame_${Math.round((video.currentTime || 0) * 1000)}ms.png`;
      link.click();
      preview.src = url;
      preview.hidden = false;
    }, 'image/png');
  });
})();
</script>

## Downloads

The images on this page, full size:

- [Faded frame from the Reptilicus trailer]({{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/01_source_reptilicus_tlr_000025-40689881.jpg' | relative_url }}) (JPG, 0.4 MB)
- [Qwen Image Edit colour proposal for the Reptilicus frame]({{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/04_inference_frame_000000_seed_0_cfg_1.000_Belak-0c1f0329.png' | relative_url }}) (PNG, 1.2 MB)
- [Final composite: the proposed colour on the original brightness of the Reptilicus frame]({{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/05_final_composite_reptilicus_tlr_05_beach_woman_source-38de94d1.png' | relative_url }}) (PNG, 3.1 MB)
