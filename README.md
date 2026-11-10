
# Ken French 12 Industry Portfolios (value-weighted, monthly)

Monthly returns of the 12 Fama-French industry portfolios, cleaned so that
other pipelines can depend on them. Built for the FINM 32800 class report.

## Source

Kenneth R. French Data Library, "12 Industry Portfolios":
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

The raw file, `data_raw/12_Industry_Portfolios.csv`, is committed unchanged.
It was created by Ken French from the 202609 CRSP database (the file says so
in its first line). The code downloads nothing, so the same commit always
produces the same output.

## What the code does

`src/clean_french.py` reads the table titled
`Average Value Weighted Returns -- Monthly` and then:

1. finds that table by its full title and fails if it is missing or duplicated,
2. converts the `YYYYMM` dates to month-end dates (`2026-09-30`),
3. blanks out Ken French's missing-data markers (`-99.99`, `-999`) and
   converts percent to decimals, rounded to 4 places,
4. drops every month after `END_DATE`,
5. writes `_output/french_12_ind_vw_monthly.csv`.

## Output

One row per month, one column per industry (wide), plus a `date` column.

- Dates: month-end, from 1926-07-31 to 2026-09-30.
- Units: decimal returns (`0.0367` is 3.67%). Missing values are blank.
- Industries: NoDur, Durbl, Manuf, Enrgy, Chems, BusEq, Telcm, Utils,
  Shops, Hlth, Money, Other.
- Weighting: value-weighted. The equal-weighted table is in the raw file but
  is not used.

## Cutoff

`END_DATE` is a committed constant in `src/settings.py` (2026-09-30). The code
reads nothing past it, and it is never set from `.env`.

## Rebuild

```
cd src
python clean_french.py
```

Requires Python and pandas.

## Data branch

The finished CSV is published on the `report-data` branch, together with a
`chartbook.toml`, for use as a ChartBook `git` dependency.