# keo-ledger

Football **tip ledger** for students who collect kèo as files (1 file = 1 leg).

Parse ticket filenames, store CSV, settle W/L, report winrate by tipster.

```
2026-07-08_jonny_denmark-italy_U2.5_FT.jpg
```

## Install

```bash
pip install -e .
keo parse ./inbox
keo settle --csv tickets.csv --scores scores.json
keo report tickets.csv
```

## Filename convention

`YYYY-MM-DD_tipster_match_market_period.ext`

- market: `O1.5` `U2.5` `AH-1.75` `COR-O9.5`
- period: `FT` `HT` `LIVE`

## License

MIT
