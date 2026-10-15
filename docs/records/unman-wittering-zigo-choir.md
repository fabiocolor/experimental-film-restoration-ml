---
layout: default
title: "Unman, Wittering and Zigo, choir"
parent: "Example Records"
nav_order: 5
permalink: /records/unman-wittering-zigo-choir/
---

# Unman, Wittering and Zigo (1971), choir: record

| | |
| --- | --- |
| Source | *Unman, Wittering and Zigo* trailer, from the archive.org [trailer reel scan](https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps). One shot of 164 frames, unbalanced, faded to magenta. |
| Route | Synthetic reference. TeleStyle (a LoRA for Qwen Image Edit 2511) made candidate frames; 101 passed review and became teachers (82 for training, 19 for validation). The Temporal CbCr adapter, trained on this shot only, coloured the rest. No MiniMax H3 frames were used. The scan keeps its own luma. |
| Code | [temporal-cbcr-adapter](https://github.com/fabiocolor/temporal-cbcr-adapter). |
| Finished | Shown on the Temporal CbCr page. |
| Colour check | A simple score of how much red, green and blue the result holds: 1.46, against the 3 normally wanted; the shot is mostly skin, blue robes and a grey wall. It is here because it is the strongest synthetic-reference shot with faces. |
| Reproduction | Not yet. The teacher frames and adapter settings for this shot are not published. |
