#!/usr/bin/env python3
"""Restore the waterworld tools' external inputs, the arXiv source of the paper the reproduction compares with.

    python -m atmosphere.waterworlds.fetch_inputs            # report state
    python -m atmosphere.waterworlds.fetch_inputs --download # fetch missing files

Each file must match the size and SHA-256 recorded in inputs.json; a mismatch stops the script instead of substituting
anything. The files are ignored by Git.
"""
from __future__ import annotations
from pathlib import Path
import sys

from shared.external_inputs import Inputs

INPUTS = Inputs(Path(__file__).resolve().parent / 'inputs.json')
manifest, input_dir, path, restore = INPUTS.manifest, INPUTS.input_dir, INPUTS.path, INPUTS.restore

if __name__ == '__main__':
    sys.exit(INPUTS.main(description=__doc__.splitlines()[0]))
