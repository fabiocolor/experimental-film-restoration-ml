---
layout: default
title: Qwen Image Edit Workflow
parent: Open-Weight Color Recovery
nav_order: 1
---

<p class="eyebrow">Downloadable experiment</p>

# Qwen Image Edit Colour Recovery Workflow

This ComfyUI workflow uses Qwen Image Edit to propose colour for a faded film frame. It then combines that colour with the original frame’s luminance so the source remains responsible for fine detail, texture, damage, and light.

You can run the workflow in ComfyUI Cloud or on a local ComfyUI installation. Start with the supplied example before using preservation material.

> **Ongoing research:** this page and its downloads describe the current working version, not a final specification. Workflows, prompts, recommended settings, and conclusions will change as experiments continue. Review every result against the source and any historical evidence; a visually convincing image is not proof of original colour.

**Status, October 2026.** This is the single-frame part of my research, shared as a research snapshot. It isn't a finished tool, and I haven't validated it for professional work.

- **ComfyUI Cloud:** the workflow can technically run there, but I haven't validated that route professionally.
- **Hardware for a local install:** a modern NVIDIA GPU with 8 GB of VRAM or more for still frames. Video work needs 16 GB or more.
- **Settings:** as shipped, the "Enable 4steps LoRA?" switch is off, so the workflow runs Qwen's own defaults: 40 steps, CFG 4, with a random seed. The settings I use are the switch on (4 steps with the Lightning LoRA, CFG 1) and a fixed seed (0), with the source-derived edge map and the colour chart as guides.
- **The whole-shot routes** (TeleStyle, MiniMax H3 with the Fun ControlNet, and the Temporal CbCr adapter) aren't part of this download yet. A cleaner, self-contained ComfyUI version is in progress. See [where the research stands]({{ '/research-status/' | relative_url }}).

<div class="app-hero-strip" aria-label="Color recovery example">
  <figure>
    <img src="{{ '/images_kebab/seapavaa2026/originals/candy_ending_frame_1619/01_source_frame.jpg' | relative_url }}" alt="Faded source frame">
    <figcaption><strong>Source</strong><br>Faded frame supplied to the model.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/seapavaa2026/originals/candy_ending_frame_1619/04_raw_inference.png' | relative_url }}" alt="Raw Qwen color inference">
    <figcaption><strong>Colour proposal</strong><br>Direct Qwen Image Edit output.</figcaption>
  </figure>
  <figure>
    <img src="{{ '/images_kebab/seapavaa2026/originals/candy_ending_frame_1619/05_final_composite.png' | relative_url }}" alt="Final color recovery composite">
    <figcaption><strong>Final composite</strong><br>Proposed colour with source luminance and detail.</figcaption>
  </figure>
</div>

<p class="experiment-credit"><em>Candy Candy</em> (1976), directed by Hiroshi Shidara. These frames illustrate the workflow; source and rights notes are recorded in <a href="{{ '/credits/' | relative_url }}">Credits &amp; Attribution</a>.</p>

<div class="app-download-panel">
  <a class="btn btn-primary" href="{{ '/downloads/faded-qwen-color-recovery-app.zip' | relative_url }}">Download the complete package</a>
  <a class="btn btn-outline" href="{{ '/downloads/qwen-color-recovery/workflows/faded-qwen-2511-cloud-composite-app.json' | relative_url }}">Download Cloud workflow</a>
  <a class="btn btn-outline" href="https://cloud.comfy.org/" target="_blank" rel="noopener">Open ComfyUI Cloud</a>
</div>

## Download options

| Download | What it is for |
| --- | --- |
| [`faded-qwen-color-recovery-app.zip`]({{ '/downloads/faded-qwen-color-recovery-app.zip' | relative_url }}) | The workflows, example frame, colour reference, and local helper node in one package. |
| [`faded-qwen-2511-cloud-composite-app.json`]({{ '/downloads/qwen-color-recovery/workflows/faded-qwen-2511-cloud-composite-app.json' | relative_url }}) | The simplest version to try in ComfyUI Cloud. |
| [`faded-qwen-2511-still-composite-app.json`]({{ '/downloads/qwen-color-recovery/workflows/faded-qwen-2511-still-composite-app.json' | relative_url }}) | The complete workflow for a local ComfyUI installation. |
| [`THIRD_PARTY_NOTICES.md`]({{ '/downloads/qwen-color-recovery/THIRD_PARTY_NOTICES.md' | relative_url }}) | Model, software, and included-asset attribution. A copy is also inside the complete package. |

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

## Run it in ComfyUI Cloud

ComfyUI Cloud may require an active plan and available credits before it can run the workflow. You can still open the graph and inspect how it works without starting a generation.

1. Open [ComfyUI Cloud](https://cloud.comfy.org/).
2. Import `faded-qwen-2511-cloud-composite-app.json`.
3. Upload your faded frame to the input labelled `source frame`.
4. If Cloud asks for the colour reference, upload `faded-color-reference-palette.png` from the app package.
5. Run the workflow.
6. Save `Recovered color` if you want to inspect the model’s direct proposal.
7. Save `Final composite` for the source-preserving version.

The hard Canny guide is created inside the workflow from the source frame. You do not need to make it separately.

## Run it on your own computer

1. Install or update ComfyUI.
2. Download and unzip the app package.
3. Copy `qwen-color-recovery/custom_nodes/faded_color_recovery` into `ComfyUI/custom_nodes/`.
4. Restart ComfyUI.
5. Copy `faded-color-reference-palette.png` into `ComfyUI/input/`.
6. Import either workflow JSON from `qwen-color-recovery/workflows/`.
7. If ComfyUI reports missing Qwen Image Edit 2511 files, use ComfyUI Manager or follow the paths shown in the missing-model message.

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
