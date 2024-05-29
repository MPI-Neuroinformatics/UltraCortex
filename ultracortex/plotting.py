import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def histplot_2kde(df, metric, xlabel, out_dir):
    """
    Create a histogram with overlaid KDE plots for the given metric.

    Parameters:
        df (pandas.DataFrame): DataFrame containing the data.
        metric (str): Column name of the metric to plot.
        xlabel (str): Label for the x-axis.
        out_dir (str): Directory to save the plot image.

    Returns:
        None
    """
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 8))

    # Plot histogram with stacked bars for different sequences
    hist_plot = sns.histplot(
        data=df, 
        x=metric, 
        hue="Sequence", 
        hue_order=["MP-RAGE", "MP2RAGE"], 
        binwidth=0.01, 
        multiple="stack", 
        element='bars', 
        stat="count", 
        legend=True
    )

    
    # Overlay KDE plots for different sequences
    sns.kdeplot(
        data=df, 
        x=metric, 
        hue="Sequence", 
        hue_order=["MP-RAGE", "MP2RAGE"], 
        fill=True, 
        alpha=0.3, 
        multiple="stack", 
        legend=False
    )

    plt.xlabel(xlabel, fontsize=24)
    plt.ylabel('Count', fontsize=24)
    plt.xticks(fontsize=20)  # Increase size of x-ticks
    plt.yticks(fontsize=20)  # Increase size of y-ticks
    # Adjust the legend font size
    legend = hist_plot.legend_
    for text in legend.get_texts():
        text.set_fontsize(24)
    legend.set_title("")

    plt.tight_layout()
    plt.savefig(f"{out_dir}/{metric}_histplot_2kde.png", dpi=300)
    plt.show()

def boxplot_segmentation(df, out_dir):
    """
    Create boxplots for the CNR and CJV metrics.

    Parameters:
        df (pandas.DataFrame): DataFrame containing the data.
        out_dir (str): Directory to save the plot image.

    Returns:
        None
    """
    data = df[["CNR", "CJV"]].dropna()  # Drop rows with NaN values in CNR or CJV

    sns.set(style="whitegrid")
    plt.figure(figsize=(6, 7))

    # Create boxplots for CNR and CJV
    sns.boxplot(data=data)

    plt.xticks(fontsize=18)  # Increase size of x-ticks
    plt.yticks(fontsize=18)  # Increase size of y-ticks

    plt.tight_layout()
    plt.savefig(f"{out_dir}/segmentation_boxplot.png")
    plt.show()

def create_all_plots(participants, metrics, out_dir):
    """
    Generate all plots for the given participants and metrics data.

    Parameters:
        participants (pandas.DataFrame): DataFrame containing participants information.
        metrics (pandas.DataFrame): DataFrame containing metrics data.
        out_dir (str): Directory to save the plot images.

    Returns:
        None
    """
    # Merge participants and metrics DataFrames on SubID and SessionID
    df = pd.merge(participants, metrics, on=["SubID", "SessionID"])

    # Generate histograms with KDE plots for EFC and T_SNR
    histplot_2kde(df, "EFC", "EFC", out_dir)
    histplot_2kde(df, "T_SNR", "SNR", out_dir)

    # Generate boxplot for segmentation metrics (CNR and CJV)
    boxplot_segmentation(df, out_dir)
   
