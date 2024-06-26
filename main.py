"""MRI Image Dataset Evaluater.

This script allows the user to calculate relevant quality metrics and plot
them.

This tool accepts strings to input and output directories. It assumes that the
data is organized in BIDS format with an organizing
`./derivatives/scanning_parameters.tsv` existing.

This script was used to generate reported results in
L. Mahler, J Steiglechner, et al. 2024.
UltraCortex: Submillimeter Ultra-High Field 9.4 T Brain MR Image Collection and
Manual Cortical Segmentations.

"""

from ultracortex import Runner
from ultracortex import create_all_plots
import pandas as pd
import argparse
import os


def print_statistics(df):
    """Print statistics for the given DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to print statistics for.

    Returns
    -------
    None.

    """
    print(f"EFC: Mean = {df['EFC'].mean()}, Std = {df['EFC'].std()}")
    print(f"T_SNR: Mean = {df['T_SNR'].mean()}, Std = {df['T_SNR'].std()}")
    segs = df[df.CNR.notnull() & df.CJV.notnull()]
    print(f"CNR: Mean = {segs['CNR'].mean()}, Std = {segs['CNR'].std()}")
    print(f"CJV: Mean = {segs['CJV'].mean()}, Std = {segs['CJV'].std()}")


def main(data_dir, output_dir):
    """Calculate metrics and generate plots for a dataset, e.g. UltraCortex.

    Parameters
    ----------
    data_dir : str
        Path to the BIDS dataset directory.
    output_dir : str
        Path to the output directory.

    Raises
    ------
    FileNotFoundError
        If data_dir does not exist.

    Returns
    -------
    None.

    """
    # Check if the data directory exists
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory {data_dir} not found.")

    # Check if the output directory exists and create it if not
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    participants = data_dir + "/derivatives/scanning_parameters.tsv"

    # Load participants data
    df = pd.read_csv(participants, sep='\t')

    # Initialize the Runner class and calculate metrics
    runner = Runner(df, data_dir, output_dir)
    runner.calculate_metrics()

    # Load the calculated metrics
    metrics = pd.read_csv(f"{output_dir}/metrics.csv")

    # Create plots using the calculated metrics
    create_all_plots(df, metrics, output_dir)
    print_statistics(metrics)


if __name__ == "__main__":
    # ArgumentParser to handle command-line arguments
    parser = argparse.ArgumentParser(
        description="Calculate metrics and plot them for the UltraCortex dataset")
    parser.add_argument("-d", "--data_dir", type=str,
                        required=True, help="Path to the BIDS dataset directory")
    parser.add_argument("-o", "--output_dir", type=str,
                        required=True, help="Path to the output directory")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Run the main function with parsed arguments
    main(args.data_dir, args.output_dir)
