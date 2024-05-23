""" 
Image Quality Metrics were adopted from MRIQC v.24.0 to work with 9.4T MRI data. 
https://mriqc.readthedocs.io/en/24.0.0/iqms/t1w.html
"""
import numpy as np

# Define constants for segmentation labels
WM_LABELS = [2, 41]  # White matter labels
GM_LABELS = [3, 42]  # Gray matter labels
BG_LABELS = [0]      # Background labels

def efc(img, framemask=None, decimals=4):
    """
    Calculate the Entropy Focus Criterion (EFC) for an image.
    
    The EFC uses the Shannon entropy of voxel intensities to indicate ghosting
    and blurring induced by head motion. Lower EFC values indicate better focus,
    with EFC = 0 when all the energy is concentrated in one pixel.

    Parameters:
    img (numpy.ndarray): Input image data.
    framemask (numpy.ndarray, optional): Mask of empty voxels inserted after a rotation of the data. 
                                         If None, defaults to an array of zeros with the same shape as img.

    Returns:
    float: The calculated EFC value.
    """

    if framemask is None:
        framemask = np.zeros_like(img, dtype=np.uint8)

    n_vox = np.sum(1 - framemask)
    # Calculate the maximum value of the EFC (which occurs any time all
    # voxels have the same value)
    efc_max = 1.0 * n_vox * (1.0 / np.sqrt(n_vox)) * np.log(1.0 / np.sqrt(n_vox))

    # Calculate the total image energy
    b_max = np.sqrt((img[framemask == 0] ** 2).sum())

    # Calculate EFC (add 1e-16 to the image data to keep log happy)
    return round(
        float(
            (1.0 / efc_max)
            * np.sum(
                (img[framemask == 0] / b_max) * np.log((img[framemask == 0] + 1e-16) / b_max)
            ),
        ),
        decimals,
    )


def anatomical_snr(img, decimals=4):
    """
    Calculate the anatomical Signal-to-Noise Ratio (SNR) of an MRI image.
    
    SNR is defined as the mean of the image divided by its standard deviation, 
    adjusted for bias in finite samples. Higher SNR indicates better image quality 
    with less random noise.

    Parameters:
    img (numpy.ndarray): The MRI image data.

    Returns:
    float: The computed SNR value, adjusted for the bias in finite samples.
    """
    mean_intensity = np.mean(img)
    std_intensity = np.std(img)
    n_voxels = img.size

    snr_value = mean_intensity / (std_intensity * np.sqrt(n_voxels / (n_voxels - 1)))
    return round(snr_value, decimals)

def cnr(img, seg, decimals=4):
    """
    Calculate the Contrast-to-Noise Ratio (CNR) between white matter and gray matter in an MRI image.
    
    CNR measures the ability to distinguish between different tissue types based on the contrast of 
    their signal intensities relative to the noise level.

    Parameters:
    img (numpy.ndarray): The MRI image data.
    seg (numpy.ndarray): Segmentation array corresponding to the MRI image, 
                         where different values represent different tissue types.

    Returns:
    float: The calculated CNR value for white matter versus gray matter.
    """
    wm_mask = np.isin(seg, WM_LABELS)
    gm_mask = np.isin(seg, GM_LABELS)
    bg_mask = np.isin(seg, BG_LABELS)

    mean_wm = np.mean(img[wm_mask])
    std_wm = np.std(img[wm_mask])
    mean_gm = np.mean(img[gm_mask])
    std_gm = np.std(img[gm_mask])
    std_bg = np.std(img[bg_mask])

    cnr_value = (mean_wm - mean_gm) / np.sqrt(std_bg**2 + std_wm**2 + std_gm**2)
    return round(cnr_value, decimals)

def cjv(img, seg, decimals=4):
    """
    Calculate the Coefficient of Joint Variation (CJV) for white matter and gray matter in an MRI image.
    
    CJV measures the combined variability of the signal intensities of two tissue types, normalized 
    by the difference in their means. Lower CJV values indicate better homogeneity of voxel intensities 
    within tissue types.

    Parameters:
    img (numpy.ndarray): The MRI image data.
    seg (numpy.ndarray): Segmentation array corresponding to the MRI image, 
                         where different values represent different tissue types.

    Returns:
    float: The CJV value, indicating the variability relative to the mean difference between 
           white and gray matter.
    """
    wm_mask = np.isin(seg, WM_LABELS)
    gm_mask = np.isin(seg, GM_LABELS)

    mean_wm = np.mean(img[wm_mask])
    std_wm = np.std(img[wm_mask])
    mean_gm = np.mean(img[gm_mask])
    std_gm = np.std(img[gm_mask])

    cjv_value = (std_wm + std_gm) / abs(mean_wm - mean_gm)
    return round(cjv_value, decimals)

