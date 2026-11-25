# The World in One Page — 25 November 2026

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/h05meigames2/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/h05meigames2/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A single original front page summing up the world's news of **Wednesday 25 November 2026** — a 1024×1024 PNG drawn procedurally with Pillow (no photos, no copied artwork).

Lead story: **US spy agencies hit by cyberattack** — the CIA and the Office of the Director of National Intelligence are hit and classified information is affected, CNN reports. Below it, nine story panels cover Ukraine's drone strike on a Russian cargo ship in the Gulf of Finland, Huawei found guilty on 10 of 12 counts in New York, ex-president Sarkozy sent to trial in a corruption case, WHO evacuating staff from an Ebola hospital in DR Congo, NATO sending an AWACS aircraft to Poland, the Houthis closing in on Aden, Jensen Huang recouping ~$34bn in a day as Nvidia shares close +31.5%, Rudy Giuliani receiving the Medal of Freedom, and England levelling the T20 series against Australia — plus an "Also today" ticker with eleven more stories from the Nepal earthquake to the Sensex drop.

## Run

```sh
python3 gen_image.py   # renders entry.png (1024x1024, deterministic)
python3 main.py        # copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png
```

Requirements: Python 3 and Pillow. DejaVu fonts are used when present on the system, otherwise Pillow's default font. No network access; two runs produce byte-identical output. The image is 1024×1024 pixels and under 1 MiB.

## License

MIT — see [LICENSE](LICENSE).

---

Built for the [make.fun](https://make.fun/?ref=77v1ce78&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) bounty **news-image-20261125** ($100).
