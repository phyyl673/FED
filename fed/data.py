import pandas as pd
from pathlib import Path
from typing import List, Optional, Union


def load_gdp_data(
    filepath: Union[str, Path],
    countries: Optional[List[str]] = None,
    start_year: int = 2000,
    end_year: int = 2022,
    save_path: Optional[Union[str, Path]] = None
) -> pd.DataFrame:
    """
    Load and preprocess GDP data from a World Bank CSV file.
    Optionally save the cleaned data to a new CSV file.

    Parameters
    ----------
    filepath : str or Path
        Path to the downloaded World Bank GDP CSV file.
    countries : list of str
        List of countries to include (default:
        ['United States', 'United Kingdom', 'Brazil',
          'Japan', 'China', 'Germany', 'Switzerland'])
    start_year : int, optional
        First year to include (default: 2000)
    end_year : int, optional
        Last year to include (default: 2022)
    save_path : str or Path, optional
        If provided, saves the cleaned dataset to this file.

    Returns
    -------
    pd.DataFrame
        A tidy DataFrame with columns ['country', 'year', 'gdp_usd'].
    """
    # Convert file path to Path object and check existence
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path.resolve()}")

    # 1. Read the CSV (skip the first 4 metadata
    # rows typical for World Bank datasets)
    df = pd.read_csv(path, skiprows=4)

    # 2. Use default list of countries if none are specified
    if countries is None:
        countries = [
            "United States",
            "United Kingdom",
            "Brazil",
            "Japan",
            "China",
            "Germany",
            "Switzerland"
        ]

    # 3. Keep only selected countries
    df = df[df["Country Name"].isin(countries)]

    # 4. Extract relevant year columns
    year_cols = [str(y) for y in range(start_year, end_year + 1)]

    # 5. Transform from wide to long format
    df_long = df.melt(
        id_vars=["Country Name"],
        value_vars=year_cols,
        var_name="year",
        value_name="gdp_usd"
    )

    # 6. Convert data types
    df_long["year"] = df_long["year"].astype(int)
    df_long["gdp_usd"] = pd.to_numeric(df_long["gdp_usd"], errors="coerce")

    # 7. Rename columns for clarity
    df_long = df_long.rename(columns={"Country Name": "country"})

    print(
        f"Loaded GDP data for {len(countries)}countries"
        f"({start_year}–{end_year}) from {path.name}"
        )

    # 8. Save cleaned data if requested
    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        df_long.to_csv(save_path, index=False)
        print(f"Cleaned data saved to {save_path.resolve()}")

    return df_long


# define function of cleaning data


def clean_gdp_data(
    df: pd.DataFrame,
    fill_method: Optional[str] = "interpolate",
    save_path: Optional[Union[str, Path]] = None
) -> pd.DataFrame:
    """
    Clean GDP data:
    - Fill missing values within each country (default: linear interpolation)
    - Convert GDP to billions of USD
    - Round to 2 decimal places
    - Optionally save the cleaned data to CSV

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with columns ['country','year','gdp_usd'].
    fill_method : {"interpolate","ffill","bfill", None}, optional
        How to fill missing values (default: interpolate).
    save_path : str or Path, optional
        If provided, saves the cleaned data to this file.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame with columns
        ['country','year','gdp_billion','gdp_unit'].
    """
    out = df.copy()

    # 1. Fill missing values (default = linear interpolation)
    if fill_method in {"ffill", "bfill"}:
        out["gdp_usd"] = (
            out.sort_values(["country", "year"])
               .groupby("country", group_keys=False)["gdp_usd"]
               .apply(lambda s: s.ffill()
                      if fill_method == "ffill" else s.bfill())
        )
    elif fill_method == "interpolate":
        out["gdp_usd"] = (
            out.sort_values(["country", "year"])
               .groupby("country", group_keys=False)["gdp_usd"]
               .apply(lambda s: s.interpolate(limit_direction="both"))
        )
    # None → do nothing

    # 2️. Convert to billions and round
    out["gdp_billion"] = (out["gdp_usd"] / 1e9).round(2)
    out["gdp_unit"] = "billion USD"

    # 3️. Keep only clean columns
    out = out[["country", "year", "gdp_billion",
               "gdp_unit"]].sort_values(["country", "year"])

    # 4️. Save if needed
    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        out.to_csv(save_path, index=False)
        print(f" Cleaned data saved to {save_path.resolve()}")

    return out
