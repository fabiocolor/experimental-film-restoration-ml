#!/usr/bin/env python3
"""Put the graph's colour on the frame's own brightness.

  python composite_still.py faded_frame.png t185_palette_00001_.png palette.png
palette.png is the still the H3 graph uses as its three references.
"""
import sys
from pathlib import Path
from build_chroma_luma_composites import composite_source_luma_with_result_chroma

composite_source_luma_with_result_chroma(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), geometry_mode='flux-kontext-inverse',
                                         flux_kontext_border_fill='edge', shadow_chroma_mode='neutral', shadow_luma_start=32,
                                         shadow_luma_end=96, shadow_min_generated_weight=0.05)
