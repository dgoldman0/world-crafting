"""Render every page of the paper's PDF for the exact-build visual review (G7) and record what was rendered.

    python3 paper/tools/render_pages.py OUTDIR [--dpi 90]

Renders each page with poppler (pdftoppm) and, for a second renderer, MuPDF (mutool draw), writes
OUTDIR/poppler/p-NN.png and OUTDIR/mupdf/p-NN.png, and prints a JSON record: the PDF's sha256, page count,
renderer versions, and each page's render hash, so that a later build's pages can be matched to pages already
inspected. Fonts and metadata come from pdffonts and pdfinfo. A render hash establishes only that two renders
are identical; the inspection itself is the reviewer's.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

PDF = Path(__file__).resolve().parents[1] / 'build' / 'main.pdf'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def version(cmd: list[str]) -> str:
    out = subprocess.run(cmd, capture_output=True, text=True)
    return (out.stdout + out.stderr).strip().splitlines()[0]


def main() -> int:
    out = Path(sys.argv[1])
    dpi = int(sys.argv[sys.argv.index('--dpi') + 1]) if '--dpi' in sys.argv else 90
    (out / 'poppler').mkdir(parents=True, exist_ok=True)
    (out / 'mupdf').mkdir(parents=True, exist_ok=True)
    subprocess.run(['nice', 'pdftoppm', '-r', str(dpi), '-png', str(PDF), str(out / 'poppler' / 'p')], check=True)
    subprocess.run(['nice', 'mutool', 'draw', '-q', '-r', str(dpi), '-o', str(out / 'mupdf' / 'p-%02d.png'), str(PDF)],
                   check=True)
    info = subprocess.run(['pdfinfo', str(PDF)], capture_output=True, text=True).stdout
    fonts = subprocess.run(['pdffonts', str(PDF)], capture_output=True, text=True).stdout.splitlines()[2:]
    pages = sorted((out / 'poppler').glob('p-*.png'))
    record = dict(
        pdf=str(PDF), pdf_sha256=sha(PDF), dpi=dpi,
        renderers=dict(poppler=version(['pdftoppm', '-v']), mupdf=version(['mutool', '-v'])),
        metadata={k.strip(): v.strip() for k, v in (l.split(':', 1) for l in info.splitlines() if ':' in l)},
        fonts_not_embedded=[l for l in fonts if l.split()[-5:-4] != ['yes'] and len(l.split()) > 5],
        pages=[dict(page=i + 1, poppler=sha(p)[:16],
                    mupdf=sha(out / 'mupdf' / p.name)[:16] if (out / 'mupdf' / p.name).exists() else None)
               for i, p in enumerate(pages)],
    )
    print(json.dumps(record, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
