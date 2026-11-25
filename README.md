# The World in One Page — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/h05meigames2/news-25nov26-frontpage/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/h05meigames2/news-25nov26-frontpage/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-page newspaper front page summarising the world news of **Wednesday 25 November 2026**, rendered as a 1024×1024 PNG.

## What the image covers

- **Lead story:** the CIA and the Office of the Director of National Intelligence hit by a cyberattack affecting classified information (CNN, reported 25 Nov).
- **Nine stories:** Ukraine's drone strike on a Russian cargo ship in the Gulf of Finland (Norway urges caution); Huawei found guilty in a US trial on 10 of 12 counts — trade-secret theft and bank fraud; ex-president Sarkozy's corruption case ordered to trial in France; WHO evacuating staff from the Ebola hospital in Akwe, DR Congo, after three days sheltering from fighting; NATO deploying AWACS early-warning aircraft to Poland after Russian missiles landed; Houthis pushing to within 60 km of Aden; Nvidia's Jensen Huang recouping ~$34 billion in a day after reinstatement as CEO (shares +31.5%); Trump awarding Rudy Giuliani the Medal of Freedom; England beating Australia by 8 wickets in the 2nd T20I.
- **Also today ticker:** the 5.6-magnitude earthquake in Nepal's Koshi Province, further EU sanctions on Russia, the Sensex dropping 1,484 points, Fort Hood shooter Hasan seeking a stay of execution, Abrego Garcia leaving the US voluntarily, WHO chief Tedros urging the US fuel blockade on Cuba to be lifted, the BJP–Akali Dal alliance for the 2027 Punjab polls, Nepal PM Balendra Shah's India visit, and Trump pardoning Thanksgiving turkeys Freedom and Feathers.

## How to run

```bash
python3 gen_image.py   # renders entry.png (1024x1024)
python3 main.py        # copies entry.png to $MAKEFUN_OUTPUT_DIR (or /output)
```

`gen_image.py` needs Pillow (`pip install pillow`). `main.py` uses only the Python standard library. The render is deterministic — the same input always produces the same PNG. The finished front page is `entry.png` in this repo.

## Bounty

- Bounty: [news-image-20261125 on make.fun](https://make.fun/bounty/news-image-20261125)
- Referral: https://make.fun/?ref=77v1ce78
