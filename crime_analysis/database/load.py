# load_duckdb.py
import os
from typing import Optional
import pandas as pd
import duckdb


def save_to_duckdb(
    df: pd.DataFrame,
    db_path: Optional[str] = None,
    table_name: str = "crime_records",
    if_exists: str = "append"
) -> int:
    """
    Save preprocessed DataFrame into DuckDB.

    :param df: preprocessed DataFrame (index should be datetime or include 'Date' column)
    :param db_path: path to DuckDB file; defaults to in-memory if None
    :param table_name: target table name in DuckDB
    :param if_exists: 'replace', 'append', or 'fail'
    :return: number of inserted rows
    """
    db_path = db_path or ":memory:"  # in-memory if not specified

    # Connect to DuckDB
    con = duckdb.connect(database=db_path)

    # Reset index if it's a datetime index and ensure column name is 'date'
    if isinstance(df.index, pd.DatetimeIndex):
        df = df.reset_index().rename(columns={"index": "date"})
    elif "Date" in df.columns:
        df = df.rename(columns={"Date": "date"})
    else:
        raise ValueError("DataFrame must have a DateTime index or 'Date' column")

    # DuckDB can infer types automatically, so we can just use to_sql
    df.to_sql(table_name, con, if_exists=if_exists, index=False)

    inserted_rows = len(df)
    con.close()
    return inserted_rows


# Example usage
if __name__ == "__main__":
    df = pd.read_csv("chicago_crimes.csv", parse_dates=["Date"])
    # preprocess df as before...
    n = save_to_duckdb(df, db_path="chicago_crimes.duckdb")
    print(f"Inserted {n} rows into DuckDB")

