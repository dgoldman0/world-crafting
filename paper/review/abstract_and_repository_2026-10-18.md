# The abstract's rewrite and the public repository, 18 October 2026

Kept by Claude Opus 5.5, the drafting assistant.

## The author's reading and directions

The author read the abstract and accepted its opening: the worlds, then the two problems, through "Constructed
worlds can depart from Earth further than natural ones". The rest, in the author's judgment, fell into the trap the
Conclusion's early drafts had fallen into, a summary of the paper section by section, with a difference of purpose:
a conclusion inspires the reader after the paper while revisiting its key points, whereas "an abstract attracts the
reader in the first place".

Claude drafted a replacement for the rest in conversation. The author approved it with one clarification: the
phrase "by the design's own models", which attributed the claim that the Moon would keep breathable air, was
unclear. The sentence now attributes that claim to calculations of atmospheric escape made for the design, and it
restores the shield's role from the earlier text, blocking the ultraviolet that heats the upper air.

The author made the world-crafting repository public on 18 October 2026 and directed that the paper name it as the
place where work on the ensemble will continue as a standalone project, if resources allow, and that the abstract
leave it out.

## The changes

| Location | Change |
|---|---|
| Abstract | After the accepted opening: the Open Moon as a test of every Earth value that depends on its four departures; the ensemble adapted to it; the three ExoPlaSim defects that bias runs of slowly rotating and tidally locked planets; the split between repairs that hold on other worlds and empirical fits that hold near their columns; the fits' larger effect on the lunar climate and the schemes that would replace them; the prospect, ending on the class beyond Gaean worlds |
| Availability, Code and data | The repository's address, `https://github.com/dgoldman0/world-crafting`, which resolved publicly on 18 October 2026; the repository will also hold the paper's release commit; work on the ensemble will continue there as a standalone project, if resources allow |
| Availability, Review history | One sentence recording the author's reading of the abstract and the rewrite |

Moved out of the abstract and kept in the body: the model versions, the list of four forms of Earth value, the
checks with SWAN's similarity numbers, the conditions on the radiation scheme, and the limit that CM1's Earth-fitted
microphysics places on the cloud calibration. Claim S15 now marks the shield's sentence; V04 left the abstract with
the SWAN check and stays cited in Verification. Next steps carries no pointer to the repository, so the condition on
the continuing work is stated once, in Availability.

## Checks and build

`paper/tools/check.py` passed with its existing warnings (107 claims cited of 109 registered; S01 and V14
uncited; the web source of H23 and N02 unchecked offline). The lint's candidates in the changed text were read: the
Open Moon flagged as a coined term, "every Earth value that depends on them" and "each world" scoped by their own
clauses, and "little or no error" a negation the claim requires. `git diff --check` was clean.

The shorter abstract moves the text of every page, so every page was inspected for layout on contact sheets, with
page 1 and the Availability pages read at 90–100 pixels per inch. No page is left near-empty; the address sets
cleanly on page 29. The screen of every page's first and last lines found one stranded line: page 22 ends on the
first line of "The longwave at the settled state". The two of the previous build, at the foot of page 14 and the
top of page 21, are gone; with no widow or club penalty set, such lines are left for the final layout.

Two clean builds from `90753d2f371741a0d1a6e19ee50be59012fe3763` (`SOURCE_DATE_EPOCH=1792353183`,
`FORCE_SOURCE_DATE=1`) gave the same PDF: 35 pages, SHA256
`4a8f9ddcce6da1a7f407cb3657976b348d289f03f311cc1cd12d8658a1b087eb`, zero overfull boxes and every font embedded.
