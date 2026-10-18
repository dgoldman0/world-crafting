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
