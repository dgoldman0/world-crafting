# The reason for CM1's slices, 18 October 2026

Kept by Claude Opus 5.5, the drafting assistant.

## The author's direction

The related-work scan (`paper/notes/related_work_scan_2026-10-18.md`) noted that the paper gives no reason for
running CM1 in slices of the GCM's climate. The author supplied the reason: the combination of rings and boxes was
shaped heavily by the hardware's limits and by "guesswork on what features would be of interest". The author
directed that the paper give that reason, and placed a global storm-resolving run, which the scan's arithmetic had
raised, outside this paper.

## The change

One sentence in the Introduction, after the sentence that introduces CM1's rings and boxes:

> These rings and boxes were sized to fit the hardware at hand, one laptop with eight processor cores, and chosen
> on a best guess at which features would be of interest.

It sits where the slices first appear, in the paragraph that already gives the GCM's cost on four processor cores.
"A best guess" carries the author's account of how the slices were chosen; the sentence names the hardware and
leaves the global run out, as the author directed.

Claim S16 registers its sources: Terluna's CM1 notes, which name the laptop and record that there is no budget for
rented compute (`climate/crm/README.md`, lines 688–690 at 186b294); its GCM notes, which give the eight cores
(`climate/gcm/README.md`, line 93); the machine's own report on 18 October 2026 (Intel Core i9-11980HK, 8 cores and
16 threads, 31 GiB of memory, a Gigabyte AERO 17 YD); and this record, for the author's account.

## Checks and build

`paper/tools/check.py` passed with its existing warnings (107 claims cited of 109 registered; S01 and V14 uncited;
the web source of H23 and N02 unchecked offline); the lint flagged nothing in the new sentence; `git diff --check`
was clean. The sentence lengthens the Introduction by about two lines, so the text from page 3 onward moved, and
every page was inspected for layout on contact sheets, with page 3 read at 110 pixels per inch. No page is left
near-empty, and Table 5 still stands whole on page 27. Next steps now opens page 23, where its heading had stood at
the foot of page 22 with two lines beneath it; page 22 now ends below Table 4 about six lines short. A screen of
every page's first and last lines, checked in the render, found two stranded lines: page 14 ends on the first line
of "Similarity and arithmetic", and page 21 opens on the last line of "The defects in other configurations".
Before the change, page 20 ended on the first line of "How the Earth values err". The paper sets no widow or club
penalty, so such lines move with every edit; they are left for the final layout.

Two clean builds from `ab465cd2d981ebba061b1b0e2373b076fd23783a` (`SOURCE_DATE_EPOCH=1792348808`,
`FORCE_SOURCE_DATE=1`) gave the same PDF: 35 pages, SHA256
`d6197caa7bd7e4334d426eba146732f0cc12b5b4f2089e554006a55e34a1a97b`, zero overfull boxes and every font embedded.
