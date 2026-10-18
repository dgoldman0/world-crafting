# Editorial round 7: dispositions

**Round.** Two fresh reviewer agents, both Claude Opus 5.5 subagents, read snapshot 654ebdf: the closing section
and the abstract whole, with the revised passages of Results, Reach, Next steps, Repairs, the introduction and the
assumptions section. The prose record (`editorial_round7_conclusion_prose.md`) raised 24 findings: 0 blocking, 5
major and 19 minor, one of them optional, and judged that the section meets the author's direction. The evidence
record (`editorial_round7_conclusion_evidence.md`) raised 17: 3 blocking, 2 major and 12 minor, two of the minor
ones on the records.

**Revision.** Claude Opus 5.5, the drafting assistant, made the revision in commit 44d67d4 and wrote these
dispositions at the time. The evidence record found a factual error that every earlier round had passed: Next steps
gave Takahashi's charging law positive ground strikes and the lightning a sign that turns with the law, where the
run record shows the storms' arrangement of charge inverted and the ground strikes under both laws negative, carried
by charge left over from a run without leakage (Terluna `climate/crm/README.md:2108–2120, 2242–2244`, read for this
disposition). The two records also found the abstract stating the spectroscopy's independent check as made, and the
closing sentence placing CM1's runs outside the adapted codes.

**Terms.** Accepted: the change was made as proposed or in an equivalent form. Adapted: the finding was met by a
different change, stated. In part: what was done and what remains. Open: left, with the reason. Moot: the passage
went in the rewrite. Locations are the records' own, at 654ebdf.

## Prose record

| # | Sev. | Location | Disposition |
|---|---|---|---|
| 1 | MAJOR | abstract.tex:21–25 | Accepted in substance: "over the pressures and temperatures where that spectroscopy agrees with an independent code, a comparison planned on one column of the test world", with "the in-house model's" (13) and the starlight (evidence 5). Same passage as evidence 1 |
| 2 | MAJOR | conclusions.tex:83–86 | Adapted: "from evidence beyond the GCM: the gas and scattering fits from line-by-line spectroscopy checked against an independent code, and the cloud from cloud-resolving runs of that world, a second model whose own drop and charging laws would in turn need laboratory tests at the conditions of its storms." Same passage as evidence 3 and 11 |
| 3 | MAJOR | conclusions.tex:20–25 | Accepted: the second paragraph ends on the maps, and Yang et al.'s comparison stands beside the cloud calibration. Same passage as evidence 8 |
| 4 | MAJOR | conclusions.tex:56–60 | Accepted: "Tuning such laws on electrified storms resolved at other gravities ... would fit them to flashes computed from ...", with evidence 9's wording for Sergeev et al.'s route |
| 5 | MAJOR | results.tex:44–48 | Accepted: the four changes and their classes take a sentence of their own, and "Together they warmed ..." follows |
| 6 | MINOR | conclusions.tex:3–8 | Accepted |
| 7 | MINOR | conclusions.tex:8–11 | Accepted |
| 8 | MINOR | conclusions.tex:16–18 | Adapted: "in a two-year test of the corrected Sun clock and tilt alone" |
| 9 | MINOR | conclusions.tex:33–38 | Accepted |
| 10 | MINOR | conclusions.tex:38–42 | Adapted: the appositive "the largest of the Earth fits" cut; "gas and scattering fits" (evidence 7); "at the pressures and temperatures where that spectroscopy agrees with an independent code"; the comparisons made and planned in a sentence of their own (evidence 6) |
| 11 | MINOR | conclusions.tex:46 | Accepted |
| 12 | MINOR | conclusions.tex:62–64 | Accepted |
| 13 | MINOR | abstract.tex:15, 21 | Accepted |
| 14 | MINOR | abstract.tex:10–12 | Accepted |
| 15 | MINOR | conclusions.tex:68 | Accepted |
| 16 | MINOR | conclusions.tex:71–72 | Accepted: Loftus and Wordsworth cited for the collisions (p. 9, Sect. 3.4, with a manifest locator), and the runs "would therefore bound how much of the lunar rain's evaporation its small drops cause" |
| 17 | MINOR | conclusions.tex:81–83 | Accepted |
| 18 | MINOR, optional | abstract.tex:21–25 | Open: for the abstract's length; the abstract ends on the scheme and the cloud calibration, which the conclusion's landing carries one step further |
| 19 | MINOR | results.tex:91–92 | Accepted |
| 20 | MINOR | reach.tex:38–39 | Accepted |
| 21 | MINOR | next.tex:42–43 | Adapted: "a comparison of the repaired climate with ROCKE-3D's would measure what the two models' own physics and configurations change once the defects are removed" |
| 22 | MINOR | next.tex:79–83 | Moot: the paragraph was rewritten for evidence 2, with "since" for the cause and new openings |
| 23 | MINOR | next.tex:83–85 | Accepted |
| 24 | MINOR | introduction.tex:71–75 | Accepted, with evidence 14 |

## Evidence record

| # | Sev. | Location | Disposition |
|---|---|---|---|
| 1 | BLOCKING | abstract.tex:21–24 | Accepted, as prose 1 |
| 2 | BLOCKING | next.tex:79–83 | Accepted in substance. The paragraph, now headed "The arrangement of the lunar storms' charge.", states the inverted dipole under Takahashi's law and the normal arrangement under Saunders and Peck's in the two windows, with their conditions; the deciding measurement at hail's impact speeds; and "The windows leave the sign of the ground strikes under Takahashi's law undecided, since their strikes under both laws, all negative, carried charge left over from a run without leakage." The consequence for protection went with the error. The same reading was corrected in Results ("which arrangement the storms take therefore depends on laboratory laws ..."), in the assumptions section's sentence and table row, and in claims G11 and H22 |
| 3 | BLOCKING | conclusions.tex:83–86 | Adapted, as prose 2 |
| 4 | MAJOR | conclusions.tex:46–50 | Accepted: "the test world's storms held their charge in opposite arrangements under the two; a measurement of that sign at hail's impact speeds of 4--8~m\,s$^{-1}$, in 0.02--0.2~g\,m$^{-3}$ of cloud water at $-5$ to $-16$\,\textdegree C, would decide which arrangement the model's lunar storms take" |
| 5 | MAJOR | next.tex:14–17; conclusions.tex:38–42; abstract.tex:21–24 | Accepted at all three: "under the starlight its shortwave is built for" in Next steps, "under the starlight the scheme is built for" and "under the starlight it is built for" in the conclusion and the abstract |
| 6 | MINOR | conclusions.tex:40–41 | Accepted: "The reference has been compared with independent codes for water-only longwave at constant gravity and for Rayleigh scattering to an optical depth of 1.5, and a comparison of its carbon dioxide, oxygen, collision-induced absorption and sunlight on the design column is planned." |
| 7 | MINOR | conclusions.tex:38–40 | Accepted |
| 8 | MINOR | conclusions.tex:20–21 | Accepted, as prose 3 |
| 9 | MINOR | conclusions.tex:56–58 | Accepted: "an application of the route Sergeev et al. propose for different planetary atmospheres where observations are lacking" |
| 10 | MINOR | conclusions.tex:71 | Accepted |
| 11 | MINOR | conclusions.tex:83–86 | Accepted: "The radiation and cloud fits, which moved the test world's climate furthest, ..." |
| 12 | MINOR | results.tex:152–153 | Accepted: "on Proxima Centauri~b with Earth-like air, and \textcite{sergeev2025lightning} on TRAPPIST-1e"; the conclusion's "tidally locked planets" names the two studies' two planets together |
| 13 | MINOR | repairs.tex:106–109 | Accepted |
| 14 | MINOR | introduction.tex:73–75 | Accepted: "by ExoPlaSim's own arithmetic" |
| 15 | MINOR | abstract.tex:6 | Adapted: "ExoPlaSim~3.4.2, an Earth model extended to other worlds, and three codes built for Earth, ..." |
| 16 | MINOR (record) | claims.json H04 | Accepted: H04 and defect B24 in `notes/defect_log.md` now quote "mostly arbitrary" |
| 17 | MINOR (record) | manifest.json | Accepted: locators for Braam et al. (abstract; Sect. 4.3), Sergeev et al. (Sects. 2.2.1, 2.3, 4.2) and Way et al. (Sect. 2; Table 2's notes), each quote checked against the archived text, with the reader recorded |

## Open after this round

- Prose 18, the abstract's last step, for its length (the abstract now runs to about 440 words).
- Round 6's open items: Figure 1's caption and round 4's evidence 14 and 17, with their reasons.
- The audible cadence pass of the conclusion, recorded as silent by both reviewers, remains for the author.
- Round 8 reads the revision (44d67d4).
