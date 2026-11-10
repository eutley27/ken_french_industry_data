#############
## Imports ##
#############

from settings import END_DATE
import io
from pathlib import Path
import pandas as pd

###############
## Variables ##
###############

RAW_FILE = Path(__file__).resolve().parent.parent / "data_raw" / "12_Industry_Portfolios.csv"
OUTPUT_FILE = Path(__file__).resolve().parent.parent / "_output" / "french_12_ind_vw_monthly.csv"
TITLE = "Average Value Weighted Returns -- Monthly"
MISSING = (-99.99, -999)

###############
## Functions ##
###############

def find_table(path=RAW_FILE, title=TITLE):
    
    """
    Find table via its `title`.
    """
    
    lines = path.read_text(encoding="latin-1").splitlines()

    matches = [i for i, ln in enumerate(lines) if ln.strip() == title]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one line titled {title!r}, found {len(matches)}")

    header = matches[0] + 1  # the line with the industry names
    end = header + 1
    while end < len(lines) and lines[end].strip():  # stop at the first blank line
        end += 1

    df = pd.read_csv(io.StringIO("\n".join(lines[header:end])), index_col=0)
    df.columns = [c.strip() for c in df.columns]
    return df


def convert_dates(df):
    
    """
    Turn YYYYMM index into month-end dates.
    """

    df = df.copy()
    df.index = pd.to_datetime(df.index.astype(str), format="%Y%m") + pd.offsets.MonthEnd(0)
    df.index.name = "date"
    return df


def to_decimals(df):
    
    """
    Change missing markers to NAN.
    Convert percent to decimals.
    """

    df = df.astype(float)
    df = df.mask(df.isin(MISSING))  # markers become NaN
    return (df / 100).round(4)  # source has 2 decimals in percent, so 4 as decimals


def apply_cutoff(df, end_date=END_DATE):
    
    """
    Enforce end date.
    """

    return df.loc[df.index <= end_date]


def write_output(df, path=OUTPUT_FILE):
    
    """
    Write cleaned table.
    Fixed line endings keep the bytes the same on every OS.
    """
    
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, lineterminator="\n")


##########
## Main ##
##########

if __name__ == "__main__":
    df = apply_cutoff(to_decimals(convert_dates(find_table())))
    write_output(df)
    print(f"Wrote {len(df)} rows, {df.index[0].date()} to {df.index[-1].date()}")