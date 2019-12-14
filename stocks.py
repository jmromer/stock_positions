from functools import reduce
from typing import Dict, List, Tuple

import pandas as pd
from pandas import DataFrame as DF


def movement_history_df(dfs: List[DF]) -> DF:
    """
    Given a list of DataFrames `df`, aggregate a complete history by
    concatenating the stock start positions with subsequent trading deltas.

    The first entry is assumed to hold start positions for the day.

    Return a DataFrame.
    """
    if not dfs:
        return pd.DataFrame()

    start_positions_df, *delta_dfs = dfs  # type: Tuple[DF, List[DF]]

    if not delta_dfs:
        return start_positions_df

    # determine which stocks common across all trade data
    common_stocks: pd.Index = reduce(lambda x, y: x.intersection(y),
                                     (df.index for df in delta_dfs)).unique()

    # slice out common stocks from all trade data frames
    delta_dfs = [df.loc[common_stocks] for df in delta_dfs]

    # return concatenated stock values and deltas
    return start_positions_df.append(delta_dfs)


def end_of_day_positions(paths: List[str]) -> DF:
    """
    Compute the end-of-day position for each stock found in the given CSVs.

    Read CSV data from the given paths list `paths`
    The first CSV in the list should consist of start-of-day positions.
    The remaining entries should be trades.

    Return a DataFrame.
    """
    column_names: List[str] = ["symbol", "shares_held"]
    dfs: List[DF] = [pd.read_csv(path, names=column_names) for path in paths]

    # Concatenate start positions and trade deltas
    df: DF = movement_history_df(dfs)

    # Sum stock-wise to compute end-of-day positions
    df = df.pipe(grouped_sum, *column_names)

    return df


def grouped_sum(df: DF, key_col: str, value_col: str) -> DF:
    """
    Group DataFrame `df` by the values in column `key_col` and aggregate by
    summing the values in `value_col`.

    Return a DataFrame indexed by `key_col`.
    """
    df = df.copy()
    df = df.groupby(key_col).sum()
    return df


def positions_by_sector(positions_df: DF, sector_table_html_path: str) -> DF:
    """
    Aggregate stock positions in the given DataFrame `positions_df` by industry
    sector.

    Takes industry data from HTML table at `sector_table_html_path`.

    Return a DataFrame.
    """
    # column names corresponding to that found in HTML table
    html_cols: List[str] = ["Symbol", "GICS Sector"]
    normalized_cols: List[str] = ["symbol", "sector"]
    col_mappings: Dict[str, str] = dict(zip(html_cols, normalized_cols))

    # map stock symbol to industry sector label
    sectors_df: DF = (pd
                      .read_html(sector_table_html_path)[0]
                      .loc[:, html_cols]
                      .rename(columns=col_mappings)
                      .set_index("symbol"))  # yapf: disable

    # sum positions values per sector
    df = positions_df.pipe(aggregate_by_sector, sectors_df)

    return df


def aggregate_by_sector(positions_df: DF, sectors_df: DF) -> DF:
    """
    Aggregate stock data given in DataFrame `positions_df` by industry sector,
    provided in `sectors_df`.

    Return a DataFrame.
    """
    positions_df = positions_df.copy()
    positions_df = positions_df.join(sectors_df).groupby("sector").sum()
    return positions_df
