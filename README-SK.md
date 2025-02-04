# skpodcasty.sk podcast downloader

English guide here: [README.md](README.md)

Jednoduchý nástroj na sťahovanie podcastov zo skpodcasty.sk. Program vytvorí priečinok s názvom podcastu, stiahne, zoradí a pomenuje všetky dostupné epizódy.

## Funkcie

- Automatická detekcia počtu stránok a epizód
- Sťahovanie po častiach
- Grafické rozhranie pre jednoduché použitie
- Zachovanie poradia epizód podľa dátumu publikácie
- Rešpektuje rate limiting servera pomocou časových odstupov medzi sťahovaniami
- V prípade chyby pri sťahovaní program pokračuje ďalšou epizódou
- Podporuje len podcasty zo skpodcasty.sk

## Požiadavky

- Python 3.12/3.13
- requests
- beautifulsoup4

## Inštalácia

1. Nainštalujte [Python](https://www.python.org/) 3.12/3.13

2. Nainštalujte potrebné balíčky:
```bash
pip install requests
pip install beautifulsoup4
```

## Použitie

1. Spustite skript dvojklikom alebo v konzole:

```bash
python skpodcasty.py
```

2. Do okna vložte URL adresu podcastu zo skpodcasty.sk
   - Príklad: `https://skpodcasty.sk/podcasts/nazov-podcastu`

3. Kliknite na tlačidlo "Stiahnuť"

4. Program vytvorí priečinok s názvom podcastu a stiahne všetky epizódy do tohto priečinka

## Výstup

- Stiahnuté súbory sú pomenované vo formáte: `{nazov-podcastu}_{cislo_epizody}_{id_epizody}.mp3`

- Príklad: `nazov-podcastu_001_id-epizody.mp3`

## Licencia

Zadarmo

