from ultracortex import Runner
from ultracortex import create_all_plots
import pandas as pd

# argparser

# parser = argparse.ArgumentParser(description="Calculate metrics and plot them for the UltraCortex dataset")
# parser.add_argument("--metrics", type

df = pd.read_csv('participants.tsv', sep='\t')
runner = Runner(df, "/mnt/DATA/datasets/ultracortex_bids_test")
runner.calculate_metrics()

metrics = pd.read_csv('metrics.csv')
create_all_plots(df, metrics)
