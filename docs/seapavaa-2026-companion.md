---
layout: default
title: SEAPAVAA 2026 Companion
parent: Open-Weight Color Recovery
nav_order: 3
---

<style>
.seapavaa-jump {
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
  margin: 1rem 0 1.8rem;
}
.seapavaa-jump a {
  display: inline-block;
  padding: 0.4rem 0.7rem;
  border-radius: 999px;
  border: 1px solid rgba(148, 163, 184, 0.35);
  text-decoration: none;
}
.seapavaa-slide {
  margin: 2.2rem 0 2.7rem;
  padding-top: 0.2rem;
}
.seapavaa-slide h2 {
  margin-bottom: 0.55rem;
}
.seapavaa-slide-intro {
  margin-bottom: 1rem;
}
.seapavaa-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1rem;
  margin: 1rem 0 0;
}
.seapavaa-card {
  border: 1px solid rgba(148, 163, 184, 0.35);
  border-radius: 0.9rem;
  padding: 0.85rem;
  background: rgba(255, 255, 255, 0.04);
}
.seapavaa-card h3 {
  margin-top: 0;
  margin-bottom: 0.35rem;
}
.seapavaa-role {
  display: inline-block;
  margin-bottom: 0.7rem;
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.01em;
  background: rgba(59, 130, 246, 0.12);
  color: #93c5fd;
}
.seapavaa-card p {
  margin-bottom: 0.65rem;
}
.seapavaa-card img,
.seapavaa-card video {
  width: 100%;
  height: auto;
  border-radius: 0.5rem;
  margin-bottom: 0.75rem;
}
.seapavaa-files {
  margin-top: 0.6rem;
  padding-top: 0.65rem;
  border-top: 1px solid rgba(148, 163, 184, 0.2);
  font-size: 0.94rem;
}
.seapavaa-files summary {
  cursor: pointer;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.seapavaa-filelist {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 0.8rem;
}
</style>

# SEAPAVAA 2026 Companion

This page follows my SEAPAVAA 2026 presentation (June 2026) by slide title. Each section shows the image or clip from the talk. Where it helps, I've also added the prompt or workflow behind it.

Some of the examples from the talk aren't shown here, because I'm still checking whether that footage can be shared. The research has also moved on since June: see [where the research stands now]({{ '/research-status/' | relative_url }}) and the [FIAT/IFTA 2026 companion]({{ '/fiat-ifta-2026-companion/' | relative_url }}).

## Jump by Title

<div class="seapavaa-jump">
  <a href="#slide-1">Advancing Open-Weight AI Models for Color Recovery in Faded Film</a>
  <a href="#slide-2">Presentation Companion</a>
  <a href="#slide-3">From CopyCat to Open-Weight Chroma Recovery</a>
  <a href="#slide-4">Correction Versus Recovery</a>
  <a href="#slide-5">Why Open-Weight Models, and How I Tested Them</a>
  <a href="#slide-6">Two Source Paths, Two Different Problems</a>
  <a href="#slide-7">The Reference Problem</a>
  <a href="#slide-8">The Semantic Boundary</a>
  <a href="#slide-9">The Product Contract</a>
  <a href="#slide-10">The Still Route Finally Generalized</a>
  <a href="#slide-11">First temporal success: Interior Woman</a>
  <a href="#slide-12">Temporal Success 2: Shot0006 Wan/VACE</a>
  <a href="#slide-13">What Still Fails: Hard Motion</a>
  <a href="#slide-14">Balanced Route: Context Boards</a>
  <a href="#slide-15">Atlas: Useful, But Not Yet Reliable</a>
  <a href="#slide-16">Tiling and the Spatial-Context Hypothesis</a>
  <a href="#slide-17">What We Can Claim Now</a>
  <a href="#slide-18">Thank you!</a>
</div>

<section id="slide-1" class="seapavaa-slide">
  <h2>Advancing Open-Weight AI Models for Color Recovery in Faded Film</h2>
  <p class="seapavaa-slide-intro">The example from this slide isn't shown on this page.</p>
</section>

<section id="slide-2" class="seapavaa-slide">
  <h2>Presentation Companion</h2>
  <p class="seapavaa-slide-intro">This is the companion-page call shown before the case-study sequence begins.</p>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>SEAPAVAA 2026 companion</h3>
      <a href="{{ '/seapavaa-2026-companion/' | relative_url }}" target="_blank">
        <img src="{{ '/images_kebab/seapavaa2026/custom_machine_learning_for_film_restoration_qr.png' | relative_url }}" alt="QR code for the SEAPAVAA 2026 companion page">
      </a>
      <p>The QR/link slide sends viewers to this companion page so the examples can be opened during or after the talk.</p>
      <details class="seapavaa-files">
        <summary>Open the companion link</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/seapavaa-2026-companion/' | relative_url }}" target="_blank">Companion page</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-3" class="seapavaa-slide">
  <h2>From CopyCat to Open-Weight Chroma Recovery</h2>
  <p class="seapavaa-slide-intro">The example from this slide isn't shown on this page.</p>
</section>

<section id="slide-4" class="seapavaa-slide">
  <h2>Correction Versus Recovery</h2>
  <p class="seapavaa-slide-intro">This is the exact still comparison used to define the boundary between correction and recovery.</p>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Reptilicus full-frame recovery pair</h3>
      <img src="{{ '/images_kebab/seapavaa2026/recovery_pair_reptilicus_beach_fullframe.png' | relative_url }}" alt="Reptilicus recovery pair">
      <p>A full-frame comparison between a faded source and an accepted composite, separating image correction from generated chroma recovery.</p>
    </div>
  </div>
</section>

<section id="slide-5" class="seapavaa-slide">
  <h2>Why Open-Weight Models, and How I Tested Them</h2>
  <p class="seapavaa-slide-intro">The example from this slide isn't shown on this page.</p>
</section>

<section id="slide-6" class="seapavaa-slide">
  <h2>Two Source Paths, Two Different Problems</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Balanced versus unbalanced path comparison</h3>
      <img src="{{ '/images_kebab/seapavaa2026/interior_woman_balanced_vs_unbalanced_paths_2x2.png' | relative_url }}" alt="Balanced versus unbalanced comparison">
      <p>The same subject behaves differently depending on whether the source is used raw or manually balanced before inference.</p>
    </div>
  </div>
</section>

<section id="slide-7" class="seapavaa-slide">
  <h2>The Reference Problem</h2>
  <p class="seapavaa-slide-intro">The example from this slide isn't shown on this page.</p>
</section>

<section id="slide-8" class="seapavaa-slide">
  <h2>The Semantic Boundary</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Source versus bad semantic inference</h3>
      <img src="{{ '/images_kebab/seapavaa2026/ben_row2_source_vs_bad_semantic_inference.png' | relative_url }}" alt="Source versus bad semantic inference">
      <p>A semantic failure case where the model produces a plausible image but misses what the original frame is actually showing.</p>
    </div>
  </div>
</section>

<section id="slide-9" class="seapavaa-slide">
  <h2>The Product Contract</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Full lineage board</h3>
      <img src="{{ '/images_kebab/seapavaa2026/jug_auditorium_full_lineage_5stage.png' | relative_url }}" alt="Full lineage board">
      <p>The lineage board makes the contract explicit: source, control, reference, raw inference, and final composite are separate things.</p>
    </div>
  </div>
</section>

<section id="slide-10" class="seapavaa-slide">
  <h2>The Still Route Finally Generalized</h2>
  <p class="seapavaa-slide-intro">The example from this slide isn't shown on this page.</p>
</section>

<section id="slide-11" class="seapavaa-slide">
  <h2>First temporal success: Interior Woman</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Interior Woman temporal comparison</h3>
      <img src="{{ '/media/seapavaa2026/interior-woman-source-proposal-composite.gif' | relative_url }}" alt="Animated source, raw inference, and source-preserving composite comparison for the Interior Woman shot">
      <p>A low-motion shot where source, raw inference, and final composite hold together well enough to demonstrate temporal potential.</p>
      <details class="seapavaa-files">
        <summary>Open the parts of this example</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/media/seapavaa2026/originals/obsession_interior_woman24_full_prompt.txt' | relative_url }}" target="_blank">Full prompt</a>
          <a href="{{ '/media/seapavaa2026/originals/obsession_interior_woman24_full_prompt.json' | relative_url }}" target="_blank">Prompt JSON</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-12" class="seapavaa-slide">
  <h2>Temporal Success 2: Shot0006 Wan/VACE</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Shot0006 native three-way comparison</h3>
      <img src="{{ '/media/seapavaa2026/shot0006-source-proposal-composite.gif' | relative_url }}" alt="Animated source, raw inference, and source-preserving composite comparison for shot 0006">
      <p>This Wan/VACE test shows a second bounded temporal success with the same three-way source, inference, and composite structure.</p>
      <details class="seapavaa-files">
        <summary>Open the parts of this example</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/media/seapavaa2026/originals/shot0006_full_prompt.txt' | relative_url }}" target="_blank">Full prompt</a>
          <a href="{{ '/media/seapavaa2026/originals/shot0006_full_prompt.json' | relative_url }}" target="_blank">Prompt JSON</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-13" class="seapavaa-slide">
  <h2>What Still Fails: Hard Motion</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Shot0011 native failure comparison</h3>
      <img src="{{ '/media/seapavaa2026/shot0011-source-proposal-composite.gif' | relative_url }}" alt="Animated source, raw inference, and source-preserving composite comparison for shot 0011">
      <p>A hard-motion example where stitching and temporal generation still break down, even when the individual parts are available.</p>
    </div>
  </div>
</section>

<section id="slide-14" class="seapavaa-slide">
  <h2>Balanced Route: Context Boards</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Shot0001 with context board</h3>
      <img src="{{ '/media/seapavaa2026/shot0001-context-source-proposal-composite.gif' | relative_url }}" alt="Animated context-board, source, raw inference, and source-preserving composite comparison for shot 0001">
      <p>The context board gives the model stable visual anchors while the video comparison shows how those anchors affect the shot.</p>
    </div>
  </div>
</section>

<section id="slide-15" class="seapavaa-slide">
  <h2>Atlas: Useful, But Not Yet Reliable</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Liked atlas target</h3>
      <img src="{{ '/images_kebab/seapavaa2026/liked_t085_target_resized_to_t092.png' | relative_url }}" alt="Liked atlas target">
      <p>This Atlas was built from source-owned crops of the shot, a soft color-chart reference, and source-derived Canny control. It was kept as a generated color reference, not as a final composite.</p>
      <details class="seapavaa-files">
        <summary>Open how this Atlas was made</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/images_kebab/seapavaa2026/originals/shot0011_t085_atlas_reference/prompt.txt' | relative_url }}" target="_blank">Prompt</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-16" class="seapavaa-slide">
  <h2>Tiling and the Spatial-Context Hypothesis</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Tiled versus full-frame raw inference</h3>
      <img src="{{ '/images_kebab/seapavaa2026/reptilicus_beach_tiled_vs_fullframe_raw_inference.png' | relative_url }}" alt="Tiled versus full-frame raw inference">
      <p>The comparison tests whether adding spatial context through tiling changes the raw inference before any final composite step.</p>
    </div>
  </div>
</section>

<section id="slide-17" class="seapavaa-slide">
  <h2>What We Can Claim Now</h2>
  <p class="seapavaa-slide-intro">The example from this slide isn't shown on this page.</p>
</section>

<section id="slide-18" class="seapavaa-slide">
  <h2>Thank you!</h2>
  <p class="seapavaa-slide-intro">The example from this slide isn't shown on this page.</p>
</section>
