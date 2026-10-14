---
layout: default
title: "Example Records"
nav_order: 7
has_children: true
permalink: /records/
---

# Example records

One record for each example on this site: the source, the route, the graph and models, the settings, the approval, and whether it has been reproduced from the published files.

| Example | Area | Route | Reproduced from the published files |
| --- | --- | --- | --- |
| [Reptilicus, beach]({{ '/records/reptilicus-beach/' | relative_url }}) | Faded colour recovery (home page) | Earlier single-frame route | Inputs and outputs published; the [single-frame kit]({{ '/downloads/colour-recovery-single-frame/' | relative_url }}) is the same route with the later prompt |
| [Counter Attack, crowd]({{ '/records/counter-attack-crowd/' | relative_url }}) | Faded colour recovery (home page) | MiniMax H3 with the Fun ControlNet, Temporal CbCr adapter | Not yet |
| [Counter Attack, waterfront]({{ '/records/counter-attack-waterfront/' | relative_url }}) | Faded colour recovery | MiniMax H3 with TeleStyle repairs | The approved first still: [single-frame kit]({{ '/downloads/colour-recovery-single-frame/' | relative_url }}), core-node rerun mean ΔE 1.89 |
| [Folgers]({{ '/records/folgers/' | relative_url }}) | Faded colour recovery, balanced kit | Balanced-source route | Yes, every stage within ΔE 1.5 |
| [Frontier Experience]({{ '/records/frontier-experience/' | relative_url }}) | Temporal CbCr, historical reference | Temporal CbCr adapter | Not yet |
| [Unman, Wittering and Zigo, choir]({{ '/records/unman-wittering-zigo-choir/' | relative_url }}) | Temporal CbCr, synthetic reference | TeleStyle and Temporal CbCr | Not yet |
| [Candy Candy]({{ '/records/candy-candy/' | relative_url }}) | Temporal CbCr, historical reference (earlier route) | CopyCat in Nuke | Not yet |
| [Wong flute players]({{ '/records/wong-flute-players/' | relative_url }}) | Diffusion healing | MiniMax H3, film luma, Wan VACE | Second pass only (ΔE 0.9) |
| [El Tinterillo, stairs]({{ '/records/el-tinterillo-stairs/' | relative_url }}) | Diffusion reconstruction | Hybrid, reference still, MiniMax H3, seam blend | Hybrid step (identical) and seam blend (ΔE 1.07) |
| [The General, garden]({{ '/records/general-1926-garden/' | relative_url }}) | Black-and-white colourization | Qwen 2511, base MiniMax H3 | Not yet |
| [Her Boy Friend, café]({{ '/records/her-boy-friend-cafe/' | relative_url }}) | Black-and-white colourization | Qwen 2511, MiniMax H3 ControlNet, stock reading | Not yet |
| [Below the Deadline, parlour]({{ '/records/below-the-deadline-parlour/' | relative_url }}) | Black-and-white colourization | Qwen 2511, MiniMax H3 ControlNet, stock reading | Not yet |
| [The Racing Fool, couple]({{ '/records/racing-fool-couple/' | relative_url }}) | Black-and-white colourization | Qwen 2511, MiniMax H3 ControlNet, stock reading | Not yet |
| [The Wildcat, ranch yard]({{ '/records/wildcat-yard/' | relative_url }}) | Black-and-white colourization | Qwen 2511, MiniMax H3 ControlNet, stock reading | Not yet |
| [Books: From Manuscript to Classroom]({{ '/records/books-manuscript-classroom/' | relative_url }}) | Black-and-white colourization | Qwen 2511, MiniMax H3 ControlNet, stock reading | Not yet |
| [Rambles 'Round Rio, ox cart]({{ '/records/rambles-round-rio-oxcart/' | relative_url }}) | Black-and-white colourization | Qwen 2511, MiniMax H3 ControlNet, stock reading | Not yet |

ΔE is the average CIEDE2000 colour difference against the approved result. The pass mark is 1.5 per stage; about 2.3 is the smallest difference most viewers can see.
