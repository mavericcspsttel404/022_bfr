import pandas as pd


def save_large_dfs_to_excel(
    dfs: dict[str, pd.DataFrame],
    file_path: str,
) -> None:
    """
    Save large DataFrames to separate sheets efficiently using xlsxwriter.

    Args:
        dfs (dict): Dictionary where keys are sheet names and values are DataFrames.
        file_path (str): Path to the output Excel file (e.g., 'output.xlsx').

    Returns:
        None
    """
    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        for sheet_name, df in dfs.items():
            safe_sheet_name = str(sheet_name)[:31]  # Excel sheet name limit
            df.to_excel(writer, sheet_name=safe_sheet_name, index=False)
