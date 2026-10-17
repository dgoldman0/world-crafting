"""Structure, citation and claim checks for the paper. Exit status 1 on any error; warnings are reported.

    python3 paper/tools/check.py

- every \\input file exists, every \\includegraphics file exists, headings stay unnumbered (secnumdepth 0);
- every cited key is in references.bib;
- every \\claim{ID} in the text is in claims.json, and every claim's source exists:
    terluna:<path>[#...]   a file in Terluna at commit 186b294 (checked with git cat-file in the local checkout);
    repo:<path>[#...]      a file in this repository;
    drive:<path>           a file on Terluna's research drive (a warning when the drive is absent);
    calc:<text>            a calculation stated in the claim (its script or formula named in the text).
Evidence states: observation, calculation, conditional model, calibration, reproduction, identity, sensitivity,
documented, finding, similarity, benchmark, implementation.
These are completeness checks; they establish nothing about whether a claim is right.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
REPO = PAPER.parent
TERLUNA = Path('/home/kir/Documents/Projects/terluna')
COMMIT = '186b294'
errors, warnings = [], []


def tex_without_comments(text: str) -> str:
    return re.sub(r'(?<!\\)%.*', '', text)


def inputs(path: Path, seen=None) -> list[Path]:
    seen = seen or []
    text = tex_without_comments(path.read_text())
    for name in re.findall(r'\\input\{([^}]+)\}', text):
        p = PAPER / (name if name.endswith('.tex') else name + '.tex')
        if not p.exists():
            errors.append(f'missing input {p.relative_to(REPO)} (from {path.name})')
            continue
        seen.append(p)
        inputs(p, seen)
    return seen


def main() -> int:
    main_tex = PAPER / 'main.tex'
    if '\\setcounter{secnumdepth}{0}' not in main_tex.read_text():
        errors.append('main.tex must set secnumdepth 0: headings stay unnumbered')
    files = [main_tex] + inputs(main_tex)
    bib = (PAPER / 'references.bib').read_text() if (PAPER / 'references.bib').exists() else ''
    keys = set(re.findall(r'@\w+\s*\{\s*([^,\s]+)\s*,', bib))
    claims_path = PAPER / 'claims.json'
    register = {c['id']: c for c in json.loads(claims_path.read_text())['claims']} if claims_path.exists() else {}
    used_claims, cited = set(), set()
    for f in files:
        text = tex_without_comments(f.read_text())
        for group in re.findall(r'\\(?:text|paren|auto|foot)?cite[tp]?\*?(?:\[[^\]]*\])*\{([^}]+)\}', text):
            cited |= {k.strip() for k in group.split(',') if k.strip()}
        for g in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', text):
            if not (PAPER / g).exists():
                errors.append(f'missing figure {g} (in {f.name})')
        used_claims |= set(re.findall(r'\\claim\{([^}]+)\}', text))
        if re.search(r'\\(sub)*section\*?\{', text) and re.search(r'\\subsubsection', text):
            warnings.append(f'{f.name}: subsubsections; the paper keeps subsectioning light')
    for k in sorted(cited - keys):
        errors.append(f'citation key not in references.bib: {k}')
    for cid in sorted(used_claims):
        if cid not in register:
            errors.append(f'claim {cid} cited in the text but absent from claims.json')
    for cid, c in register.items():
        for src in ([c['source']] if isinstance(c['source'], str) else c['source']):
            kind, _, rest = src.partition(':')
            path = rest.split('#')[0]
            if kind == 'terluna':
                ok = subprocess.run(['git', '-C', str(TERLUNA), 'cat-file', '-e', f'{COMMIT}:{path}'],
                                    capture_output=True).returncode == 0
                if not ok:
                    errors.append(f'claim {cid}: {path} absent from Terluna at {COMMIT}')
            elif kind == 'repo':
                if not (REPO / path).exists():
                    errors.append(f'claim {cid}: {path} absent from this repository')
            elif kind == 'drive':
                if not Path('/media/projectspace').exists():
                    warnings.append(f'claim {cid}: research drive not mounted, {path} unchecked')
                elif not Path(path).exists():
                    errors.append(f'claim {cid}: {path} absent from the research drive')
            elif kind != 'calc':
                errors.append(f'claim {cid}: unknown source kind {kind!r}')
        if c.get('state') not in ('observation', 'calculation', 'conditional model', 'calibration', 'reproduction',
                                  'identity', 'sensitivity', 'documented', 'finding', 'similarity',
                                  'benchmark', 'implementation'):
            errors.append(f"claim {cid}: unknown evidence state {c.get('state')!r}")
    unused = sorted(set(register) - used_claims)
    print(f'{len(files)} TeX files; {len(cited)} cited keys of {len(keys)} in references.bib; '
          f'{len(used_claims)} claims cited of {len(register)} registered')
    if unused:
        warnings.append(f'{len(unused)} registered claims not cited in the text: {", ".join(unused[:12])}'
                        + (' ...' if len(unused) > 12 else ''))
    for w in warnings:
        print('WARN ', w)
    for e in errors:
        print('ERROR', e)
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
