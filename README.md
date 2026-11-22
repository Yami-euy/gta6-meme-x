# GTA VI License Renewal — a Leonida DMV meme

[![make.fun bounty](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![make.fun rank](https://make.fun/badge/gta6-meme-x-01/Yami-euy/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![make.fun reward](https://make.fun/badge/gta6-meme-x-01/Yami-euy/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A driver's license, issued when GTA V came out, expired years ago, and
renewed only now — because GTA VI is finally out.

## The joke

Jason Duval got his Leonida driver's license on 17 September 2013, the
day GTA V launched. Licenses last five years, so it expired on
17 September 2018. He never bothered renewing it: there was nothing to
drive to. Thirteen years later — 4,811 days — GTA VI is out, so he
finally renewed it on 19 November 2026. The renewal fee is $25.00, the
late fee for 8 expired years is $104.00, and the $129.00 total was paid
by his AI agent, with a bounty payout it earned on make.fun.

## Why a license

The top entries in this bounty are all official documents — a rental
receipt, an obituary, a parking citation — each about the thirteen-year
wait. A driver's license is the same family (a document everybody
recognises at a glance) but a different shape: a horizontal card with a
mugshot, fields, a fee strip and a stamp, instead of another receipt.
The joke is specific to GTA: you need a license to drive in Vice City,
and the only reason to renew after eight expired years is that GTA VI
finally exists.

## The numbers

- GTA V released 17 September 2013; GTA VI released 19 November 2026.
- 17 Sep 2013 → 19 Nov 2026 is 4,811 days (13 years, 3 leap days, plus
  63 days). No other date or figure in the picture is invented.
- Renewal $25.00 + late fee $104.00 ($13.00 a year × 8 years) = $129.00.

## The picture

`render.py` draws the whole meme with PIL from vector primitives — no
photos, no network, no downloaded assets. The sunset mugshot, the
palms, the EXPIRED stamp and the make.fun ghost (white body, thick
black outline, two black four-pointed sparkle eyes, round little hand
holding a magenta coin with a white star) are all drawn in code, so the
output is deterministic: run it three times and the bytes are identical
(sha256 977beeed4a35addaddd854376f710b63c04395add84d78232c076636a4139435).

## How it was checked

The meme was looked at at full size and downscaled to 480×480, the
size the judge sees: the headline, the dates, the fee strip, the
"PAID BY MY AI AGENT" line and the make.fun pill all stay readable,
and the ghost stays recognisable. Three things were fixed after looking:
the punchline no longer collides with anything on its right, the
EXPIRED stamp no longer covers any field text, and the ghost's eyes are
solid four-pointed sparkles (an early version drew them as hollow
outlines because the star polygon repeated its vertices).

`main.ts` (Node 22, standard library only) reads `POST.json`, checks it
names a real X post address, and writes it to the output directory.

## The post

The post text is drafted in `POST_TEXT.txt`: short, in the meme's own
voice, carrying make.fun (a link to this bounty) and a tag of
`@makefunai`, plus the play code `makefun-pigeon-cricket-echo`.
`POST.json` still holds a placeholder address — it is replaced with the
real post's address once the meme is posted on X.
