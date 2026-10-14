---
layout: default
title: SEAPAVAA 2026 Companion
parent: Talks
nav_order: 2
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

**Talk archive, June 2026.** This page lists the examples shown at SEAPAVAA 2026, by slide title. They are earlier versions of the research and are no longer the recommended methods.

The research has moved on since June: see [where the research stands now]({{ '/research-status/' | relative_url }}) and the [FIAT/IFTA 2026 companion]({{ '/fiat-ifta-2026-companion/' | relative_url }}).

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
  <p class="seapavaa-slide-intro">The image from the presentation, followed by its separate parts.</p>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3><em>Counter Attack</em>: full-frame split</h3>
      <a href="{{ '/images_kebab/seapavaa2026/fanji_c4_row3_garden_split_comparison_fullframe_clean.png' | relative_url }}" target="_blank">
        <img src="{{ '/images_kebab/seapavaa2026/fanji_c4_row3_garden_split_comparison_fullframe_clean.png' | relative_url }}" alt="Counter Attack split hero image">
      </a>
      <p>Full-frame split view of the faded scan and the recovered composite, used as the opening example.</p>
      <details class="seapavaa-files">
        <summary>Open the prompt</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/images_kebab/seapavaa2026/originals/fanji_garden/01_source_fanji_film_copy_000015-db56f6f7.png' | relative_url }}" target="_blank">Source</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/fanji_garden/02_control_fanji_film_copy_r4_v1_03_garden_buil-dd5a1638.png' | relative_url }}" target="_blank">Control</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/fanji_garden/04_inference_frame_000000_test-7b87dbc0.png' | relative_url }}" target="_blank">Raw inference</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/fanji_garden/05_final_composite_fanji_film_copy_r4_v1_03_garden_buil-1622230d.png' | relative_url }}" target="_blank">Final composite</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-2" class="seapavaa-slide">
  <h2>Presentation Companion</h2>
  <p class="seapavaa-slide-intro">The link to this companion page, shown before the case studies.</p>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>SEAPAVAA 2026 companion</h3>
      <a href="{{ '/seapavaa-2026-companion/' | relative_url }}" target="_blank">
        <img src="{{ '/images_kebab/seapavaa2026/custom_machine_learning_for_film_restoration_qr.png' | relative_url }}" alt="QR code for the SEAPAVAA 2026 companion page">
      </a>
      <p>The QR code and link point to this page.</p>
      <details class="seapavaa-files">
        <summary>Open the companion link</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/seapavaa-2026-companion/' | relative_url }}" target="_blank">Companion page</a>
          <a href="{{ '/images_kebab/seapavaa2026/custom_machine_learning_for_film_restoration_qr.png' | relative_url }}" target="_blank">QR image</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-3" class="seapavaa-slide">
  <h2>From CopyCat to Open-Weight Chroma Recovery</h2>
  <p class="seapavaa-slide-intro">The Muralla Verde comparison, used for the transition from CopyCat to open-weight models.</p>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Muralla Verde comparison</h3>
      <a href="{{ '/images_kebab/muralla-verde/muralla-verde-comparison-preview.gif' | relative_url }}" target="_blank">
        <img src="{{ '/images_kebab/muralla-verde/muralla-verde-comparison-preview.gif' | relative_url }}" alt="Animated Muralla Verde source-to-recovery comparison">
      </a>
      <p>Source and recovery, showing the difference between source correction and chroma recovery.</p>
      <details class="seapavaa-files">
        <summary>Open this example</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/images_kebab/muralla-verde/muralla-verde-comparison-preview.gif' | relative_url }}" target="_blank">Animated comparison</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-4" class="seapavaa-slide">
  <h2>Correction Versus Recovery</h2>
  <p class="seapavaa-slide-intro">The still comparison used to define the difference between correction and recovery.</p>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Reptilicus full-frame recovery pair</h3>
      <a href="{{ '/images_kebab/seapavaa2026/recovery_pair_reptilicus_beach_fullframe.png' | relative_url }}" target="_blank">
        <img src="{{ '/images_kebab/seapavaa2026/recovery_pair_reptilicus_beach_fullframe.png' | relative_url }}" alt="Reptilicus recovery pair">
      </a>
      <p>Full-frame comparison of a faded source and an accepted composite.</p>
      <details class="seapavaa-files">
        <summary>Open the prompt</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/01_source_reptilicus_tlr_000025-40689881.jpg' | relative_url }}" target="_blank">Source</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/02_control_reptilicus_tlr_05_beach_woman_canny-73d21cd9.png' | relative_url }}" target="_blank">Control</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/04_inference_frame_000000_seed_0_cfg_1.000_Belak-0c1f0329.png' | relative_url }}" target="_blank">Raw inference</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/reptilicus_beach/05_final_composite_reptilicus_tlr_05_beach_woman_source-38de94d1.png' | relative_url }}" target="_blank">Final composite</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-5" class="seapavaa-slide">
  <h2>Why Open-Weight Models, and How I Tested Them</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>ComfyUI workflow screenshot</h3>
      <a href="{{ '/images_kebab/seapavaa2026/comfyui_workflow_fanji_waterfront_screenshot.png' | relative_url }}" target="_blank">
        <img src="{{ '/images_kebab/seapavaa2026/comfyui_workflow_fanji_waterfront_screenshot.png' | relative_url }}" alt="ComfyUI workflow screenshot">
      </a>
      <p>The test setup: source, reference, control image, prompt, model and output in one graph.</p>
      <details class="seapavaa-files">
        <summary>Open the workflow and its parts</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/images_kebab/seapavaa2026/originals/fanji_waterfront_workflow/01_source.png' | relative_url }}" target="_blank">Source image</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/fanji_waterfront_workflow/03_control.png' | relative_url }}" target="_blank">Control image</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/fanji_waterfront_workflow/04_output.png' | relative_url }}" target="_blank">Output image</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-6" class="seapavaa-slide">
  <h2>Two Source Paths, Two Different Problems</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Balanced versus unbalanced path comparison</h3>
      <a href="{{ '/images_kebab/seapavaa2026/interior_woman_balanced_vs_unbalanced_paths_2x2.png' | relative_url }}" target="_blank">
        <img src="{{ '/images_kebab/seapavaa2026/interior_woman_balanced_vs_unbalanced_paths_2x2.png' | relative_url }}" alt="Balanced versus unbalanced comparison">
      </a>
      <p>The same subject gives different results depending on whether the source is used raw or balanced before inference.</p>
      <details class="seapavaa-files">
        <summary>Open the parts of this example</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/images_kebab/seapavaa2026/originals/interior_woman_paths/01_unbalanced_source.png' | relative_url }}" target="_blank">Unbalanced source</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/interior_woman_paths/02_unbalanced_final_composite.png' | relative_url }}" target="_blank">Unbalanced final composite</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/interior_woman_paths/03_balanced_source.jpg' | relative_url }}" target="_blank">Balanced source</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/interior_woman_paths/04_balanced_final_composite.png' | relative_url }}" target="_blank">Balanced final composite</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-7" class="seapavaa-slide">
  <h2>The Reference Problem</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Leader-lady semantic contamination</h3>
      <a href="{{ '/images_kebab/seapavaa2026/leader_lady_semantic_contamination_gar01_triptych.png' | relative_url }}" target="_blank">
        <img src="{{ '/images_kebab/seapavaa2026/leader_lady_semantic_contamination_gar01_triptych.png' | relative_url }}" alt="Leader lady semantic contamination">
      </a>
      <p>A reference image can transfer identity or scene content to the subject, not only color.</p>
      <details class="seapavaa-files">
        <summary>Open the parts of this example</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/images_kebab/seapavaa2026/originals/leader_lady_gar01/01_raw_source.png' | relative_url }}" target="_blank">Raw source</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/leader_lady_gar01/02_early_marcie_contamination.png' | relative_url }}" target="_blank">Early Marcie contamination</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/leader_lady_gar01/03_belak_chart_corrected.png' | relative_url }}" target="_blank">Belak chart corrected</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-8" class="seapavaa-slide">
  <h2>The Semantic Boundary</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Source versus bad semantic inference</h3>
      <a href="{{ '/images_kebab/seapavaa2026/ben_row2_source_vs_bad_semantic_inference.png' | relative_url }}" target="_blank">
        <img src="{{ '/images_kebab/seapavaa2026/ben_row2_source_vs_bad_semantic_inference.png' | relative_url }}" alt="Source versus bad semantic inference">
      </a>
      <p>A failure case: the model produces a plausible image that does not match the content of the original frame.</p>
      <details class="seapavaa-files">
        <summary>Open the parts of this example</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/images_kebab/seapavaa2026/originals/ben_row2/01_source.png' | relative_url }}" target="_blank">Source</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/ben_row2/02_bad_semantic_inference.png' | relative_url }}" target="_blank">Bad semantic inference</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-9" class="seapavaa-slide">
  <h2>The Product Contract</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Full lineage board</h3>
      <a href="{{ '/images_kebab/seapavaa2026/jug_auditorium_full_lineage_5stage.png' | relative_url }}" target="_blank">
        <img src="{{ '/images_kebab/seapavaa2026/jug_auditorium_full_lineage_5stage.png' | relative_url }}" alt="Full lineage board">
      </a>
      <p>The lineage board shows source, control, reference, raw inference and final composite as separate items.</p>
      <details class="seapavaa-files">
        <summary>Open the parts of this example</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/images_kebab/seapavaa2026/originals/jug_auditorium/01_source_juggernaut_tlr_000066-ed2dda29.jpg' | relative_url }}" target="_blank">Source</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/jug_auditorium/02_control_juggernaut_tlr_r5_v1_10_auditorium_c-16fdc330.png' | relative_url }}" target="_blank">Control</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/jug_auditorium/04_inference_frame_000000_test-feb2c14f.png' | relative_url }}" target="_blank">Raw inference</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/jug_auditorium/05_final_composite_juggernaut_tlr_r5_v1_10_auditorium_c-9d2f7cbe.png' | relative_url }}" target="_blank">Final composite</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-10" class="seapavaa-slide">
  <h2>The Still Route Finally Generalized</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Counter Attack row-9 top three raw generations</h3>
      <a href="{{ '/images_kebab/seapavaa2026/fanji_round4_row9_top3_raw_generations.png' | relative_url }}" target="_blank">
        <img src="{{ '/images_kebab/seapavaa2026/fanji_round4_row9_top3_raw_generations.png' | relative_url }}" alt="Counter Attack row-9 top three raw generations">
      </a>
      <p>Three prompt variants on the same source, from the prompt tests that made the still route more reliable.</p>
      <details class="seapavaa-files">
        <summary>Open the parts of this example</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/images_kebab/seapavaa2026/originals/fanji_child_close_top3_fullframe/fanji_film_copy_000059.png' | relative_url }}" target="_blank">Source</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/fanji_child_close_top3_fullframe/i2_frame_000000_test.png' | relative_url }}" target="_blank">Iris Spectrum</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/fanji_child_close_top3_fullframe/c4_frame_000000_test.png' | relative_url }}" target="_blank">Celeste Redguard</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/fanji_child_close_top3_fullframe/cl2_frame_000000_test.png' | relative_url }}" target="_blank">Clara Anchor</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-11" class="seapavaa-slide">
  <h2>First temporal success: Interior Woman</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Interior Woman temporal comparison</h3>
      <img src="{{ '/media/seapavaa2026/interior-woman-source-proposal-composite.gif' | relative_url }}" alt="Animated source, raw inference, and source-preserving composite comparison for the Interior Woman shot">
      <p>A low-motion shot where source, raw inference and final composite stay consistent over time.</p>
      <details class="seapavaa-files">
        <summary>Open this example</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/media/seapavaa2026/interior-woman-source-proposal-composite.gif' | relative_url }}" target="_blank">Animated comparison</a>
          <a href="{{ '/images_kebab/seapavaa2026/obsession_interior_woman24_source_raw_inference_final_composite_preview.png' | relative_url }}" target="_blank">Preview still</a>
          <a href="{{ '/images_kebab/seapavaa2026/obsession_interior_woman24_source_raw_inference_final_composite_with_prompt_side.png' | relative_url }}" target="_blank">Prompt-side still</a>
        </div>
      </details>
      <details class="seapavaa-files">
        <summary>Open the parts of this example</summary>
        <div class="seapavaa-filelist">
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
      <h3><em>Obsession</em>, shot 6: source, model output and composite</h3>
      <img src="{{ '/media/seapavaa2026/shot0006-source-proposal-composite.gif' | relative_url }}" alt="Animated source, raw inference, and source-preserving composite comparison for shot 0006">
      <p>A second Wan/VACE test with consistent results over time, shown as source, inference and composite.</p>
      <details class="seapavaa-files">
        <summary>Open this example</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/media/seapavaa2026/shot0006-source-proposal-composite.gif' | relative_url }}" target="_blank">Animated comparison</a>
          <a href="{{ '/images_kebab/seapavaa2026/shot0006_source_raw_inference_final_composite_fullrun_preview.png' | relative_url }}" target="_blank">Preview still</a>
        </div>
      </details>
      <details class="seapavaa-files">
        <summary>Open the parts of this example</summary>
        <div class="seapavaa-filelist">
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
      <h3><em>Obsession</em>, shot 11: a failure with hard motion</h3>
      <img src="{{ '/media/seapavaa2026/shot0011-source-proposal-composite.gif' | relative_url }}" alt="Animated source, raw inference, and source-preserving composite comparison for shot 0011">
      <p>A shot with fast motion, where stitching and temporal generation fail.</p>
      <details class="seapavaa-files">
        <summary>Open this example</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/media/seapavaa2026/shot0011-source-proposal-composite.gif' | relative_url }}" target="_blank">Animated comparison</a>
          <a href="{{ '/images_kebab/seapavaa2026/shot0011_fourchunk_vace_stitched_source_raw_inference_composite_preview.png' | relative_url }}" target="_blank">Preview still</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-14" class="seapavaa-slide">
  <h2>Balanced Route: Context Boards</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3><em>Obsession</em>, shot 1, with a context board</h3>
      <img src="{{ '/media/seapavaa2026/shot0001-context-source-proposal-composite.gif' | relative_url }}" alt="Animated context-board, source, raw inference, and source-preserving composite comparison for shot 0001">
      <p>The context board gives the model fixed visual references; the video comparison shows their effect on the shot.</p>
      <details class="seapavaa-files">
        <summary>Open this example</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/media/seapavaa2026/shot0001-context-source-proposal-composite.gif' | relative_url }}" target="_blank">Animated comparison</a>
          <a href="{{ '/images_kebab/seapavaa2026/shot0001_t091_source_raw_inference_final_composite_fullrun_with_context_board.png' | relative_url }}" target="_blank">Preview still</a>
          <a href="{{ '/images_kebab/seapavaa2026/02_overview_t091_generated_anchor_contact_sheet_t073_unl-55294673.png' | relative_url }}" target="_blank">Context board</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-15" class="seapavaa-slide">
  <h2>Atlas: Useful, But Not Yet Reliable</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Selected atlas target</h3>
      <a href="{{ '/images_kebab/seapavaa2026/liked_t085_target_resized_to_t092.png' | relative_url }}" target="_blank">
        <img src="{{ '/images_kebab/seapavaa2026/liked_t085_target_resized_to_t092.png' | relative_url }}" alt="Liked atlas target">
      </a>
      <p>This Atlas was built from source-owned crops of the shot, a soft color-chart reference, and source-derived Canny control. It was kept as a generated color reference, not as a final composite.</p>
      <details class="seapavaa-files">
        <summary>Open how this Atlas was made</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/images_kebab/seapavaa2026/originals/shot0011_t085_atlas_reference/01_source_atlas.png' | relative_url }}" target="_blank">Source atlas</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/shot0011_t085_atlas_reference/03_source_canny_control.png' | relative_url }}" target="_blank">Canny control</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/shot0011_t085_atlas_reference/04_generated_atlas_reference.png' | relative_url }}" target="_blank">Generated Atlas reference</a>
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
      <a href="{{ '/images_kebab/seapavaa2026/reptilicus_beach_tiled_vs_fullframe_raw_inference.png' | relative_url }}" target="_blank">
        <img src="{{ '/images_kebab/seapavaa2026/reptilicus_beach_tiled_vs_fullframe_raw_inference.png' | relative_url }}" alt="Tiled versus full-frame raw inference">
      </a>
      <p>Tests whether tiling, which adds spatial context, changes the raw inference.</p>
      <details class="seapavaa-files">
        <summary>Open the full-size images behind this comparison</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/images_kebab/seapavaa2026/originals/reptilicus_t001_tiling/reptilicus_t001_four_tile_raw_inference_hard_stitch.png' | relative_url }}" target="_blank">Tiled raw inference</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/reptilicus_t001_tiling/reptilicus_t001_fullframe_clara_baseline_frame_000000_test.png' | relative_url }}" target="_blank">Full-frame raw inference</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-17" class="seapavaa-slide">
  <h2>What We Can Claim Now</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Counter Attack 600-frame full run</h3>
      <img src="{{ '/media/seapavaa2026/fanji-600-source-proposal-composite.gif' | relative_url }}" alt="Animated source, raw inference, and source-preserving composite comparison for the Counter Attack sequence">
      <p>The method applied frame by frame across a longer sequence.</p>
      <details class="seapavaa-files">
        <summary>Open this example</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/media/seapavaa2026/fanji-600-source-proposal-composite.gif' | relative_url }}" target="_blank">Animated comparison</a>
          <a href="{{ '/images_kebab/seapavaa2026/fanji_600_source_raw_inference_final_composite_fullrun_preview.png' | relative_url }}" target="_blank">Preview still</a>
        </div>
      </details>
    </div>
  </div>
</section>

<section id="slide-18" class="seapavaa-slide">
  <h2>Thank you!</h2>
  <div class="seapavaa-grid">
    <div class="seapavaa-card">
      <span class="seapavaa-role">Seen in the talk</span>
      <h3>Candy Ending matched-reference recovery</h3>
      <a href="{{ '/images_kebab/seapavaa2026/originals/candy_ending_frame_1619/05_final_composite.png' | relative_url }}" target="_blank">
        <img src="{{ '/images_kebab/seapavaa2026/originals/candy_ending_frame_1619/05_final_composite.png' | relative_url }}" alt="Candy Ending matched-reference recovery">
      </a>
      <p>A matched, non-generated reference frame provides the color; the faded source frame provides geometry and luma.</p>
      <details class="seapavaa-files">
        <summary>Open the full-size images behind this example</summary>
        <div class="seapavaa-filelist">
          <a href="{{ '/images_kebab/seapavaa2026/originals/candy_ending_frame_1619/01_source_frame.jpg' | relative_url }}" target="_blank">Source frame</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/candy_ending_frame_1619/02_matched_reference_frame_2030.png' | relative_url }}" target="_blank">Matched reference frame</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/candy_ending_frame_1619/03_source_canny_control.png' | relative_url }}" target="_blank">Canny control</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/candy_ending_frame_1619/04_raw_inference.png' | relative_url }}" target="_blank">Raw inference</a>
          <a href="{{ '/images_kebab/seapavaa2026/originals/candy_ending_frame_1619/05_final_composite.png' | relative_url }}" target="_blank">Final composite</a>
        </div>
      </details>
    </div>
  </div>
</section>
