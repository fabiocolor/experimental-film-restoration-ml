# How the example figures and the kit graphs are made

- `make_examples.py <dir with the release videos>`: cuts the source | result pairs in `docs/images_kebab/examples/` from the
  videos on the `examples-2026-10` release, the Google Drive comparison videos and the published stills. Every output is a
  JPEG under 1 MiB. Needs ffmpeg, NumPy and Pillow.
- `make_graphs.py <object_info.json>`: generates the laid-out ComfyUI graphs of the single-frame kit and the balanced kit's
  palette still (UI format, with notes) and their API-format twins, from the node schemas of a running ComfyUI
  (`GET /object_info`). `wfbuild.py` is the small builder it uses.

The graphs were checked by loading them in the ComfyUI editor and comparing the prompt it produces with the API-format
graph node for node, and by running the composite branch on a CPU ComfyUI against the kit's `composite_still.py`.
