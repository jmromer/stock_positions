Stocks
======

A command-line tool to compute end-of-day positions for a given set of stocks,
read from CSVs.

Data
-----

### Input Data

- `start.csv`: stock positions (number of shares held) for the start of a given day
- `trades.csv`: transactions (position changes) throughout the same day may not
  be coextensive with the set of stocks in `start.csv`.
- `table.html`: HTML table relating ticker symbols to industrial sector

### Results Data

- `end.csv`: start of day portfolio for the following day. Each entry sums the
  start of day value and all subsequent trades for each stock in `start.csv`.
- `sector.csv`: for each sector, the number of shares held on the given day.

Usage
-----

Issue `./stock_positions` to see subcommand help.

```sh
./stock_positions --help

# Usage: stock_positions [OPTIONS] COMMAND [ARGS]...
#
# Options:
#   --help  Show this message and exit.
#
# Commands:
#   end-of-day     Calculate today's end-of-day positions.
#   eod-by-sector  Aggregate the day's positions by industry sector.
```

### end-of-day

```sh
./stock_positions end-of-day --help

# Usage: stock_positions end-of-day [OPTIONS]
#
#   Calculate today's end-of-day positions.
#
#   Print to stdout and save CSV summary to the default output path.
#
# Options:
#   --start TEXT   Start positions CSV path (local or URI)
#   --trades TEXT  Trades CSV path(s) (local or URI), comma-separated if
#                  multiple.
#   --out TEXT     Store result as CSV at this path.
#   --help         Show this message and exit.
```

```sh
Calculating end-of-day positions...
Using data from:
- https://raw.githubusercontent.com/clear-street/datasci-screening-jmromer/master/data/start.csv?token=ABB2QF5OCWUUWOP66BTDC4K57GGXS
- https://raw.githubusercontent.com/clear-street/datasci-screening-jmromer/master/data/trades.csv?token=ABB2QFZQ54WZL2LITM6362K57GI64

Results:
        shares_held
symbol
A           1864817
AAP        -3298989
ABBV       -1556626
ABC         2436387
ABT          878535
ACN         4028944
ADM         -794997
ADS         -530077
AEE        -1520723
AEP         3351904
AES         -609290
AFL         4493323
AGN        -1384731
AIG         -994018
AIV        -5605954
AIZ          -18026
...

Results CSV saved to ./results/end.csv
```

### eod-by-sector

```sh
./stock_positions eod-by-sector --help

# Usage: stock_positions eod-by-sector [OPTIONS]
#
#   Aggregate the day's positions by industry sector.
#
#   Print to stdout and save CSV summary to the default output path.
#
# Options:
#   --sectors TEXT  Path to HTML file containing sectors data table (local or
#                   URI)
#   --start TEXT    Start positions CSV path (local or URI)
#   --trades TEXT   Trades CSV path(s) (local or URI), comma-separated if
#                   multiple.
#   --out TEXT      Store result as CSV at this path.
#   --help          Show this message and exit.
```

```sh
Calculating end-of-day positions...
Using data from:
- https://raw.githubusercontent.com/clear-street/datasci-screening-jmromer/master/data/start.csv?token=ABB2QF5OCWUUWOP66BTDC4K57GGXS
- https://raw.githubusercontent.com/clear-street/datasci-screening-jmromer/master/data/trades.csv?token=ABB2QFZQ54WZL2LITM6362K57GI64

Calculating positions by sector...
Using data from:
- https://raw.githubusercontent.com/clear-street/datasci-screening-jmromer/master/data/table.html?token=ABB2QF5PEP4CNS2QCF5GDJK57GLI6

Results:
                        shares_held
sector
Communication Services     17543418
Consumer Discretionary    -29123263
Consumer Staples           31028909
Energy                     20474677
Financials                 47425709
Health Care                36026170
Industrials                 8244436
Information Technology     17527762
Materials                 -29528000
Real Estate               -20684352
Utilities                  23679353

Results CSV saved to ./results/sector.csv
```

Dependencies
------------

- python: anaconda3-2019.07 (set by `.tool-versions`)
- pandas
- click
- pytest

To install all dependencies, issue

```sh
conda create --name <env_name> --file requirements.txt
```

if using Anaconda.

Alternatively, assuming you've created and activated a virtualenv,

```sh
pip install -r requirements.txt
```

Testing
-------

Issue `pytest` from the project root to run tests.

```sh
% pytest
======================================= test session starts ========================================
platform darwin -- Python 3.7.5, pytest-5.3.1, py-1.8.0, pluggy-0.13.1
rootdir: /Users/jmromer/Desktop/datasci-screening-jmromer
collected 3 items

stocks_test.py ...                                                                           [100%]

======================================== 3 passed in 0.40s =========================================
```

Colophon
--------

- Operating system: macOS 10.15.1
- Text editor: Emacs 26.3
- Terminal type: iTerm2 3.3.20191207-nightly
- Scripting language: Python 3.7
