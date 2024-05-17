import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_2histograms(mprage, mp2rage):
    # Set the aesthetic style of the plots
    sns.set(style="whitegrid")

    # Create the histogram using seaborn
    plt.figure(figsize=(12, 8))
    sns.histplot(data=mprage, binwidth=0.01, alpha=0.9, element='step', stat="density", kde=True, label='MPRAGE')
    sns.histplot(data=mp2rage,binwidth=0.01, alpha=0.3, element='step', stat="density", kde=True, label='MP2RAGE')

    plt.xlabel('EFC Value', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.title('Histogram of EFC Values for MPRAGE and MP2RAGE Sequences', fontsize=16)
    plt.legend()
    plt.show()

def histplot_2kde(df, metric, xlabel):
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 8))
    

    sns.histplot(data=df, x=metric, hue="Sequence", hue_order=["MPRAGE", "MP2RAGE"], binwidth=0.01,  multiple="stack", element='bars', stat="count", legend=True)
    sns.kdeplot(data=df, x=metric, hue="Sequence", hue_order=["MPRAGE", "MP2RAGE"], fill=True, alpha=0.3, multiple="stack", legend=False)
    # sns.kdeplot(data=df, x=metric,  alpha=0.4, color="black", linewidth=2, label="Overall KDE", legend=True)
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel('Count', fontsize=20)
    # increase size of ticks
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    # plt.legend()
    plt.tight_layout()
    plt.savefig(f"{metric}_histplot_2kde.png")
    plt.show()

def create_all_plots(participants, metrics):
    # join subjects and metrics dataframes on SubID and SesID
    df = pd.merge(participants, metrics, on=["SubID", "SessionID"])

    histplot_2kde(df, "EFC", "EFC")
    histplot_2kde(df, "T_SNR", "SNR")

    
