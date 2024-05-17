import pandas as pd
from ultracortex.metrics import efc, anatomical_snr, cnr, cjv
import nibabel as nib
import numpy as np
import os
from tqdm import tqdm



class Runner:
    def __init__(self, df, base_dir):
        self.df = df
        self.base_dir = base_dir

    def calculate_metrics(self):
        # of course this is bids style

        subids = []
        sesids = []
        efcs = []
        t_snr = []
        cnrs = []
        cjvs = []

        for i, row in tqdm(self.df.iterrows(), total=len(self.df)):
            subid = row["SubID"]
            subids.append(subid)
            sesid = row["SessionID"]
            sesids.append(sesid)
            

            img = nib.load(f"{self.base_dir}/sub-{subid}/ses-{sesid}/anat/sub-{subid}_T1w.nii")
            img_data = np.array(img.get_fdata(), dtype=np.int32)

            _efc = efc(img_data)


            if np.isnan(_efc) or np.isinf(_efc):
                print(f"Found NaN or Inf for sub-{subid} ses-{sesid}")

            efcs.append(_efc)

            # skullstrip 
            skullstrip = nib.load(f"{self.base_dir}/derivatives/skullstrips/sub-{subid}_ses-{sesid}_skullstrip.nii").get_fdata()
            t_snr.append(anatomical_snr(skullstrip))

            # if seg is availabel calculate cnrs and cjvs
            seg_p = f"{self.base_dir}/derivatives/manual_segmentation/sub-{subid}_ses-{sesid}_seg.nii"
            if os.path.exists(seg_p):
                # print(f"Seg for sub-{subid} ses-{sesid}")
                seg_img = nib.load(seg_p)
                seg = np.array(seg_img.get_fdata(), dtype=np.int32)

                # normalize image_data
                img_data = (img_data - img_data.min()) / (img_data.max() - img_data.min())


                _cnr = cnr(img_data, seg)
                _cjv = cjv(img_data, seg)


                cnrs.append(_cnr)
                cjvs.append(_cjv)

            else:
                cnrs.append(None)
                cjvs.append(None)

        df = pd.DataFrame({
            "SubID": subids,
            "SessionID": sesids,
            "EFC": efcs,
            "T_SNR": t_snr,
            "CNR": cnrs,
            "CJV": cjvs
        })
        df.to_csv("metrics.csv", index=False)


