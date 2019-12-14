from typing import Callable, List, Union

from pandas import DataFrame as DF


def calculating(title: str,
                sources: Union[List[str], str],
                out: Callable = print) -> None:
    if not isinstance(sources, list):
        sources = [sources]

    out(f"\nCalculating {title}...")
    out("Using data from:")
    for source in sources:
        out(f"- {source}")


def save_df_to_csv(df: DF, output_path: str, out: Callable = print) -> None:
    try:
        df.to_csv(output_path)
        out(f"\nResults CSV saved to {output_path}")
    except FileNotFoundError as err:
        out(f"\nFailed to write CSV to {output_path}")
        out(err)
