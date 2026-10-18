"""A prose lint for the editorial passes: it lists candidate places, it never clears a gate.

    python3 paper/tools/lint.py [section.tex ...]

The charter's G4 excludes the authorial phrases "not" and "rather than" and asks for other negative-contrast
structures to be examined by meaning; G2 and G4 exclude reader-management, self-reference, stock transitions and
promotional language; the repository's AGENTS.md adds empty actions on abstractions, coined terms and claims
wider than their evidence. This script finds the words; each hit still needs a reading, and its counts are
screening, never a verdict on the prose. Bibliographic titles, code,
quotations and labels are outside its scope, so it strips commands, citations and verbatim before scanning.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
PATTERNS = {
    'excluded: not': r"\bnot\b|n't\b",
    'excluded: rather than': r'\brather than\b',
    'negative contrast (read for meaning)': r'\b(no|never|neither|nor|without|instead of|unlike|cannot)\b',
    'self-reference': r'\b(this (paper|article|study|work|section)|the present (paper|analysis|work)|we (show|present|argue|demonstrate))\b',
    'reader management': r'\b(note that|it is (important|worth noting|clear)|as (we will|we shall) see|recall that|importantly|interestingly|notably)\b',
    'stock transition': r'^\s*(Moreover|Furthermore|In addition|Additionally|However|Thus|Hence|Therefore|Overall|In summary|In conclusion)\b',
    'promotional': r'\b(novel|first time|groundbreaking|crucial|key|unprecedented|robust|powerful|significant(ly)?(?! wave height)|state-of-the-art|comprehensive)\b',
    'vague intensifier': r'\b(very|quite|rather|somewhat|really|extremely|highly)\b',
    # AGENTS.md, Writing: verbs of action on abstractions, and the coined terms of the rejected first draft
    'possible empty action (read for meaning)': r'\b(carr(y|ies|ied|ying)|sits?|hides?|hiding|answers?|stands? behind|'
                                                r'expos(e|es|ed)|reach(es|ed)?|divides? the work|owns)\b',
    'coined term': r'\b(hidden Earth|Earth inside|where Earth hides|Open Moon)\b',
    'universal claim (check its scope)': r'\b(each|every|all|most|always|any)\b',
    'generic verb (earns its place?)': r'\b(shows?|provides?|supports?|demonstrates?|allows?|gives?|establish(es)?|'
                                       r'reflects?|enables?|address(es)?)\b',
}


def prose(text: str) -> list[tuple[int, str]]:
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        line = re.sub(r'(?<!\\)%.*', '', line)
        line = re.sub(r'\\(cite[tp]?|claim|label|ref|eqref|code|url|href|includegraphics|input)\*?(\[[^\]]*\])*\{[^}]*\}', ' ', line)
        line = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?', ' ', line)
        out.append((n, line))
    return out


def main(argv) -> int:
    files = [Path(a).resolve() for a in argv] or sorted((PAPER / 'sections').glob('*.tex'))
    total = {k: 0 for k in PATTERNS}
    for f in files:
        hits = []
        for n, line in prose(f.read_text()):
            for name, pat in PATTERNS.items():
                for m in re.finditer(pat, line, flags=re.IGNORECASE if name != 'stock transition' else 0):
                    hits.append((n, name, line.strip()[:110]))
                    total[name] += 1
        if hits:
            print(f'== {f.relative_to(PAPER)}')
            for n, name, line in hits:
                print(f'  {n:4d}  {name:38s} {line}')
    print('totals:', ', '.join(f'{k}: {v}' for k, v in total.items() if v))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
