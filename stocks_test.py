import io
from inspect import cleandoc

import pandas as pd

import stocks


def build_df(rows: str, cols=None) -> pd.DataFrame:
    cols = cols or ["symbol", "shares_held"]
    csv = io.StringIO(cleandoc(rows))
    df = pd.read_csv(csv, names=cols, skipinitialspace=True)
    df = df.set_index(cols[0])
    return df


def test_movement_history_df():
    csv1 = """
    AA, 100
    AB, -40
    """
    df1 = build_df(csv1)

    csv2 = """
    AA, -40
    ZZ, -100
    """
    df2 = build_df(csv2)

    csv3 = """
    AA, 10
    ZB, -100
    """
    df3 = build_df(csv3)

    result_df = stocks.movement_history_df([df1, df2, df3])

    assert list(result_df.index) == ["AA", "AB", "AA", "AA"]
    assert list(result_df["shares_held"]) == [100, -40, -40, 10]


def test_grouped_sum():
    csv = """
    AA, 100
    AB, -40
    AA, -100
    AA, 50
    AA, 80
    """
    result_df = stocks.grouped_sum(build_df(csv),
                                   key_col="symbol",
                                   value_col="shares_held")

    assert list(result_df.index) == ["AA", "AB"]
    assert list(result_df.loc["AA"]) == [130]
    assert list(result_df.loc["AB"]) == [-40]


def test_aggregate_by_sector():
    positions_csv = """
    AA, 100
    AB, -10
    AC, 50
    """
    positions_df = build_df(positions_csv, cols=["symbol", "shares_held"])
    sector_csv = """
    AA, technology
    AB, technology
    AC, agriculture
    """
    sectors_df = build_df(sector_csv, cols=["symbol", "sector"])

    result_df = stocks.aggregate_by_sector(positions_df, sectors_df)

    assert list(result_df.index) == ["agriculture", "technology"]
    assert list(result_df.loc["technology"]) == [90]
    assert list(result_df.loc["agriculture"]) == [50]
