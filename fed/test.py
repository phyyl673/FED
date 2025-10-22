from data import load_gdp_data, clean_gdp_data

df = load_gdp_data(
    "gdp_whole.csv",
    start_year=2000,
    end_year=2022,
    save_path="data_remove.csv"
)

df_clean = clean_gdp_data(
    df, 
    fill_method="interpolate", 
    save_path="data_clean.csv"
)


