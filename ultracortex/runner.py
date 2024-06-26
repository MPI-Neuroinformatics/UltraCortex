"""Module aims to provide a wrapper to calculate MRI image quality metrics."""

import pandas as pd
from ultracortex.metrics import efc, anatomical_snr, cnr, cjv
import nibabel as nib
import numpy as np
import os
from tqdm import tqdm


class Runner:
    """
    A class to calculate various metrics for MRI images.

    It requires data structured in BIDS format.

    Attributes
    ----------
    df : pd.DataFrame
        DataFrame containing subject and session IDs.
    base_dir : str
        Base directory containing the MRI images.
    metrics_path : str
        Path to save the calculated metrics CSV file.

    """

    def __init__(self, df, base_dir, out_dir):
        """Initialize the Runner class with the data und directory paths.

        It uses the DataFrame, base directory, and output directory.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame with columns `SubID` and `SessionID`.
        base_dir : str
            Base directory containing the MRI images.
        out_dir : str
            Output directory to save the metrics CSV file.

        Returns
        -------
        None.

        """
        self.df = df
        self.base_dir = base_dir
        self.metrics_path = f"{out_dir}/metrics.csv"

    def calculate_metrics(self):
        """Calculate image quality metrics for each subject and session.

        The metrics to calculate are EFC, anatomical SNR, CNR, and CJV.
        Results are saved to a CSV file.

        Returns
        -------
        None.

        """
        # Initialize lists to store metrics for each subject and session
        subids = []
        sesids = []
        efcs = []
        t_snr = []
        cnrs = []
        cjvs = []

        # Iterate over each row in the DataFrame
        for i, row in tqdm(self.df.iterrows(), total=len(self.df)):
            subid = row["participant_id"]
            sesid = row["session_id"]
            subids.append(subid)
            sesids.append(sesid)

            # Load the anatomical image
            img_path = f"{self.base_dir}/{subid}/ses-{sesid}/anat/{subid}_ses-{sesid}_T1w.nii"
            img = nib.load(img_path)
            img_data = np.array(img.get_fdata(), dtype=np.int32)

            # Calculate EFC
            _efc = efc(img_data)
            if np.isnan(_efc) or np.isinf(_efc):
                print(f"Found NaN or Inf for {subid} ses-{sesid}")
            efcs.append(_efc)

            # Load skull-stripped image and calculate anatomical SNR
            skullstrip_path = f"{self.base_dir}/derivatives/skullstrips/{subid}_ses-{sesid}_skullstrip.nii"
            skullstrip = nib.load(skullstrip_path).get_fdata()
            t_snr.append(anatomical_snr(skullstrip))

            # Check if segmentation file exists to calculate CNR and CJV
            seg_path = f"{self.base_dir}/derivatives/manual_segmentation/{subid}_ses-{sesid}_seg.nii"
            if os.path.exists(seg_path):
                seg_img = nib.load(seg_path)
                seg = np.array(seg_img.get_fdata(), dtype=np.int32)

                # Normalize image data
                img_data_normalized = (
                    img_data - img_data.min()
                ) / (img_data.max() - img_data.min())

                # Calculate CNR and CJV
                _cnr = cnr(img_data_normalized, seg)
                _cjv = cjv(img_data_normalized, seg)

                cnrs.append(_cnr)
                cjvs.append(_cjv)
            else:
                cnrs.append(None)
                cjvs.append(None)

        # Create a DataFrame with the calculated metrics and save to CSV
        metrics_df = pd.DataFrame({
            "participant_id": subids,
            "session_id": sesids,
            "EFC": efcs,
            "T_SNR": t_snr,
            "CNR": cnrs,
            "CJV": cjvs
        })
        metrics_df.to_csv(self.metrics_path, index=False)
