# Exact-build visual and production review (G7)

**Reviewer.** Claude Opus 5.5, the drafting assistant (main session), 18 October 2026. The reviewer drafted the text
it inspected; this is a separate pass recorded with its actual identity, as the charter's E4 allows, and the author's
own inspection of the PDF is a separate review still to come.

**Source identity.** Commit 94d337a (`94d337a68f248528f54b09421d403ab942216003`), working tree clean for every build
input. sha256 of each input at that commit:

| Input (under `paper/`) | sha256 |
|---|---|
| `main.tex` | 116d1a8ff0f25694a864c6d7d9d6922e5289e6e583f38c15eac07b81a06facd8 |
| `references.bib` | c0c9662b362141759bce9a27bb566e7ee6a00479ef773273f1dc109d7888747e |
| `Makefile` | a79bebc7bc3abc1f5e14e31aceddabfa2bbdffee6bf9587a4b9ebf5e9949ad7d |
| `figures/fig_gap.pdf` | 943022583a689edf2a10a0cd68503b9131280d9695f51ec0568f30e5373bd422 |
| `figures/fig_layers.pdf` | 119955426500005e90653008a80bf9a37b4c570875c20ff3576d85dae8bb701a |
| `figures/fig_regimes.pdf` | aa8282a952f8dfcdcc72ee4508e0b3ce969c3ab6158355ef70aa0923a13d6c7f |
| `figures/fig_repairs.pdf` | 2fcb37ca7a6538c8187332ede7682c57d0111ecc087c89e454835865d31c59c9 |
| `figures/fig_slant.pdf` | 5af5b9ead93a4b611b79c58479afeac4a3704f0390cb3b20260739f954811ee4 |
| `figures/fig_sun_clock.pdf` | 1a70fb8a8c7b6ee2f4593098c88b8f1337a91fe1f852010b15e33df1ae6affe6 |
| `sections/abstract.tex` | 1d22734b8e9c39bc9b52f4eeff8c8436ee598b84e6bf5c14025f2b3fd17416b0 |
| `sections/appendix.tex` | 17abe050d20a86031b7f3b1e426afcca0050cb9928bdb6500d84850d73013bbc |
| `sections/assumptions.tex` | 77bc704fe58d964ff2567a39ffbdf6e2af9b0cc422bfb88e04d25e949b877107 |
| `sections/availability.tex` | 8cadbf912ba8e0d4a92b9c23f60fbd95dcd407f3da3c5cc8f3382995e96c08a7 |
| `sections/conclusions.tex` | acee92c3ae5c1667275745b96267cf8ff487f21e39530ab0e2f58d8c15ac8208 |
| `sections/introduction.tex` | a88f442f589e007dbb57f081334fc53ef066dbc26734d9f6610e12194bbea3d2 |
| `sections/next.tex` | 789a34bd471f58e00c23ae3f422796c7c3333308337f80e49898017f862753ad |
| `sections/reach.tex` | fff8183910168eeb9ee837c8e5766ac0bea7f64b6e95e0d63b8cf821e26f5b63 |
| `sections/repairs.tex` | c846dbbf4dbaf39ae194d7bb93a26204aaa1b12f4b24e7aa1accdd948b281102 |
| `sections/results.tex` | 112e8074232fd04300fccf280bb7bf5341e0b3d34a31a5c9a4561e46fcc4ca35 |
| `sections/verification.tex` | 4ddeb46903522c7276a17cb5e3537b87181b38f676b45e2f939ce07ffcf92e00 |
| `sections/worlds.tex` | 453a1d6cd6e39bf3ed867b3e704ad05e0cf86405a4cab258472481189bfb2112 |

**Build.** `make paper` (`make -C paper pdf`): latexmk 4.83 with pdfTeX 3.141592653-2.6-1.40.25 (TeX Live
2023/Debian) and biber 2.19, with `SOURCE_DATE_EPOCH=1792299769` (2026-10-18 01:02:49 −0400, the time of the last
commit that changed a build input) and `FORCE_SOURCE_DATE=1`, and `\pdftrailerid{}` in `main.tex`. Two builds from
a cleaned build directory gave byte-identical PDFs. The log holds no overfull box, no undefined reference or citation,
and one underfull box, in the bibliography (below).

**The PDF.** sha256 `c0c63cf1eff7c476a6913f0b06830f9d9a03ec8c48de50e099688d67aa17ff55`; 34 pages, A4 (595.276 ×
841.89 pt), PDF 1.5. Metadata: Title "Modelling Earth-like worlds beyond Earth's range: ExoPlaSim, CM1, SWAN and SWASH
adapted and tested on a breathable Moon"; Author "Daniel S. Goldman"; Creator "LaTeX with hyperref"; Producer
"pdfTeX-1.40.25"; creation and modification dates 2026-10-18 01:02:49 −0400. Fonts (pdffonts): every font embedded
and subset — TeXGyreTermesX Regular, Bold and Italic, TeXGyreTermes-Regular, NewTXMI, NewTXMI7, txsys, txexs,
txmiaX, SFRM0900, SFRM1095, t1xtt, and DejaVuSans with its bold in the figures. Links (counted on a qpdf-decompressed
copy): 218 link annotations, with borders hidden; 78 URIs, 77 to doi.org and one to the author's ORCID record,
https://orcid.org/0000-0003-2835-3521.

**Renderers.** pdftoppm 24.02.0 (poppler) for every page, and MuPDF's mutool 1.23.10 for every page as the second
renderer, both at 90 dpi, by `paper/tools/render_pages.py`. Every page was read whole in the poppler render; the six
figure pages were read again in the MuPDF render. The renders are kept outside the repository; their hashes follow, so
a later build's pages can be matched to these.

## Page by page

| Page | Contents | Observations |
|---|---|---|
| 1 | Title, author with ORCID mark, date, abstract, start of the introduction | Title in three lines as set; the abstract justified and complete; the date reads 17 October 2026 (below) |
| 2–3 | Introduction; start of "Worlds beyond Earth's range and the test world" | Text and citations resolved; no widow or orphan line at the section heading |
| 4 | Figure 1 and its caption; text | Both panels legible: every point labelled clear of the others and of the lines (Venus, Titan, Mars at 1 bar, the breathable Moon at 1.2 and 1.0 atm, Mars present and at 1 bar, the open points of the slowly rotating planets); axis labels and units complete; the two annotations ("PlaSim's horizon air mass of 35 holds here", "Earth's column: the broadband fits' range", "PlaSim's per-day formulas hold") clear of the data. The caption distinguishes computed natural worlds from constructed or illustrative points |
| 5 | Table 1; heading "Earth values and defects in the released codes"; text | Table rules and alignment clean; units in the first column |
| 6 | Text | Inline mathematics (the slant factor, $GM/r^2$, units) set correctly |
| 7–9 | Text; Table 2 from its caption over three pages | Continuation headers "Table 2, continued" on pages 8 and 9; the "Charging laws" row reads "Arrangement of charge turned with the law in two windows" |
| 9–10 | "Repairs"; Figure 2 | Figure 2's labels ("PlaSim's clock", "circles: PlaSim's arithmetic alone", "synodic clock") clear of the curves and the title; circles visible on the curve |
| 11 | Text | The Titan sentence with "typically" and the haze's 80 km |
| 12 | Figure 3; text | Legend inside the frame, clear of the curves; the 35.0, 13.5 and 7.1 labels at the axis readable |
| 13 | Figure 4; "Verification" | Layer labels, legend and markers distinct; the legend clear of the points |
| 14–15 | Verification; "Results on the test world" | Text |
| 16 | Table 3; text | Run names in typewriter break inside their cell; the Sun-and-tilt row names the whole model days |
| 17 | Figure 5; text | Every bar labelled with its value; the off-scale first calibration labelled inside its bar; the hatched bars for two classes in one step distinct from the solid ones; the legend clear of the bars |
| 18 | Figure 6; text | The legend sits left of the data, clear of every marker |
| 19–20 | Results' end; "Reach to other worlds" | Text |
| 21–22 | Table 4 | One row (Seas) continues onto page 22 under "Table 4, continued"; the table reads correctly |
| 22–24 | "Next steps" | The charge paragraph's heading and text as revised |
| 24–26 | "Discussion and conclusions" | Text complete, ending on page 26 |
| 26 | Appendix; Table 5 | Table 5 whole, after its text and before Tables 6 and 7; about a tenth of the page left blank below it, as Table 6's caption and header start page 27 |
| 27–29 | Tables 6 and 7 | Continuation headers on pages 28 and 29; typewriter switch names legible |
| 29–30 | "Availability, authorship and review" | Review history through the eighth round |
| 30–34 | References | Every entry complete with its DOI or archive record; long hashes break inside the entry; one line of Paradise et al. (2025) set loosely around its hash (below) |

## Second renderer

MuPDF's renders of pages 4, 10, 12, 13, 17 and 18 match poppler's in every label, marker, line and fill. The one
difference: MuPDF draws a faint vertical seam inside the longest hatched bar of Figure 5, near +8.5 K, where the
hatch pattern's tiles meet; poppler draws none. It is a rendering difference of the pattern, with no change to the
bar's length or label.

## Findings

None blocking. For the author:

1. The title page dates the paper 17 October 2026, while the last revision and the PDF's metadata are dated 18
   October 2026 (`\date` in `main.tex`).
2. In the bibliography, one line of Paradise et al. (2025) is set with wide spaces before its sha256 (underfull box,
   badness 2894).
3. Table 4's last row stands alone on page 22 under its continued header.

## Page render hashes (first 16 hex digits of each PNG's sha256, 90 dpi)

| Page | poppler | MuPDF |
|---|---|---|
| 1 | 86fdade9a4aa2b28 | f7486921a784c455 |
| 2 | 5c3941318938bafe | eadbfe77f986df7e |
| 3 | 91af1103f0f843ca | 8bca90f5fbde0f85 |
| 4 | 6ff1d34362414050 | f4a16108a0851b13 |
| 5 | a479803e3d685d77 | fbcc7127ffd756cc |
| 6 | 00f68ab60cc2a70e | e9704b4e73c0d9b5 |
| 7 | 8940d7fcf42d0c0d | 7c12bd4d0a224cc7 |
| 8 | 3a92e6179c3b157d | 1f9bd2867b949e14 |
| 9 | b0d3883375f9ea31 | 63b4ef39c37b7c4b |
| 10 | 9d90a87fb462136d | 5ca363b3f1cfd591 |
| 11 | 6fbc9d17c20c417a | debadce8ef954e88 |
| 12 | b279c584d5173e84 | 9bf5acc4237d7f62 |
| 13 | 2214b7f21052c4d2 | 822fa011baa63f8a |
| 14 | ed991253a6fc1a83 | 18a8867ed2bb345a |
| 15 | 01d1f5b15a66914b | f653c2b9e455af6a |
| 16 | 94e39d74fdee0b35 | d2bfd42cba5124c7 |
| 17 | 8dabe0f8ab188ce3 | 12bfeb548bc89ea5 |
| 18 | c36d653e537b0e37 | ea186943a2a0bf77 |
| 19 | 9d0cd1146be08677 | cdb2677156973e8d |
| 20 | a990343939e8b409 | 5008a379cac148e4 |
| 21 | 7c95428748f8e47b | 2de11b85f67cd832 |
| 22 | ceca171303c1d24b | 461d3ff92b1bed6f |
| 23 | 5364d37fdf74e12c | 3f62e841e7a40173 |
| 24 | 016f4507c0de556e | 6455e4bf60d4ae67 |
| 25 | 9901c000da53da54 | 6a4ab4f2a7f7ee42 |
| 26 | 8ef0b7647933abec | ad60cd782bfa3313 |
| 27 | dda8d0ad3928ab87 | e08f4dbde1c6c9e1 |
| 28 | a85b72b6f9582373 | 07466e3880191a07 |
| 29 | 0c038388bbb696e8 | 6bd945ef3ad127af |
| 30 | 07b6b36b27e65941 | 625509bef6e8ebfd |
| 31 | 7d77035743174373 | 0b9de6cfd2c1de7e |
| 32 | 004df30e5779cb90 | 6d1dabbf1312911a |
| 33 | 7fe3d8b8cdc27c4b | 5fc0b9c745e8d56b |
| 34 | 99945ff434375cf5 | 47398444b1bf4009 |

## Result

**PASS** for the PDF with sha256 `c0c63cf1eff7c476a6913f0b06830f9d9a03ec8c48de50e099688d67aa17ff55`, built from
commit 94d337a. Any change to a build input changes the PDF and reopens this review.
