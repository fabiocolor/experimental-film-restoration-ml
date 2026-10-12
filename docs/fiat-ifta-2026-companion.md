---
layout: default
title: FIAT/IFTA 2026 Companion
nav_order: 2
permalink: /fiat-ifta-2026-companion/
fc_lang: en
description: Full-size examples and notes from Fabio Bedoya's FIAT/IFTA 2026 talk, The Current Limits of AI in Film Restoration and How They May Be Surpassed.
---

{% include fiat-companion/style.html %}
{% assign vb = site.fc_view_base_override | default: site.data.fiat_evidence.view_base %}

<div class="fc" lang="en">

{% include fiat-companion/langswitch.html %}

<header class="fc-hero">
  <p class="fc-kicker">FIAT/IFTA World Conference · São Paulo 2026</p>
  <h1 id="the-current-limits-of-ai-in-film-restoration">The Current Limits of AI in Film Restoration and How They May Be Surpassed</h1>
  <p class="fc-byline">Fabio Bedoya<span>Head of Restoration, Filmfinity</span></p>
  <p class="fc-panel">Cinemateca Brasileira<span>8 October 2026</span></p>
  <div class="fc-buttons">
    <a class="fc-btn fc-btn-primary" href="https://github.com/fabiocolor/custom-machine-learning-for-film-restoration">The research on GitHub</a>
    <a class="fc-btn" href="#workflows">Workflows and guides</a>
  </div>
  <p>This page goes with my talk. It follows the slides in order, so you can find the full-size version of each example as it comes up, or come back to it later. For each experiment, I've written down what worked and where it still falls short.</p>
  <p>Since the talk, I've also written up <a href="{{ '/research-status/' | relative_url }}">where the research stands</a>: what works, what doesn't yet, and which workflows you can reproduce today.</p>
</header>

<p class="fc-tip">Tap a video to play it here. The player streams from Google Drive, so it may show a lower quality than the original, especially on a slow connection. The parts and evidence under each example open at full size in a viewer, where you can zoom in to see the detail. Most videos are side-by-side comparisons, so each half is smaller than the full file.</p>

<nav class="fc-toc" aria-labelledby="contents">
  <h2 id="contents">Follow the talk</h2>
  <ol>
    <li><a href="#copycat-to-open-weight"><span class="fc-n">2</span>From CopyCat to open-weight models</a></li>
    <li><a href="#masking-versus-recovery"><span class="fc-n">3</span>Masking versus recovery</a></li>
    <li><a href="#the-limits"><span class="fc-n">4</span>The limits<span class="fc-v">Stills</span></a></li>
    <li><a href="#reference-recovery"><span class="fc-n">5–6</span>Reference-based colour recovery</a></li>
    <li><a href="#synthetic-reference"><span class="fc-n">7</span>Creating a synthetic reference<span class="fc-v">Stills</span></a></li>
    <li><a href="#telestyle"><span class="fc-n">8–9</span>Keeping colour steady through a shot<span class="fc-v">Video</span></a></li>
    <li><a href="#h3-controlnet"><span class="fc-n">10–11</span>Making it faster</a></li>
    <li><a href="#temporal-cbcr"><span class="fc-n">12–13</span>The Temporal CbCr adapter<span class="fc-v">Video</span></a></li>
    <li><a href="#diffusion-upscaling"><span class="fc-n">14–15</span>Diffusion upscaling</a></li>
    <li><a href="#diffusion-reconstruction"><span class="fc-n">16–17</span>Diffusion reconstruction</a></li>
    <li><a href="#combining-sources"><span class="fc-n">18–19</span>Combining sources, then reconstructing</a></li>
    <li><a href="#dialogue-recovery"><span class="fc-n">20</span>Dialogue recovery</a></li>
    <li><a href="#inside-existing-tools"><span class="fc-n">21</span>AI inside the tools we already use<span class="fc-v">Video</span></a></li>
    <li><a href="#limits-now"><span class="fc-n">22</span>Where the limits are now</a></li>
    <li><a href="#thanks"><span class="fc-n">23</span>Thank you and credits</a></li>
  </ol>
</nav>

<section class="fc-section" id="copycat-to-open-weight">
  <p class="fc-slide">Slide 2</p>
  <h2 id="copycat-to-open-weight-title">From CopyCat to open-weight models</h2>
  <p>My research started with CopyCat, inside Nuke. The idea is to train a small model for each film from matching frames of two copies: the damaged scan, and a better copy of the same film that shows the result we want. That's what I presented last year in Rome, and it's still my baseline. But it needs that better copy to learn from, and it's a closed platform built for visual effects.</p>
  <p>Since then, open-weight models, the ones anyone can download and run, have become good enough for images, video and voice on a single workstation. People already use them to “restore” old photos and home movies, but almost always outside the archive. So my question is: how do we constrain them so they become useful for the work we actually need?</p>
</section>

<section class="fc-section" id="masking-versus-recovery">
  <p class="fc-slide">Slide 3</p>
  <h2 id="masking-versus-recovery-title">Masking versus recovery</h2>
  <p>Most restoration tools use spatial and temporal filters. They borrow picture from the same frame, or from the frames around it, and when there's nothing clean to copy, they interpolate. The slide shows Dry Clean in Phoenix on <em>Point Blank</em> (1967); the red marks are what it detected and removed.</p>
  <p>These tools can hide dust, scratches and flicker, and bridge two or three missing frames. But they can't bring back what is lost. If we're honest, digital restoration has always been about masking, not recovery.</p>
  <p>So AI in restoration isn't something completely new. What it gives us is a way to take on problems that weren't technically or financially possible before, working with the scan as it is. In many archives, especially in Latin America and Southeast Asia, that faded scan is the only thing left of a film.</p>
{% include fiat-companion/evidence.html key="slide03" %}
</section>

<section class="fc-section" id="the-limits">
  <p class="fc-slide">Slide 4</p>
  <h2 id="the-limits-title">The limits</h2>
  <p>As I see it, there are three main limits.</p>
  <ul class="fc-points">
    <li><strong>They weren't made for film.</strong> These models were built to create or edit born-digital images. They smooth away grain and fine detail, or invent new detail. The picture looks sharper, but it stops looking like film.</li>
    <li><strong>Resolution and length.</strong> In my tests, local video models worked at around 768 × 432 pixels and could only follow about ten seconds at a time. On the slide, Qwen Image Edit ran twice on a frame from <em>Reptilicus</em> (1961) with the same prompt: once on the whole frame (1184 × 880) and once on four tiles stitched together (2048 × 1556). Look at the lifeguard tower: the tiles keep more of the film's grain and detail, but the colour drifts between them and the seams show. Tiling helps, but it brings a new problem to solve.</li>
    <li><strong>Cost.</strong> Restoration takes a lot of iterations, and in the cloud every one costs money. That's why I work locally, but that still means hardware, time and electricity. There's no free compute, even if you own the computer.</li>
  </ul>

  <figure class="fc-media fc-still">
    <button type="button" class="fc-ev fc-ev-img" data-id="v-reptilicus-beach-tiled-vs-fu-f83c" data-kind="image" data-w="1732" data-h="770" data-title="Reptilicus beach frame: four tiles stitched together on the left, the whole frame in one pass on the right"><img src="{{ vb }}v-reptilicus-beach-tiled-vs-fu-f83c_preview.jpg" alt="Reptilicus beach frame: four tiles stitched together on the left, the whole frame in one pass on the right" loading="lazy" decoding="async"></button>
    <p class="fc-bar">Slide 4 · <em>Reptilicus</em> (1961): four tiles stitched together (left) and the whole frame in one pass (right)</p>
    <figcaption class="fc-body">
      <p class="fc-file">How it was made · open each part at full size</p>
      <ol class="fc-parts">
        <li><button type="button" class="fc-part fc-ev" data-id="v-01-source-reptilicus-tlr-000-f859" data-kind="image" data-w="2048" data-h="1556" data-title="Faded source">Faded source<span class="fc-dims">2048 × 1556</span></button><p>The faded frame at the scan's full size.</p></li>
        <li><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-fullframe-cl-cf78" data-kind="image" data-w="1184" data-h="880" data-title="Whole frame in one pass">Whole frame in one pass<span class="fc-dims">1184 × 880</span></button><p>Qwen Image Edit on the whole frame, with the Clara prompt from slide 7. The result comes back smaller than the scan.</p></li>
        <li><span class="fc-part-label">Four tiles from the source<span class="fc-dims">1328 × 800 each</span></span><span class="fc-part-set"><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-top-left-sou-fd20" data-kind="image" data-w="1328" data-h="800" data-title="top left">top left</button><button type="button" class="fc-part fc-ev" data-id="s04-01" data-kind="image" data-w="1328" data-h="800" data-title="top right">top right</button><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-bottom-left--3036" data-kind="image" data-w="1328" data-h="800" data-title="bottom left">bottom left</button><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-bottom-right-b547" data-kind="image" data-w="1328" data-h="800" data-title="bottom right">bottom right</button></span><p>The same frame cut into four overlapping tiles.</p></li>
        <li><span class="fc-part-label">Each tile after the model<span class="fc-dims">1328 × 800 each</span></span><span class="fc-part-set"><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-tile-top-lef-75eb" data-kind="image" data-w="1328" data-h="800" data-title="top left">top left</button><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-tile-top-rig-e731" data-kind="image" data-w="1328" data-h="800" data-title="top right">top right</button><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-tile-bottom--4bd3" data-kind="image" data-w="1328" data-h="800" data-title="bottom left">bottom left</button><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-tile-bottom--f8c1" data-kind="image" data-w="1328" data-h="800" data-title="bottom right">bottom right</button></span><p>Each tile went through the model on its own, with the same prompt.</p></li>
        <li><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-four-tile-ra-2024" data-kind="image" data-w="2048" data-h="1556" data-title="Four tiles stitched">Four tiles stitched<span class="fc-dims">2048 × 1556</span></button><p>The four results pasted back into one frame at the scan's size, without blending, so the seams stay visible.</p></li>
      </ol>
    </figcaption>
  </figure>
{% include fiat-companion/evidence.html key="slide04" %}
</section>

<section class="fc-section" id="reference-recovery">
  <p class="fc-slide">Slides 5–6</p>
  <h2 id="reference-recovery-title">Reference-based colour recovery</h2>
  <p>Let's start with what already works. A small model trains on matching pairs of frames: the faded source, and a reference that still carries the colour. That reference can be a telecine, a DVD, another print, or the original negative wherever the two overlap.</p>
  <p>The model only learns colour. Its output is combined with the luma, the brightness, of the original scan, so resolution, grain and detail stay as they were. The workflow is <a href="{{ '/chroma-recovery/' | relative_url }}">documented here</a>.</p>
  <div class="fc-missing"><p>The examples from slides 5 and 6 aren't shown on this page.</p></div>

</section>

<section class="fc-section" id="synthetic-reference">
  <p class="fc-slide">Slide 7</p>
  <h2 id="synthetic-reference-title">Creating a synthetic reference</h2>
  <p>So what happens when there's no reference? You create one: an approved colour frame for each shot. I call it a synthetic reference, and I make it with Qwen Image Edit, an open-weight image model from Alibaba.</p>
  <p>My first try was to guide it with a leader lady, the woman on the calibration frames at the start of a reel. It didn't work. These models don't understand meaning the way we do, so instead of taking only the colour, the model mixed the two images and the woman ended up in the shot. I call that semantic contamination.</p>
  <p>A plain colour chart worked better, once I softly blurred it. It guides the colour without giving the model anything else to copy.</p>

  <p>Then came the prompt, which is how you talk to the model. I ran a small contest, which I called America's Next Top Machine Learning Model: dozens of prompts and hundreds of test frames, over seven rounds on seven faded films. A prompt only survived a round if eight out of ten frames were acceptable. The winner, Clara, is the one I use most, but I use the others too, depending on the shot.</p>
  <p>From the synthetic reference I keep only the colour. The brightness still comes from the scan.</p>



  <div class="fc-missing"><p>The test frames from slide 7 aren't shown on this page. The colour chart is in the evidence below.</p></div>
{% include fiat-companion/evidence.html key="slide07" %}
</section>

<section class="fc-section" id="telestyle">
  <p class="fc-slide">Slides 8–9</p>
  <h2 id="telestyle-section-title">Keeping colour steady through a shot</h2>
  <p>Getting one convincing frame is no longer the hard part. If you just run the model 24 times a second, it doesn't work, because these models aren't deterministic: every run is a bit of a roulette. Each frame gets a slightly different interpretation, and the colour flickers.</p>
  <p>Slide 8 shows a dance scene from <em>Obsession</em> where every frame was recovered on its own. Watch the dress of the woman on the right, and the background. Each frame is a fair interpretation by itself, but together they don't agree. One good frame is a thumbnail. A restoration needs the whole shot to agree with itself. That's temporal consistency, and it was the biggest hurdle.</p>

{% include fiat-companion/evidence.html key="slide08" %}

  <figure class="fc-media">
      <div class="fc-missing"><p>The clip from the talk isn't shown on this page. What follows comes from the research records.</p></div>
    <figcaption class="fc-body">
      <p>TeleStyle, from TeleAI, is a LoRA: a small add-on for Qwen Image Edit, made to copy the style of one image onto another. I take one approved reference and copy its colour onto every frame of the shot.</p>
      <div class="fc-verdict">
        <div><strong>What worked</strong><p>The colour holds through the whole shot.</p></div>
        <div><strong>Limits</strong><p>It runs the model on every single frame, with one fixed seed for the whole shot. This 11-second shot took almost four hours. Fine as a test, but not something you can use on a feature film.</p></div>
      </div>
      <p class="fc-file">How it was made, from the research records</p>
      <ol class="fc-parts fc-steps">
        <li><span class="fc-part-label">TeleStyle on every frame</span><p>Each frame went through Qwen Image Edit with the TeleStyle LoRA on its own, with the faded frame and the approved reference as its two inputs, in 4 steps. All 338 frames were generated.</p></li>
        <li><span class="fc-part-label">Colour only</span><p>The TeleStyle colour, made at 1184 × 880, was put on top of the untouched 1920 × 1440 brightness of the scan.</p></li>
        <li><span class="fc-part-label">Time</span><p>The whole run took about 13,560 seconds, close to four hours: around 32 seconds a frame once the machine was warm.</p></li>
        <li><span class="fc-part-label">Comparison</span><p>After approval, the three panels were put side by side: original scan, approved reference and chroma recovery, at 30 frames per second.</p></li>
      </ol>
    </figcaption>
  </figure>
</section>

<section class="fc-section" id="h3-controlnet">
  <p class="fc-slide">Slides 10–11</p>
  <h2 id="h3-controlnet-section-title">Making it faster: H3 and ControlNet</h2>
  <p>I had colour that held together, but it took far too long. At the end of July, MiniMax released H3, a video model that is very good with reference images. In one pass, it carries the approved colour through a whole section of a shot.</p>
  <p>On its own, though, H3 drifts from the picture and loses the geometry. So I had to run it in short sections and make them all agree, which meant more processing and more time. Then in August, Alibaba PAI released a ControlNet for H3. A ControlNet is a way to steer what the model does; this one feeds it the edges of every frame, which helps keep the film's own geometry and movement.</p>
  <p>I keep only the colour and put it on top of the original brightness, so the grain, the roughness, even the dirt, stay. Left on their own, these models want to change everything and make it look plasticky.</p>

  <figure class="fc-media">
      <div class="fc-missing"><p>The clip from the talk isn't shown on this page. What follows comes from the research records.</p></div>
    <figcaption class="fc-body">
      <p>The colour comes from H3 with the ControlNet, and it's finished with the Temporal CbCr adapter, explained in the next section. I chose this shot because it's hard: a lot of movement, a crowd that keeps changing, and a fast pan in the middle.</p>
      <div class="fc-verdict">
        <div><strong>What worked</strong><p>The colour holds through all that movement, and the geometry stays the same as the original.</p></div>
        <div><strong>Limits</strong><p>Look closely and there's some tint in the shadows. My copy was 30 frames per second with a broken cadence, so getting clean frames out of it was hard, and the adapter needs properly aligned frames. I'm still working on this.</p></div>
      </div>
      <p class="fc-file">How it was made, from the research records</p>
      <ol class="fc-parts fc-steps">
        <li><span class="fc-part-label">Source and cadence</span><p>385 frames at 1920 × 1440 and 30 frames per second. 77 of them were near-duplicates from the broken cadence, so the 308 distinct frames were mapped to 24 frames per second, frame by frame.</p></li>
        <li><span class="fc-part-label">Approved palettes</span><p>Two approved colour references: the main outdoor palette, and one for an indoor close-up.</p></li>
        <li><span class="fc-part-label">Edges</span><p>An edge map (Canny) of every frame, made from the source after a small median filter and a local contrast step.</p></li>
        <li><span class="fc-part-label">H3 with the ControlNet</span><p>H3 ran with the ControlNet on 124-frame sections, at 768 × 576 and 24 frames per second.</p></li>
        <li><span class="fc-part-label">Teachers</span><p>Each H3 frame was registered to the source and kept only if its brightness lined up, within 1.5 pixels overall. After an audit for contamination, 278 frames were admitted as teachers.</p></li>
        <li><span class="fc-part-label">Adapter</span><p>The Temporal CbCr adapter learned from the teachers. The best epoch was chosen on held-out frames, then the adapter was fitted again on all of them.</p></li>
        <li><span class="fc-part-label">Final</span><p>The colour was run again at 640 × 480, upscaled with guidance and put on the original brightness at 1920 × 1440, for all 385 frames. Approved on 30 September. The tint that remains is in the shadowed folds of a yellow jacket, in the first frames.</p></li>
      </ol>
      <p class="fc-more fc-steps-note">The images for these steps are in private research folders and aren't on this page yet.</p>
    </figcaption>
  </figure>
</section>

<section class="fc-section" id="temporal-cbcr">
  <p class="fc-slide">Slides 12–13</p>
  <h2 id="temporal-cbcr-section-title">The Temporal CbCr adapter</h2>
  <p>This is the idea behind my CopyCat work, taken out of Nuke so the research can run on an open platform. CbCr are the two colour channels of a video picture, kept separate from its brightness.</p>
  <p>I run H3 or TeleStyle once or twice, depending on the length of the shot, and keep only the frames that pass review. I call them teachers. They don't have to cover the whole shot, as long as their geometry lines up with the picture.</p>
  <p>A small model, with fewer than a million parameters, learns the colour of the shot from the teachers in minutes. Then it fills in the frames that have no teacher and keeps the colour steady across the whole shot. On slide 12, the first and third frames have no teacher and the second and fourth do.</p>

  <figure class="fc-media">
{% include fiat-companion/video.html key="slide13" title="Unman, Wittering and Zigo: Temporal CbCr adapter" label="Play video: Unman, Wittering and Zigo, Temporal CbCr adapter (7 seconds)" %}
    <p class="fc-bar">Slide 13 · <em>Unman, Wittering and Zigo</em> (1971): Temporal CbCr adapter</p>
    <figcaption class="fc-body">
      <p>A choir scene, with the faded source on the left and the adapter's result on the right. For this shot, H3 didn't line up with the picture, so all the teachers came from TeleStyle. They covered 101 of the 164 frames, and the adapter filled the rest. Training itself took about a minute and a half (88.5 seconds).</p>
      <div class="fc-verdict">
        <div><strong>What worked</strong><p>It keeps everything in the original: the dirt, the roughness of the film. Even the stained glass behind the choir stays consistent through the whole pan.</p></div>
        <div><strong>Limits</strong><p>The adapter is only as good as its teachers, and it needs frames that line up properly. The colour is still an interpretation unless a surviving reference supports it.</p></div>
      </div>
{% include fiat-companion/files.html key="slide13" desc="1920 × 850 comparison · 7 s · 24 fps" %}
      <p class="fc-file">How it was made, from the research records</p>
      <ol class="fc-parts fc-steps">
        <li><span class="fc-part-label">Source</span><p>164 frames of the trailer, 2048 × 1556, at 24 frames per second.</p></li>
        <li><span class="fc-part-label">H3, tried first</span><p>H3 was run first on two overlapping sections. None of its frames lined up well enough with the source, so none were used.</p></li>
        <li><span class="fc-part-label">Palette</span><p>One approved frame set the palette: a Qwen Image Edit result laid on the source brightness.</p></li>
        <li><span class="fc-part-label">Teachers</span><p>TeleStyle made the teachers, each checked for alignment and palette. 101 frames passed: 82 in three runs used for training, and a separate run of 19 kept for validation. 63 frames had no teacher.</p></li>
        <li><span class="fc-part-label">Training</span><p>The adapter has 931,274 parameters. 60 epochs took 88.5 seconds of training on one RTX 5090. The best epoch was 56.</p></li>
        <li><span class="fc-part-label">Result</span><p>The adapter coloured all 164 frames, and its colour was laid on the untouched brightness of the source.</p></li>
      </ol>
      <p class="fc-more fc-steps-note">The images for these steps are in private research folders and aren't on this page yet.</p>
    </figcaption>
  </figure>
{% include fiat-companion/evidence.html key="slide13" %}
</section>

<section class="fc-section" id="diffusion-upscaling">
  <p class="fc-slide">Slides 14–15</p>
  <h2 id="diffusion-upscaling-section-title">Diffusion upscaling</h2>
  <p>So far, the model only adds colour and the scan keeps its own picture. But sometimes the surviving element doesn't carry enough information for a traditional restoration. Our tools borrow from the same frame or the frames around it, and when every frame is damaged, there's nothing left to borrow. Diffusion upscaling lets a video model rebuild the picture from what survives, following its structure and movement.</p>
  <p><em>El Tinterillo</em> survives only as a damaged 16mm print and a telecine that is cleaner, but soft, cropped and with the strange cadence of telecines from that time. I smoothed the 16mm with a median filter, then combined the two, with the telecine inside and the 16mm around it. That gives a rough outline to guide the geometry, but the filter also removes the fine detail. So, for how the picture should look, I made more synthetic references with ChatGPT Images. MiniMax H3, in reference mode, then uses those references, with the telecine clip for the movement, to generate each section of the shot.</p>

  <figure class="fc-media">
      <div class="fc-missing"><p>The clip from the talk isn't shown on this page. What follows comes from the research records.</p></div>
    <figcaption class="fc-body">
      <div class="fc-verdict">
        <div><strong>What worked</strong><p>The picture in this scan is beyond saving with traditional tools. H3 fills those gaps and rebuilds the picture, following the structure and movement of the original.</p></div>
        <div><strong>Limits</strong><p>The result is partly synthetic: the model invents fine detail the film no longer carries, and that has to be declared. The model worked at 768 × 432. There's still a jump in brightness on the first frame, and faces and fine detail remain weak.</p></div>
      </div>
      <p>Some people will call this heresy, and to a degree it is. I wouldn't call it proper film restoration myself. But with footage like this, I don't see another way, and we may need to open our minds to what restoration can be.</p>
      <p class="fc-file">How it was made, from the research records</p>
      <ol class="fc-parts fc-steps">
        <li><span class="fc-part-label">Sources</span><p>The 16mm scan, which the result is judged against, and the telecine, used for its motion. The shot is 624 frames at 24 frames per second.</p></li>
        <li><span class="fc-part-label">Hybrid</span><p>For each key frame, the 16mm scan was smoothed with a median filter and shrunk to make a soft base for the full frame. The telecine, registered and matched in tone, went inside it with a 48-pixel feather.</p></li>
        <li><span class="fc-part-label">Synthetic references</span><p>Seven stills were generated with ChatGPT Images, each from its own hybrid. Each was checked for drift inside the frame against a 3-pixel limit; the accepted ones measured 0.66 to 1.23 pixels.</p></li>
        <li><span class="fc-part-label">H3 in sections</span><p>H3 in reference mode generated the shot in four sections at 768 × 432 (frames 1 to 200, 201 to 340, 341 to 400 and 401 to 624), with three reference images each and the telecine clip as the motion input. 20 steps, seed 0.</p></li>
        <li><span class="fc-part-label">One section redone</span><p>The second section was made again with calibrated references, because the first version lagged behind the motion.</p></li>
        <li><span class="fc-part-label">Joining the sections</span><p>A tone bridge and a 12-frame dissolve joined the sections. The brightness jump on the first frame was left as it was.</p></li>
      </ol>
      <p class="fc-more fc-steps-note">The images for these steps are in private research folders and aren't on this page yet.</p>
    </figcaption>
  </figure>
</section>

<section class="fc-section" id="diffusion-reconstruction">
  <p class="fc-slide">Slides 16–17</p>
  <h2 id="diffusion-reconstruction-title">Diffusion reconstruction</h2>
  <p>Sometimes the picture isn't damaged, it's gone: frames missing from the only surviving element. This happens a lot with nitrate, when a decaying section was cut out so it wouldn't damage the rest of the reel.</p>
  <p>Tools like Phoenix, DIAMANT or DaVinci Resolve can bridge two or three missing frames with optical flow. Across a longer gap, the motion starts to feel wrong, because they can only interpolate what survives.</p>
  <p>In the talk, the example is a 15-frame gap in a camera negative where the sound still survives, so the gap has to be filled to keep picture and sound together. I tracked the actors from the last frame before the gap to the first frame after it, and carried that movement through the missing frames: those are the skeletons on slide 16. Then Alibaba's VACE video model generated the picture, guided by that movement, only inside the gap.</p>
  <div class="fc-limits"><p><strong>What worked, and the limits.</strong> The generated frames hold up well, and every original frame stays untouched. The resolution limit from slide 4 still applies, and what is generated has to be declared.</p></div>
  <div class="fc-missing" style="margin-top: 1rem"><p>The clip shown on slide 17 isn't included on this page.</p></div>
</section>

<section class="fc-section" id="combining-sources">
  <p class="fc-slide">Slides 18–19</p>
  <h2 id="combining-sources-section-title">Combining sources, then reconstructing</h2>
  <p>When several elements survive, each one is usually damaged in different places. In the talk I showed this on a silent film that survives as a nitrate print and a diacetate safety copy. Together they cover most of the film, but in some places the nitrate has decayed and the safety copy is missing those frames too.</p>
  <p>First, I bring the two elements together. They had different colour, warping and framing, so each frame of one is matched to the other by its features and warped into place. Then one tone correction, fitted on the cleanest matching frames, gives both the same look.</p>
  <p>After that, each frame comes from whichever element survives undamaged. A timeline of the shot works as a map of this: which element each frame comes from, and where neither survives. In those frames I mask only the damaged areas, and Wan VACE 14B, Alibaba's video model, reconstructs only those. The surviving picture stays original, because we don't want to replace a whole frame just because part of it is damaged.</p>
  <div class="fc-limits"><p><strong>What worked, and the limits.</strong> It holds together well, and everything that survives stays untouched. It was a working test at reduced resolution, not a native HD restoration.</p></div>
  <div class="fc-missing" style="margin-top: 1rem"><p>The example from the talk isn't shown on this page.</p></div>
</section>

<section class="fc-section" id="dialogue-recovery">
  <p class="fc-slide">Slide 20</p>
  <h2 id="dialogue-recovery-title">Dialogue recovery</h2>
  <p>The same idea applies to sound: a word that has been badly distorted can be rebuilt from the actor's own voice.</p>
  <p>I used Fish Audio S2 Pro, an open-weight speech model, running locally. It's given a few seconds of the same actor's clean dialogue from the film, about ten seconds in this case, and the exact words. It generates many takes of the whole line. Speech recognition and voice comparison help rank them, but listening decides. Then only the damaged part goes back in, about a third of a second here. Everything else is the original soundtrack.</p>
  <div class="fc-limits"><p><strong>Limits.</strong> The model's output was so clean that it didn't blend in, so I added some of the film's own background noise. A good ear may still hear it in the repaired word.</p></div>
  <div class="fc-missing" style="margin-top: 1rem"><p>The audio example from the talk isn't included on this page.</p></div>
</section>

<section class="fc-section" id="inside-existing-tools">
  <p class="fc-slide">Slide 21</p>
  <h2 id="inside-existing-tools-section-title">AI inside the tools we already use</h2>
  <p>AI can also work through the tools we already use. The companies that make them are building it in, for control and management as well as processing. DaVinci Resolve 21.1 lets AI assistants operate it directly, Premiere Pro has an AI Assistant that works inside the project, and Avid has shown agentic AI for Media Composer. Restoration tools can work the same way.</p>

  <figure class="fc-media">
{% include fiat-companion/video.html key="slide21" title="Point Blank: a model working inside Phoenix" label="Play video: Point Blank, a model working inside Phoenix (30 seconds)" %}
    <p class="fc-bar">Slide 21 · <em>Point Blank</em> (1967): a model working inside Phoenix</p>
    <figcaption class="fc-body">
      <p>One of my research tests. After Dry Clean runs in Phoenix, a model paints the protection masks directly in the project. The red shows what Dry Clean changed.</p>
      <div class="fc-limits"><p><strong>Limits.</strong> It's still at an early stage. This is a screen recording of the workflow, not a finished restoration.</p></div>
{% include fiat-companion/files.html key="slide21" desc="1920 × 1080 screen recording · 30 s · 24 fps · silent" %}
      <p class="fc-file">How it was made, from the research records</p>
      <ol class="fc-parts fc-steps">
        <li><span class="fc-part-label">Source</span><p>A teaching copy of the Point Blank trailer project in Phoenix: a 52-frame shot, 2048 × 1556, at 24 frames per second.</p></li>
        <li><span class="fc-part-label">Two renders</span><p>The shot was exported twice from Phoenix: once without Dry Clean and once with it.</p></li>
        <li><span class="fc-part-label">What Dry Clean changed</span><p>The difference between the two renders shows what Dry Clean changed. Changes larger than 8 code values were grouped into separate marks.</p></li>
        <li><span class="fc-part-label">The model</span><p>A small image classifier (ResNet18), trained on brush strokes from another film, looked at each mark with the frames before and after it and predicted whether to bring the original picture back there.</p></li>
        <li><span class="fc-part-label">Into the project</span><p>Its choices became Matte Paint brush strokes: 630 over the 52 frames, written into the Phoenix project and read back to check them.</p></li>
        <li><span class="fc-part-label">Review</span><p>The recording is Phoenix playing the result with Red Difference on. In review, it also brought back wall areas where no meaningful information was lost, so it isn't accepted yet.</p></li>
      </ol>
      <p class="fc-more fc-steps-note">The images for these steps are in private research folders and aren't on this page yet.</p>
    </figcaption>
  </figure>
{% include fiat-companion/evidence.html key="slide21" %}
</section>

<section class="fc-section" id="limits-now">
  <p class="fc-slide">Slide 22</p>
  <h2 id="limits-now-title">Where the limits are now</h2>
  <ul class="fc-points">
    <li>What has worked best is keeping the film's own picture and letting the model add only what is missing: the colour, a gap, a word.</li>
    <li>Colour holds through a shot when approved references guide the whole shot, either through a video model or through the small adapter.</li>
    <li>Control helps the most. Edges, tracked movement and registration keep the model on the film, not on its own idea of it.</li>
    <li>In the colour workflow, a small model learns from approved teacher frames and fills in the shot, so the big model doesn't have to run on every frame.</li>
    <li>What still needs to improve is resolution and length. The models still see a reduced picture, about ten seconds at a time.</li>
    <li>None of it is one click. It takes patience, and a restorer to decide what is acceptable and to say what was generated.</li>
  </ul>
  <p>A year ago, even a couple of months ago, none of this was possible.</p>
</section>

<section class="fc-section" id="workflows">
  <h2 id="workflows-title">Workflows and guides</h2>
  <ul class="fc-points">
    <li><a href="{{ '/chroma-recovery/' | relative_url }}">Reference-trained colour recovery</a>: learn from matched source and reference frames, then combine the predicted colour with the brightness of the scan.</li>
    <li><a href="{{ '/open-weight-color-recovery/' | relative_url }}">Open-weight colour recovery</a>: create and review colour proposals while the scan stays the authority.</li>
    <li><a href="{{ '/training-inference-review/' | relative_url }}">Training, inference and review</a>: preparing material, iterating, and deciding when a result is acceptable.</li>
    <li><a href="{{ '/open-weight-color-recovery/research-routes/' | relative_url }}">Research routes and open questions</a>: an earlier snapshot of the research, with its evidence and limits.</li>
    <li><a href="{{ '/research-status/' | relative_url }}">Where the research stands (October 2026)</a>: what works, what doesn't yet, and what you can reproduce. The Nuke template runs locally in Nuke Non-Commercial or Indie with your own footage, and the Qwen Image Edit workflows run in ComfyUI. Both still need some work before they're easy to use.</li>
    <li><a href="{{ '/' | relative_url }}">All research on this site</a>, or the <a href="https://github.com/fabiocolor/custom-machine-learning-for-film-restoration">repository on GitHub</a>.</li>
  </ul>
</section>

<section class="fc-thanks" id="thanks">
  <p class="fc-slide fc-slide-light">Slide 23</p>
  <h2 id="thanks-title">Thank you</h2>
  <p>Thank you to FIAT/IFTA and the organisers.</p>
  <p class="fc-small">The examples on this page are research tests on faded trailers from a 35mm trailer reel scan that was posted publicly on <a href="https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps">archive.org</a>. Film excerpts remain the property of their rights holders, and showing them here doesn't grant permission to reuse them. See <a href="{{ '/credits/' | relative_url }}">credits and attribution</a>.</p>
  <p>Questions or suggestions are welcome:</p>
  <ul>
    <li>Email: <a href="mailto:info@fabiocolor.com">info@fabiocolor.com</a></li>
    <li>LinkedIn: <a href="https://www.linkedin.com/in/fabiobedoya/">/fabiobedoya</a> · Instagram: <a href="https://www.instagram.com/fabiocolor/">@fabiocolor</a></li>
    <li>YouTube: <a href="https://www.youtube.com/@fabiocolor">@fabiocolor</a> · GitHub: <a href="https://github.com/fabiocolor">/fabiocolor</a></li>
  </ul>
</section>

</div>

{% include fiat-companion/script.html %}
