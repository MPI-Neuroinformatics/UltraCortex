from ultracortex import Runner
from ultracortex import create_all_plots
import pandas as pd
import argparse
import os

def main(participants, data_dir, output_dir):
    """
    Main function to calculate metrics and generate plots for the UltraCortex dataset.

    Parameters:
        participants (str): Path to the participants.tsv file.
        data_dir (str): Path to the BIDS dataset directory.
        output_dir (str): Path to the output directory.

    Returns:
        None
    """
    # Check if the data directory exists
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory {data_dir} not found.")

    # Check if the output directory exists and create it if not
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load participants data
    df = pd.read_csv(participants, sep='\t')

    # Initialize the Runner class and calculate metrics
    runner = Runner(df, data_dir, output_dir)
    runner.calculate_metrics()

    # Load the calculated metrics
    metrics = pd.read_csv(f"{output_dir}/metrics.csv")

    # Create plots using the calculated metrics
    create_all_plots(df, metrics, output_dir)

if __name__ == "__main__":
    # ArgumentParser to handle command-line arguments
    parser = argparse.ArgumentParser(description="Calculate metrics and plot them for the UltraCortex dataset")
    parser.add_argument("-p", "--participants", type=str, required=True, help="Path to the participants.tsv file")
    parser.add_argument("-d", "--data_dir", type=str, required=True, help="Path to the BIDS dataset directory")
    parser.add_argument("-o", "--output_dir", type=str, required=True, help="Path to the output directory")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Run the main function with parsed arguments
    main(args.participants, args.data_dir, args.output_dir)

