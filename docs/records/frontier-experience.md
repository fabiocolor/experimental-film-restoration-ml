---
layout: default
title: "Frontier Experience"
parent: "Example Records"
nav_order: 4
permalink: /records/frontier-experience/
---

# Frontier Experience (1975): record

| | |
| --- | --- |
| Source | A faded film print of *Frontier Experience* (1975, directed by Barbara Loden). |
| Reference | A telecine of the same film, supplied by Ross Lipman. Cadence problems, but aligned closely enough to use as a colour reference. Only its colour is used, not its detail. |
| Route | Historical reference. Temporal CbCr adapter (ConvLSTM U-Net, 931,274 parameters), trained on 926 aligned frame pairs at 1464 × 1080. The scan keeps its own luma; the adapter predicts only CbCr. No generated targets. |
| Code | [temporal-cbcr-adapter](https://github.com/fabiocolor/temporal-cbcr-adapter), checkpoint manifest `config/promoted_frontier_checkpoint.json` (epoch 25, SHA-256 `d2e5069f27c8896ab6fd9b072c9955ce0c97ec16cbe7671e1b69df550fd2c9ba`). |
| Evaluation | 504 held-out frames from 16 shots. Lower colour error than CopyCat on 9 of 16 shots; overall colour error 1.79% higher than CopyCat. |
| Finished | The checkpoint named above. Some skies and shadows do not fully resolve. |
| Reproduction | Not yet. The checkpoint (11 MB), the frame pairs and the film material are not published. |

A newer version of this example is being made.
