import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_gdp_trends(df: pd.DataFrame, save_path: str | None = None) -> None:
    """
    Plot GDP trends over time for selected countries.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing ['country', 'year', 'gdp_billion'] columns.
    save_path : str or None, optional
        File path to save the plot (default: None).

    Returns
    -------
    None
        This function displays and optionally saves the plot.
    """
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="year", y="gdp_billion", hue="country", marker="o")

    plt.title("GDP Trends (2000–2022)")
    plt.xlabel("Year")
    plt.ylabel("GDP (billion USD)")
    plt.grid(True, alpha=0.3)
    plt.legend(title="Country", loc="upper left")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to {save_path}")
    plt.show()
