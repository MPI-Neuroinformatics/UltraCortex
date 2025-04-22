# UltraCortex MRI Metrics

## Overview

UltraCortex is a Python-based toolkit for calculating and visualizing various metrics for MRI images following the BIDS (Brain Imaging Data Structure) format. The toolkit includes metrics such as Entropy Focus Criterion (EFC), Anatomical Signal-to-Noise Ratio (SNR), Contrast-to-Noise Ratio (CNR), and Coefficient of Joint Variation (CJV). The related paper, dataset and project hub can be accessed via:

- Paper (Nature Scientific Data): [doi.org/10.1038/s41597-025-04779-2](https://doi.org/10.1038/s41597-025-04779-2)
- Data: [OpenNeuro](https://openneuro.org/datasets/ds005216)
- Project hub: [ultracortex.org](www.ultracortex.org)

## Features

- **EFC Calculation**: Quantifies ghosting and blurring in MRI images.
- **Anatomical SNR Calculation**: Measures image quality by comparing the mean signal to noise.
- **CNR Calculation**: Evaluates the ability to distinguish between white matter and gray matter.
- **CJV Calculation**: Assesses the variability within tissue types.
- **Visualization**: Generates histograms, KDE plots, and boxplots for metrics.

## Reference

```bibtex
@article{Mahler2025,
  title = {Submillimeter Ultra-High Field 9.4 T Brain MR Image Collection and Manual Cortical Segmentations},
  volume = {12},
  ISSN = {2052-4463},
  url = {http://dx.doi.org/10.1038/s41597-025-04779-2},
  DOI = {10.1038/s41597-025-04779-2},
  number = {1},
  journal = {Scientific Data},
  publisher = {Springer Science and Business Media LLC},
  author = {Mahler,  Lucas and Steiglechner,  Julius and Bender,  Benjamin and Lindig,  Tobias and Ramadan,  Dana and Bause,  Jonas and Birk,  Florian and Heule,  Rahel and Charyasz,  Edyta and Erb,  Michael and Kumar,  Vinod Jangir and Hagberg,  Gisela E. and Martin,  Pascal and Lohmann,  Gabriele and Scheffler,  Klaus},
  year = {2025},
  month = apr 
}
```
## Installation

To install UltraCortex, you need to have Python 3.7+ installed. Clone the repository and install the required dependencies using `pip`:

```bash
git clone https://github.com/MPI-NeuroInformatics/UltraCortex.git
cd ultracortex
pip install -r requirements.txt
```

## Usage

### Command Line Interface

You can use UltraCortex from the command line to calculate metrics and generate plots.

```bash
python main.py -d /path/to/data_dir -o /path/to/output_dir
```

#### Arguments:

- `-d, --data_dir`: Path to the BIDS dataset directory.
- `-o, --output_dir`: Path to the output directory.

### Example

```bash
python main.py -d ./data/bids_dataset -o ./output
```

## Modules

### Runner

The `Runner` class calculates various metrics for MRI images.

#### Methods:

- `__init__(self, df, base_dir, out_dir)`: Initializes the Runner with a DataFrame, base directory, and output directory.
- `calculate_metrics(self)`: Calculates EFC, SNR, CNR, and CJV metrics for each subject and session and saves them to a CSV file.

### Plotting Functions

- `histplot_2kde(df, metric, xlabel, out_dir)`: Creates a histogram with overlaid KDE plots for the given metric.
- `boxplot_segmentation(df, out_dir)`: Creates boxplots for the CNR and CJV metrics.
- `create_all_plots(participants, metrics, out_dir)`: Generates all plots for the given participants and metrics data.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes. Make sure to include tests for any new features or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

This toolkit is based on work from various contributors and inspired by existing MRI processing tools.
